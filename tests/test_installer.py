import importlib.util
import os
from pathlib import Path
import stat
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, call, patch


source = Path(__file__).resolve().parents[1] / "secux-installer" / "main.py"
spec = importlib.util.spec_from_file_location("installer", source)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class EspCheckTests(unittest.TestCase):
    def test_space_thresholds(self):
        device = SimpleNamespace(st_mode=stat.S_IFBLK, st_rdev=10)
        mount = SimpleNamespace(st_dev=10)
        with patch.object(installer, "os", wraps=os) as filesystem:
            filesystem.stat.side_effect = lambda path: device if path == "/dev/esp" else mount
            for kernels, mib in ((1, 384), (2, 640), (3, 896)):
                with self.subTest(kernels=kernels):
                    limit = mib * 1024 ** 2
                    space = SimpleNamespace(f_bavail=limit, f_frsize=1, f_flag=0)
                    filesystem.statvfs.return_value = space
                    filesystem.ST_RDONLY = os.ST_RDONLY
                    installer.check_esp_space("/dev/esp", "/efi", kernels, require_writable=True)
                    space.f_bavail -= 1
                    with self.assertRaisesRegex(installer.EspCheckError, str(mib)):
                        installer.check_esp_space("/dev/esp", "/efi", kernels)
                    space.f_bavail = limit
                    space.f_flag = os.ST_RDONLY
                    installer.check_esp_space("/dev/esp", "/efi", kernels)
                    with self.assertRaises(installer.EspCheckError):
                        installer.check_esp_space("/dev/esp", "/efi", kernels, require_writable=True)

    def test_wrong_mount_device(self):
        device = SimpleNamespace(st_mode=stat.S_IFBLK, st_rdev=10)
        with patch.object(installer, "os", wraps=os) as filesystem:
            filesystem.stat.side_effect = [device, SimpleNamespace(st_dev=11)]
            with self.assertRaises(installer.EspCheckError):
                installer.check_esp_space("/dev/esp", "/efi", 1)

    def test_rejects_alias_of_esp_as_root(self):
        device = SimpleNamespace(st_mode=stat.S_IFBLK, st_rdev=10)
        with patch.object(installer, "os", wraps=os) as filesystem:
            filesystem.stat.return_value = device
            with self.assertRaises(installer.EspCheckError):
                installer.validate_manual_partitions("/dev/esp", "/dev/alias")

    def test_failed_probe_does_not_skip_validation(self):
        with patch.object(installer.tempfile, "mkdtemp", return_value="/probe"), \
                patch.object(installer.os, "rmdir") as rmdir, \
                patch.object(installer.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "mount")), \
                patch.object(installer, "check_esp_space") as check:
            with self.assertRaises(installer.EspCheckError):
                installer.check_manual_esp("/dev/esp", 1)
            check.assert_not_called()
            rmdir.assert_called_once_with("/probe")

    def test_unmounts_after_space_check_failure(self):
        error = installer.EspCheckError("title", "low space")
        with patch.object(installer.tempfile, "mkdtemp", return_value="/probe"), \
                patch.object(installer.os, "rmdir") as rmdir, \
                patch.object(installer.subprocess, "run") as run, \
                patch.object(installer, "check_esp_space", side_effect=error):
            with self.assertRaisesRegex(installer.EspCheckError, "low space"):
                installer.check_manual_esp("/dev/esp", 1)
            self.assertEqual(run.call_args_list, [
                call(["sudo", "mount", "-t", "vfat", "-o", "ro", "/dev/esp", "/probe"], check=True),
                call(["sudo", "umount", "/probe"], check=True),
            ])
            rmdir.assert_called_once_with("/probe")

    def test_preflight_rejection_stays_on_summary(self):
        class InstallPage:
            start_installation = Mock()

        page = InstallPage()
        window = SimpleNamespace(
            current_step_index=0,
            steps=[object(), page],
            partition_page=SimpleNamespace(get_config=lambda: {
                "mode": "manual", "efi_part": "/dev/esp", "root_part": "/dev/root",
            }),
            kernel_page=SimpleNamespace(get_selected_kernels=lambda: ["linux", "linux-lts"]),
            show_message_dialog=Mock(),
            nav_view=Mock(),
        )
        with patch.object(installer, "InstallPage", InstallPage), \
                patch.object(installer, "validate_manual_partitions"), \
                patch.object(installer, "check_manual_esp", side_effect=installer.EspCheckError("title", "low space")) as probe:
            installer.InstallerWindow.on_next_step(window, None, None)

        probe.assert_called_once_with("/dev/esp", 2)
        window.show_message_dialog.assert_called_once_with("title", "low space")
        page.start_installation.assert_not_called()
        window.nav_view.push.assert_not_called()
        self.assertEqual(window.current_step_index, 0)


class HostnameTests(unittest.TestCase):
    def test_hostname_validation(self):
        window = Mock()
        form = SimpleNamespace(
            entry_fullname=Mock(**{"get_text.return_value": "Secux User"}),
            entry_hostname=Mock(),
            entry_username=Mock(**{"get_text.return_value": "secux"}),
            entry_password=Mock(**{"get_text.return_value": "password"}),
            entry_confirm=Mock(**{"get_text.return_value": "password"}),
            error_stack=Mock(),
            get_native=lambda: window,
        )
        for hostname in ("Secux-01_PC", "_secux", "-secux"):
            with self.subTest(hostname=hostname):
                form.entry_hostname.get_text.return_value = hostname
                installer.UserPage.on_validate_and_next(form, None, None)
                window.activate_action.assert_called_once_with("win.next_step", None)
                self.assertEqual(installer.UserPage.get_user(form)["hostname"], hostname)
                window.reset_mock()

        for hostname in ("1secux", "secux.local", " secux", "secux ", "se cux", "секуx"):
            with self.subTest(hostname=hostname):
                form.entry_hostname.get_text.return_value = hostname
                form.error_stack.reset_mock()
                installer.UserPage.on_validate_and_next(form, None, None)
                form.error_stack.set_visible_child_name.assert_called_once_with("ascii_host")
                window.activate_action.assert_not_called()
