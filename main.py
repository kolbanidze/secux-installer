import sys
import os
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GObject, Gdk

import threading
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
import datetime
import subprocess
import gettext
from gettext import gettext as _
import locale
import time
import re

TIMEZONES = {'Africa': ['Abidjan', 'Accra', 'Addis_Ababa', 'Algiers', 'Asmara', 'Bamako', 'Bangui', 'Banjul', 'Bissau', 'Blantyre', 'Brazzaville', 'Bujumbura', 'Cairo', 'Casablanca', 'Ceuta', 'Conakry', 'Dakar', 'Dar_es_Salaam', 'Djibouti', 'Douala', 'El_Aaiun', 'Freetown', 'Gaborone', 'Harare', 'Johannesburg', 'Juba', 'Kampala', 'Khartoum', 'Kigali', 'Kinshasa', 'Lagos', 'Libreville', 'Lome', 'Luanda', 'Lubumbashi', 'Lusaka', 'Malabo', 'Maputo', 'Maseru', 'Mbabane', 'Mogadishu', 'Monrovia', 'Nairobi', 'Ndjamena', 'Niamey', 'Nouakchott', 'Ouagadougou', 'Porto-Novo', 'Sao_Tome', 'Tripoli', 'Tunis', 'Windhoek'], 'America': ['Adak', 'Anchorage', 'Anguilla', 'Antigua', 'Araguaina', 'Argentina/Buenos_Aires', 'Argentina/Catamarca', 'Argentina/Cordoba', 'Argentina/Jujuy', 'Argentina/La_Rioja', 'Argentina/Mendoza', 'Argentina/Rio_Gallegos', 'Argentina/Salta', 'Argentina/San_Juan', 'Argentina/San_Luis', 'Argentina/Tucuman', 'Argentina/Ushuaia', 'Aruba', 'Asuncion', 'Atikokan', 'Bahia', 'Bahia_Banderas', 'Barbados', 'Belem', 'Belize', 'Blanc-Sablon', 'Boa_Vista', 'Bogota', 'Boise', 'Cambridge_Bay', 'Campo_Grande', 'Cancun', 'Caracas', 'Cayenne', 'Cayman', 'Chicago', 'Chihuahua', 'Costa_Rica', 'Creston', 'Cuiaba', 'Curacao', 'Danmarkshavn', 'Dawson', 'Dawson_Creek', 'Denver', 'Detroit', 'Dominica', 'Edmonton', 'Eirunepe', 'El_Salvador', 'Fort_Nelson', 'Fortaleza', 'Glace_Bay', 'Godthab', 'Goose_Bay', 'Grand_Turk', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guayaquil', 'Guyana', 'Halifax', 'Havana', 'Hermosillo', 'Indiana/Indianapolis', 'Indiana/Knox', 'Indiana/Marengo', 'Indiana/Petersburg', 'Indiana/Tell_City', 'Indiana/Vevay', 'Indiana/Vincennes', 'Indiana/Winamac', 'Inuvik', 'Iqaluit', 'Jamaica', 'Juneau', 'Kentucky/Louisville', 'Kentucky/Monticello', 'Kralendijk', 'La_Paz', 'Lima', 'Los_Angeles', 'Lower_Princes', 'Maceio', 'Managua', 'Manaus', 'Marigot', 'Martinique', 'Matamoros', 'Mazatlan', 'Menominee', 'Merida', 'Metlakatla', 'Mexico_City', 'Miquelon', 'Moncton', 'Monterrey', 'Montevideo', 'Montserrat', 'Nassau', 'New_York', 'Nipigon', 'Nome', 'Noronha', 'North_Dakota/Beulah', 'North_Dakota/Center', 'North_Dakota/New_Salem', 'Ojinaga', 'Panama', 'Pangnirtung', 'Paramaribo', 'Phoenix', 'Port-au-Prince', 'Port_of_Spain', 'Porto_Velho', 'Puerto_Rico', 'Rainy_River', 'Rankin_Inlet', 'Recife', 'Regina', 'Resolute', 'Rio_Branco', 'Santarem', 'Santiago', 'Santo_Domingo', 'Sao_Paulo', 'Scoresbysund', 'Sitka', 'St_Barthelemy', 'St_Johns', 'St_Kitts', 'St_Lucia', 'St_Thomas', 'St_Vincent', 'Swift_Current', 'Tegucigalpa', 'Thule', 'Thunder_Bay', 'Tijuana', 'Toronto', 'Tortola', 'Vancouver', 'Whitehorse', 'Winnipeg', 'Yakutat', 'Yellowknife'], 'Antarctica': ['Casey', 'Davis', 'DumontDUrville', 'Macquarie', 'Mawson', 'McMurdo', 'Palmer', 'Rothera', 'Syowa', 'Troll', 'Vostok'], 'Arctic': ['Longyearbyen'], 'Asia': ['Aden', 'Almaty', 'Amman', 'Anadyr', 'Aqtau', 'Aqtobe', 'Ashgabat', 'Atyrau', 'Baghdad', 'Bahrain', 'Baku', 'Bangkok', 'Barnaul', 'Beirut', 'Bishkek', 'Brunei', 'Chita', 'Choibalsan', 'Colombo', 'Damascus', 'Dhaka', 'Dili', 'Dubai', 'Dushanbe', 'Famagusta', 'Gaza', 'Hebron', 'Ho_Chi_Minh', 'Hong_Kong', 'Hovd', 'Irkutsk', 'Jakarta', 'Jayapura', 'Jerusalem', 'Kabul', 'Kamchatka', 'Karachi', 'Kathmandu', 'Khandyga', 'Kolkata', 'Krasnoyarsk', 'Kuala_Lumpur', 'Kuching', 'Kuwait', 'Macau', 'Magadan', 'Makassar', 'Manila', 'Muscat', 'Nicosia', 'Novokuznetsk', 'Novosibirsk', 'Omsk', 'Oral', 'Phnom_Penh', 'Pontianak', 'Pyongyang', 'Qatar', 'Qyzylorda', 'Riyadh', 'Sakhalin', 'Samarkand', 'Seoul', 'Shanghai', 'Singapore', 'Srednekolymsk', 'Taipei', 'Tashkent', 'Tbilisi', 'Tehran', 'Thimphu', 'Tokyo', 'Tomsk', 'Ulaanbaatar', 'Urumqi', 'Ust-Nera', 'Vientiane', 'Vladivostok', 'Yakutsk', 'Yangon', 'Yekaterinburg', 'Yerevan'], 'Atlantic': ['Azores', 'Bermuda', 'Canary', 'Cape_Verde', 'Faroe', 'Madeira', 'Reykjavik', 'South_Georgia', 'St_Helena', 'Stanley'], 'Australia': ['Adelaide', 'Brisbane', 'Broken_Hill', 'Currie', 'Darwin', 'Eucla', 'Hobart', 'Lindeman', 'Lord_Howe', 'Melbourne', 'Perth', 'Sydney'], 'Europe': ['Amsterdam', 'Andorra', 'Astrakhan', 'Athens', 'Belgrade', 'Berlin', 'Bratislava', 'Brussels', 'Bucharest', 'Budapest', 'Busingen', 'Chisinau', 'Copenhagen', 'Dublin', 'Gibraltar', 'Guernsey', 'Helsinki', 'Isle_of_Man', 'Istanbul', 'Jersey', 'Kaliningrad', 'Kiev', 'Kirov', 'Lisbon', 'Ljubljana', 'London', 'Luxembourg', 'Madrid', 'Malta', 'Mariehamn', 'Minsk', 'Monaco', 'Moscow', 'Oslo', 'Paris', 'Podgorica', 'Prague', 'Riga', 'Rome', 'Samara', 'San_Marino', 'Sarajevo', 'Saratov', 'Simferopol', 'Skopje', 'Sofia', 'Stockholm', 'Tallinn', 'Tirane', 'Ulyanovsk', 'Uzhgorod', 'Vaduz', 'Vatican', 'Vienna', 'Vilnius', 'Volgograd', 'Warsaw', 'Zagreb', 'Zaporozhye', 'Zurich'], 'Indian': ['Antananarivo', 'Chagos', 'Christmas', 'Cocos', 'Comoro', 'Kerguelen', 'Mahe', 'Maldives', 'Mauritius', 'Mayotte', 'Reunion'], 'Pacific': ['Apia', 'Auckland', 'Bougainville', 'Chatham', 'Chuuk', 'Easter', 'Efate', 'Enderbury', 'Fakaofo', 'Fiji', 'Funafuti', 'Galapagos', 'Gambier', 'Guadalcanal', 'Guam', 'Honolulu', 'Johnston', 'Kiritimati', 'Kosrae', 'Kwajalein', 'Majuro', 'Marquesas', 'Midway', 'Nauru', 'Niue', 'Norfolk', 'Noumea', 'Pago_Pago', 'Palau', 'Pitcairn', 'Pohnpei', 'Port_Moresby', 'Rarotonga', 'Saipan', 'Tahiti', 'Tarawa', 'Tongatapu', 'Wake', 'Wallis']}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION = "0.0.5"

LOG_FILE = "/tmp/secux-install.log"

APP_ID = "secux-installer"
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

REPO_URL = "https://kolbanidze.github.io/secux-repo/x86_64/"

def get_ui_path(filename):
    return os.path.join(os.path.join(BASE_DIR, "ui"), filename)

def load_resources():    
    res = Gio.Resource.load("resources.gresource")
    
    Gio.resources_register(res)

    display = Gdk.Display.get_default()
    icon_theme = Gtk.IconTheme.get_for_display(display)
    
    icon_theme.add_resource_path("/org/secux/installer/icons")

def init_i18n():
    """Инициализация системы перевода для Python и GTK"""
    try:
        if os.environ.get("LANG") is None:
             os.environ["LANG"] = "en_US.UTF-8"
        
        locale.setlocale(locale.LC_ALL, '') 
    except locale.Error:
        print("Warning: Failed to set locale. Using default.")

    try:
        lang = gettext.translation(APP_ID, localedir=LOCALES_DIR, fallback=True)
        lang.install()
    except Exception as e:
        print(f"Python translation error: {e}")
        import builtins
        builtins._ = lambda x: x

    try:
        locale.bindtextdomain(APP_ID, LOCALES_DIR)
        
        if hasattr(locale, 'bind_textdomain_codeset'):
            locale.bind_textdomain_codeset(APP_ID, 'UTF-8')
        
        locale.textdomain(APP_ID)
        
        gettext.bindtextdomain(APP_ID, LOCALES_DIR)
        gettext.textdomain(APP_ID)
        
    except Exception as e:
        print(f"GTK/C translation bind error: {e}")


@Gtk.Template(filename=get_ui_path("install.ui"))
class InstallPage(Adw.NavigationPage):
    __gtype_name__ = "InstallPage"

    status_page = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    console_view = Gtk.Template.Child()
    btn_finish = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Буфер для текста консоли
        self.text_buffer = self.console_view.get_buffer()
        self.config = {}

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"--- Log started at {datetime.datetime.now()} ---\n")

    def start_installation(self, main_window):
        """
        Метод вызывается из InstallerWindow перед переходом на этот экран.
        Собираем все данные и запускаем поток.
        """

        self.config = {
            "source": main_window.source_page.get_source_mode(),
            "user": main_window.user_page.get_user(),
            "partition": main_window.partition_page.get_config(),
            "security": main_window.security_page.get_selected_mode(),
            "desktop": main_window.desktop_page.get_selected_de(),
            "timezone": main_window.timezone_page.get_timezone(),
            "encryption_pwd": main_window.encryption_page.get_password(),
            "kernels": main_window.kernel_page.get_selected_kernels(),
            "packages": main_window.software_page.get_selected_packages()
        }

        self.log(_("INFO: Сбор данных завершен. Начало установки..."))
        
        thread = threading.Thread(target=self._installation_sequence, daemon=True)
        thread.start()

    def update_console(self, text):
        print(text)
        GLib.idle_add(self._append_text, text)

    def _append_text(self, text):
        end_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert(end_iter, text)
        # Автоскролл вниз
        adj = self.console_view.get_parent().get_vadjustment()
        adj.set_value(adj.get_upper())

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"

        self.update_console(f"{full_message}\n")
        
        print(full_message)

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(full_message + "\n")
        except Exception as e:
            print(_(f"Error writing to log file: {e}"))


    def set_progress(self, fraction):
        GLib.idle_add(self.progress_bar.set_fraction, fraction)

    def execute(self, cmd: list, input_str: str = None, shell=False):
        """
        Выполняет команду, пишет вывод в лог UI.
        Поддерживает передачу input_str (например, пароли) в stdin.
        """
        cmd_str = " ".join(cmd)
        self.log(f"> {cmd_str}")

        try:
            process = subprocess.Popen(
                ["sudo"] + cmd,
                stdin=subprocess.PIPE if input_str else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=shell
            )

            if input_str:
                stdout_data, _ = process.communicate(input=input_str + "\n")
                if stdout_data:
                    self.update_console(stdout_data)
            else:
                for line in process.stdout:
                    self.update_console(line)
            
            process.wait()
            
            if process.returncode != 0:
                self.log("ERROR: Command failed with code " + process.returncode)
                return process.returncode
            
            return 0

        except Exception as e:
            self.log(e)
            return 1

    def __list_partitions(self, drive):
        result = subprocess.run(['lsblk', '-ln', '-o', 'NAME,TYPE'], stdout=subprocess.PIPE, text=True)
        partitions = []
        for line in result.stdout.splitlines():
            name, type_ = line.split()
            if type_ == 'part' and name.startswith(drive.replace('/dev/', '')):
                partitions.append(f"/dev/{name}")
        return partitions

    def __split_device(self, device):
        match = re.match(r"(.+?)(p?\d+)$", device)
        if match:
            base, num = match.groups()
            if base.endswith("p"):  # Remove trailing 'p' for nvme devices
                base = base[:-1]
            return base, num.lstrip("p")  # Remove 'p' from number
        return device, ""

    def _get_ucode_package(smth):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "vendor_id" in line:
                        if "GenuineIntel" in line:
                            return ["intel-ucode"]
                        elif "AuthenticAMD" in line:
                            return ["amd-ucode"]
            return ["amd-ucode", "intel-ucode"]
        except FileNotFoundError:
            return ["amd-ucode", "intel-ucode"]

    def _installation_sequence(self):
        """
        Основная логика установки. Выполняется последовательно.
        """
        try:
            # === ЭТАП 1: Подготовка диска ===
            self.set_progress(0.1)
            part_conf = self.config["partition"]
            
            if part_conf["mode"] == "auto":
                drive = part_conf["target"]
                self.log(_("INFO: Автоматическая разметка диска ") + drive)

                if self.execute(['sgdisk', '-Z', drive]) != 0:
                    self.log(_("ОШИБКА: не удалось форматировать диск"))
                    self.an_error_occurred()
                    return

                if self.execute(['sgdisk', f'-n1:0:+1G', '-t1:ef00', '-c1:EFI', '-N2', '-t2:8304', drive]) != 0:
                    self.log(_("ОШИБКА: не удалось создать разделы"))
                    self.an_error_occurred()
                    return
                
                partitions = self.__list_partitions(drive)
                if len(partitions) < 2:
                    self.log(_("ОШИБКА: не удалось найти разделы"))
                    self.an_error_occurred()
                    return
                
                efi_partition = partitions[0]
                rootfs_partition = partitions[1]
                self.log(f"EFI: {efi_partition}, Root: {rootfs_partition}")
            else:
                self.log(_("INFO: Используется ручная разметка."))
                efi_partition = part_conf["efi_part"]
                rootfs_partition = part_conf["root_part"]
                self.log(F"EFI: {efi_partition}, Root: {rootfs_partition}")

                efi_base_drive, efi_number = self.__split_device(efi_partition)
                self.execute(['sgdisk', f'--typecode={efi_number}:ef00', efi_base_drive])
            
            if not efi_partition or not rootfs_partition:
                self.log(_("ОШИБКА: не удалось определить разделы"))
                self.an_error_occurred()
                return
            
            swap_size = part_conf["swap_size"]
            self.log(_("Размер файла подкаки: ") + str(swap_size))

            # === ЭТАП 2: LUKS, LVM ===
            self.set_progress(0.2)
            self.execute(['cryptsetup', 'luksFormat', rootfs_partition], input_str=self.config["encryption_pwd"]) 
            self.execute(['cryptsetup', 'luksOpen', rootfs_partition, 'cryptlvm'], input_str=self.config["encryption_pwd"])
            
            self.execute(['pvcreate', '/dev/mapper/cryptlvm'])
            self.execute(['vgcreate', 'volumegroup', '/dev/mapper/cryptlvm'])
            
            self.execute(['lvcreate', '-l', '100%FREE', 'volumegroup', '-n', 'root']) 
            
            root_lv_path = "/dev/volumegroup/root"
            self.execute(['mkfs.ext4', root_lv_path])
                    
            if part_conf['mode'] == "auto":
                self.execute(['mkfs.fat', '-F32', efi_partition])
            
            mount_point = '/mnt'
            efi_mount_point = os.path.join(mount_point, 'efi')

            self.execute(['mount', root_lv_path, mount_point])
            if swap_size > 0:
                swap_path = os.path.join(mount_point, "swapfile")
                self.execute(['fallocate', '-l', f'{str(swap_size)}G', swap_path])
                self.execute(['chmod', '600', swap_path])
                self.execute(['mkswap', swap_path])
                self.execute(['swapon', swap_path])
                
            # === ЭТАП 3: Монтирование ===
            self.set_progress(0.3)
            self.log(_("INFO: Монтирование файловых систем..."))
            self.execute(['mount', '--mkdir', '-o', 'uid=0,gid=0,fmask=0077,dmask=0077', efi_partition, efi_mount_point])

            # === ЭТАП 4: Настройка репозиториев ===
            self.set_progress(0.35)
            if self.config['source'] == "online":   
                self.execute(['cp', '/etc/pacman_online.conf', '/etc/pacman.conf'])
            else:
                self.execute(['cp', '/etc/pacman_offline.conf', '/etc/pacman.conf'])
                self.execute(['pacman-key', '--init'])
                self.execute(['pacman-key', '--populate', 'archlinux'])
                self.execute(['pacman-key', '--populate', 'kolbanidze'])

            # === ЭТАП 5: Установка системы ===
            self.set_progress(0.4)
            self.log(_("INFO: Установка пакетов операционной системы"))
            
            self.execute(['bash', '-c', f'rm -rf {mount_point}/efi/loader/entries/secux-*'])

            # Логика выбора пакетов
            kernels = self.config["kernels"]
            user_packages = self.config["packages"]
            kernels.extend([i+'-headers' for i in kernels])

            pacstrap_packages = ['base', 'base-devel', 'linux-firmware', 'vim', 'nano', 'efibootmgr', 'sudo', 'plymouth', 'python-pip', 'lvm2', 'networkmanager', 'systemd-ukify', 'sbsigntools', 'efitools', 'less', 'git', 'ntfs-3g', 'gvfs', 'gvfs-mtp', 'xdg-user-dirs', 'fwupd', 'apparmor', 'ufw', 'flatpak', 'mokutil', 'python-argon2-cffi', 'python-pycryptodome', 'tpm2-tools', 'secux-hooks']
            pacstrap_packages.extend(self._get_ucode_package())
            pacstrap_packages.extend(kernels)
            pacstrap_packages.extend(user_packages)

            if self.config['desktop'] == 'gnome':
                pacstrap_packages.extend(["xorg", "gnome", "networkmanager-openvpn", "gnome-tweaks", "gdm"])
            elif self.config['desktop'] == 'kde':
                pacstrap_packages.extend(["xorg", "plasma", "networkmanager-openvpn", "kde-applications"])
            
            if self.config['security'] == "secure_full":
                pacstrap_packages.extend(['sbctl'])
            elif self.config['security'] == "secure_compat":
                pacstrap_packages.extend(['shim-signed'])
            
            pacstrap_cmd = ['stdbuf', '-oL', 'pacstrap', '-K', mount_point] + pacstrap_packages
            self.execute(pacstrap_cmd)
            
            # === ЭТАП 6: Настройка системы ===
            self.set_progress(0.6)
            self.log(_("INFO: Настройка операционной системы"))

            # Adding custom repo
            repo_conf_line = f'\n[kolbanidze]\nServer = {REPO_URL}\n'
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e "{repo_conf_line}" >> /etc/pacman.conf'])
            self.execute(['cp', '/usr/share/pacman/keyrings/kolbanidze.gpg', f'{mount_point}/usr/share/pacman/keyrings/'])
            self.execute(['cp', '/usr/share/pacman/keyrings/kolbanidze-trusted', f'{mount_point}/usr/share/pacman/keyrings/'])
            self.execute(['arch-chroot', mount_point, 'pacman-key', '--populate', 'kolbanidze'])

            self.set_progress(0.62)
            self.execute(['bash', '-c', 'genfstab -U /mnt >> /mnt/etc/fstab']) 

            self.execute(['arch-chroot', mount_point, 'useradd', '-m', self.config['user']['username'], '-c', self.config['user']['fullname']])
            
            # Configuring timezone
            timezone = self.config["timezone"]
            self.execute(['arch-chroot', '/mnt', 'ln', '-sf', f'/usr/share/zoneinfo/{timezone}', '/etc/localtime'])
            
            # Настройка пользователя
            user = self.config["user"]
            self.log(f"INFO: Создание пользователя {user['username']}...")
            self.execute(['arch-chroot', '/mnt', 'useradd', '-m', user['username'], '-c', user['fullname']])
            self.execute(['arch-chroot', '/mnt', 'passwd', user['username']], input_str=f"{user['password']}\n{user['password']}")

            sudoers_line = '"%wheel ALL=(ALL:ALL) ALL"'
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo {sudoers_line} >> /etc/sudoers']) 
            self.execute(['arch-chroot', mount_point, 'usermod', '-aG', 'wheel', user['username']])

            self.set_progress(0.7)
            # Creating mkinitcpio.conf
            mkinitcpio_conf_content = "MODULES=()\nBINARIES=()\nFILES=()\nHOOKS=(base systemd autodetect microcode modconf kms keyboard sd-vconsole plymouth block sd-encrypt lvm2 filesystems fsck)\n"
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e \'{mkinitcpio_conf_content}\' > /etc/mkinitcpio.conf'])

            # Creating cmdline
            self.execute(['arch-chroot', mount_point, 'mkdir', '-p', '/etc/cmdline.d'])
            process = subprocess.run(["blkid", '-s', 'UUID', '-o', 'value', rootfs_partition], check=True, capture_output=True)
            uuid = process.stdout.strip().decode()
            cmdline_content = f"rd.luks.name={uuid}=cryptlvm root={root_lv_path} rw rootfstype=ext4 rd.shell=0 rd.emergency=reboot audit=1 quiet oops=panic init_on_alloc=1 init_on_free=1 pti=on lockdown=confidentiality lsm=landlock,lockdown,yama,integrity,apparmor,bpf splash"
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{cmdline_content}" > /etc/cmdline.d/root.conf'])

            self.set_progress(0.8)

            # Creating UKI config
            uki_conf_content = "[UKI]\nOSRelease=@/etc/os-release\nPCRBanks=sha256\n\n[PCRSignature:initrd]\nPhases=enter-initrd\nPCRPrivateKey=/etc/kernel/pcr-initrd.key.pem\nPCRPublicKey=/etc/kernel/pcr-initrd.pub.pem\n"
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e \'{uki_conf_content}\' > /etc/kernel/uki.conf'])

            # Generate ukify keys
            self.execute(['arch-chroot', mount_point, 'ukify', 'genkey', '--config=/etc/kernel/uki.conf'])

            current_lang = os.environ.get("LANG", "en_US.UTF-8")
            setup_english = True
            setup_russian = False
            if "ru" in current_lang.lower():
                setup_russian = True
            
            if setup_english:
                self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen'])
            if setup_russian:
                self.execute(['arch-chroot', mount_point, 'bash', '-c', 'echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen'])
            
            self.execute(['arch-chroot', mount_point, 'locale-gen'])
            self.execute(['arch-chroot', mount_point, 'bash', '-c', 'echo "FONT=cyr-sun16" >> /etc/vconsole.conf'])

            # Set plymouth theme
            self.execute(['rm', '-rf', f'{mount_point}/usr/share/plymouth/themes'])
            self.execute(['cp', '-r', '/usr/share/plymouth/themes/', f'{mount_point}/usr/share/plymouth/themes/'])
            self.execute(['arch-chroot', mount_point, 'plymouth-set-default-theme', 'bgrt-nologo']) 

            # Prepare EFI Partition
            self.execute(['mkdir', '-p', f'{mount_point}/efi/EFI/secux'])

            # Delete previous UKI if exists
            self.execute(['bash', '-c', f'rm -rf {mount_point}/efi/EFI/secux/*'])

            # Change distro info and logo
            installer_path = "/usr/local/share/secux-installer"

            # Mitigated by secux-hooks
            # self.execute(['cp', f'{installer_path}/images/SecuxLinux.svg', f'{mount_point}/usr/share/icons/'])

            self.execute(['rm', '-f', f'{mount_point}/usr/share/factory/etc/ssh/sshd_config.d/99-archlinux.conf'])
            self.execute(['rm', '-f', f'{mount_point}/etc/debuginfod/archlinux.urls'])
            self.execute(['rm', '-f', f'{mount_point}/etc/ssh/sshd_config.d/99-archlinux.conf'])
            self.execute(['rm', '-f', f'{mount_point}/etc/arch-release'])
            self.execute(['rm', '-f', f'{mount_point}/usr/share/factory/etc/arch-release'])
            self.execute(['rm', '-f', f'{mount_point}/usr/share/plymouth/themes/spinner/watermark.png'])

            self.execute(['arch-chroot', mount_point, 'mkinitcpio', '-P'])
            
            self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'NetworkManager.service'])
            self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'systemd-timesyncd.service'])
            self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'auditd.service'])
            self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'apparmor.service'])
            self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'ufw.service'])

            if self.config["desktop"] == "GNOME":
                self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'gdm.service'])

            elif self.config["desktop"] == "KDE":
                self.execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'sddm.service'])
                self.execute(['sed', '-i', 's/^Current=.*/Current=breeze/', f'{mount_point}/usr/lib/sddm/sddm.conf.d/default.conf'])

            # Hostname
            hostname = self.config['user']["hostname"]
            self.execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{hostname}" > /etc/hostname'])
            
            self.execute(['arch-chroot', mount_point, 'bootctl', 'install', '--esp-path=/efi']) 

            default_kernel_conf = ""
            if 'linux-hardened' in self.config['kernels']: default_kernel_conf = "secux-linux-hardened.conf"
            elif 'linux-lts' in self.config['kernels']: default_kernel_conf = "secux-linux-lts.conf"
            elif 'linux' in self.config['kernels']: default_kernel_conf = "secux-linux.conf"

            self.set_progress(0.9)

            loader_conf_content = f"timeout 3\ndefault {default_kernel_conf}\nconsole-mode keep\nreboot-for-bitlocker yes"
            self.execute(['bash', '-c', f'echo -e "{loader_conf_content}" > {mount_point}/efi/loader/loader.conf'])

            for kernel in self.config['kernels']:
                entry_content = f"title Secux Linux ({kernel})\nefi /EFI/secux/secux-{kernel}.efi\n"
                entry_fallback_content = f"title Secux Linux ({kernel}-fallback)\nefi /EFI/secux/secux-{kernel}-fallback.efi\n"
                self.execute(['bash', '-c', f'echo -e "{entry_content}" > {mount_point}/efi/loader/entries/secux-{kernel}.conf'])
                self.execute(['bash', '-c', f'echo -e "{entry_fallback_content}" > {mount_point}/efi/loader/entries/secux-{kernel}-fallback.conf'])

            if self.config["security"] == "secure_full":
                self.execute(['arch-chroot', mount_point, 'sbctl', 'create-keys'])
                self.execute(['arch-chroot', mount_point, 'sbctl', 'enroll-keys', '--yes-this-might-brick-my-machine'])
                self.execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', '/efi/EFI/BOOT/BOOTX64.EFI'])
                self.execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', '/efi/EFI/systemd/systemd-bootx64.efi'])
                for kernel in self.config['kernels']:
                    self.execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', f'/efi/EFI/secux/secux-{kernel}.efi'])

            elif self.config["security"] == "secure_compat":
                self.execute(['cp', f'{mount_point}/usr/share/shim-signed/shimx64.efi', f'{mount_point}/efi/EFI/secux/shimx64.efi'])
                self.execute(['cp', f'{mount_point}/usr/share/shim-signed/mmx64.efi', f'{mount_point}/efi/EFI/secux/mmx64.efi'])
                self.execute(['mkdir', '-p', f'{mount_point}/etc/secureboot'])
                self.execute(['openssl', 'req', '-newkey', 'rsa:4096', '-nodes', '-keyout', f'{mount_point}/etc/secureboot/sb.key', '-new', '-x509', '-sha256', '-days', '3650', '-subj', '/CN=Secux Linux MOK/', '-out', f'{mount_point}/etc/secureboot/sb.crt'])
                self.execute(['openssl', 'x509', '-outform', 'DER', '-in', f'{mount_point}/etc/secureboot/sb.crt', '-out', f'{mount_point}/etc/secureboot/sb.cer'])
                self.execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', '/efi/EFI/systemd/systemd-bootx64.efi', '/usr/lib/systemd/boot/efi/systemd-bootx64.efi'])
                for kernel in self.config['kernels']:
                    self.execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', f'/efi/EFI/secux/secux-{kernel}.efi', f'/efi/EFI/secux/secux-{kernel}.efi'])
                    self.execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', f'/efi/EFI/secux/secux-{kernel}-fallback.efi', f'/efi/EFI/secux/secux-{kernel}-fallback.efi'])

                # TODO: MOK page on encryption page
                mok_input = f"{self.config['MOK']}\n{self.config['MOK']}\n"
                self.execute(['arch-chroot', mount_point, 'mokutil', '--import', '/etc/secureboot/sb.cer'], input_str=mok_input)

                self.execute(['cp', f'{installer_path}/scripts/92-shim-signed.hook', f'{mount_point}/usr/share/libalpm/hooks/'])
                self.execute(['cp', f'{installer_path}/scripts/shim-copy.sh', f'{mount_point}/usr/share/'])
                self.execute(['chmod', '+x', f'{mount_point}/usr/share/shim-copy.sh'])
                self.execute(['cp', f'{installer_path}/scripts/91-systemd-boot.hook', f'{mount_point}/usr/share/libalpm/hooks/'])
                self.execute(['cp', f'{installer_path}/scripts/systemd-boot-sign.sh', f'{mount_point}/usr/share'])
                self.execute(['chmod', '+x', f'{mount_point}/usr/share/systemd-boot-sign.sh'])
                self.execute(['cp', f'{installer_path}/scripts/sign-uki.sh', f'{mount_point}/usr/lib/initcpio/post/'])
                self.execute(['chmod', '+x', f'{mount_point}/usr/lib/initcpio/post/sign-uki.sh'])

                self.execute(['cp', f'{mount_point}/efi/EFI/systemd/systemd-bootx64.efi', f'{mount_point}/efi/EFI/secux/grubx64.efi'])

                efi_base_drive, efi_number_str = self.__split_device(efi_partition)
                efi_part_num = ''.join(filter(str.isdigit, efi_number_str))
                if efi_base_drive and efi_part_num:
                    self.execute(['efibootmgr', '--create', '--disk', efi_base_drive, '--part', efi_part_num, '--label', "Secux Linux shim", '--loader', '\\EFI\\secux\\shimx64.efi'])

            self.set_progress(0.95)

            # Hardening
            self.execute(['cp', f'{installer_path}/scripts/hardening.conf', f'{mount_point}/etc/sysctl.d/'])
            self.execute(['arch-chroot', mount_point, 'ufw', 'default', 'deny'])
            self.execute(['sed', '-i', 's/ENABLED=no/ENABLED=yes/', f"{mount_point}/etc/ufw/ufw.conf"])
            # self.execute(['arch-chroot', mount_point, 'ufw', 'enable'])
            self.execute(['cp', f'{installer_path}/scripts/secux.rules', f'{mount_point}/etc/audit/rules.d/secux.rules'])

            # Flatpak offline installation support
            self.execute(['arch-chroot', mount_point, 'flatpak', 'remote-modify', '--collection-id=org.flathub.Stable', 'flathub'])

            # === ФИНАЛ ===
            self.set_progress(1.0)
            self.log("INFO: Установка успешно завершена!")
            
            # Обновляем UI по завершении
            GLib.idle_add(self._on_install_finished, True)

        except Exception as e:
            self.log(f"CRITICAL ERROR: {e}")
            import traceback
            self.log(traceback.format_exc())
            GLib.idle_add(self._on_install_finished, False)

    def an_error_occurred(self):
        GLib.idle_add(self._on_install_finished, False)

    def _on_install_finished(self, success):
        self.spinner.stop()
        self.spinner.set_visible(False)
        self.btn_finish.set_visible(True)
        
        if success:
            self.status_page.set_title(_("Установка завершена"))
            self.status_page.set_description(_("Система готова к работе. Извлеките установочный носитель."))
            self.status_page.set_icon_name("object-select-symbolic")
        else:
            self.status_page.set_title(_("Ошибка установки"))
            self.status_page.set_description(_("Произошла критическая ошибка. Смотрите логи ниже."))
            self.status_page.set_icon_name("dialog-error-symbolic")
            self.btn_finish.set_label("Закрыть")


@Gtk.Template(filename=get_ui_path("summary.ui"))
class SummaryPage(Adw.NavigationPage):
    __gtype_name__ = "SummaryPage"

    source_stack = Gtk.Template.Child()
    security_stack = Gtk.Template.Child()
    desktop_stack = Gtk.Template.Child()
    disk_mode_stack = Gtk.Template.Child()
    disk_conf = Gtk.Template.Child() 
    swap_stack = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()
    encryption_label = Gtk.Template.Child()
    user_label = Gtk.Template.Child()
    hostname_label = Gtk.Template.Child()
    disk_auto_label = Gtk.Template.Child()
    swap_yes_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def populate_data(self, win):        
        source_mode = win.source_page.get_source_mode() 
        self.source_stack.set_visible_child_name(source_mode)

        sec_mode = win.security_page.get_selected_mode()
        self.security_stack.set_visible_child_name(sec_mode)

        de_mode = win.desktop_page.get_selected_de()
        self.desktop_stack.set_visible_child_name(de_mode)

        tz = win.timezone_page.get_timezone()
        self.timezone_label.set_label(tz)

        disk_config = win.partition_page.get_config()
        
        if disk_config['mode'] == 'auto':
            self.disk_mode_stack.set_visible_child_name("auto")
            
            self.disk_conf.set_visible_child_name("disk_auto")
            self.disk_auto_label.set_label(disk_config.get('target', 'Error'))
        else:
            self.disk_mode_stack.set_visible_child_name("manual")
            self.disk_conf.set_visible_child_name("disk_manual")

        swap_size = disk_config.get('swap_size', 0)
        
        if swap_size > 0:
            self.swap_stack.set_visible_child_name("swap_yes")
            self.swap_yes_label.set_label(f"{swap_size} GiB")
        else:
            self.swap_stack.set_visible_child_name("swap_no")

        user_data = win.user_page.get_user()
        full_user_str = f"{user_data.get('fullname', '')} ({user_data.get('username', '')})"
        self.user_label.set_label(full_user_str)
        
        self.hostname_label.set_label(user_data.get('hostname', 'localhost'))


@Gtk.Template(filename=get_ui_path("software.ui"))
class SoftwarePage(Adw.NavigationPage):
    __gtype_name__ = "SoftwarePage"
    
    chk_sec_manager = Gtk.Template.Child()
    chk_chromium = Gtk.Template.Child()
    chk_firefox = Gtk.Template.Child()
    chk_vlc = Gtk.Template.Child()
    chk_libreoffice = Gtk.Template.Child()
    chk_keepassxc = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_selected_packages(self):
        packages = []
        
        # Secux
        if self.chk_sec_manager.get_active():
            # TODO: create secux-security-manager package in kolbanidze repo
            # packages.append("secux-security-manager")
            pass
            
        # Pacman
        if self.chk_chromium.get_active():
            packages.append("chromium")
        if self.chk_firefox.get_active():
            packages.append("firefox")
        if self.chk_vlc.get_active():
            packages.append("vlc")
            packages.append("vlc-plugin-ffmpeg")
        if self.chk_libreoffice.get_active():
            packages.append("libreoffice-fresh")
        if self.chk_keepassxc.get_active():
            packages.append("keepassxc")
            
        return packages


@Gtk.Template(filename=get_ui_path("source.ui"))
class SourcePage(Adw.NavigationPage):
    __gtype_name__ = "SourcePage"
    
    btn_online = Gtk.Template.Child()
    btn_offline = Gtk.Template.Child()
    status_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_image_status()

    def check_is_netinstall(self):
        if os.path.isfile(os.path.join(BASE_DIR, "offline_installation.conf")):
            return False
        else:
            return True

    def update_image_status(self):
        is_netinstall = self.check_is_netinstall()
        
        if is_netinstall:
            self.status_stack.set_visible_child_name("online")
            self.btn_online.set_active(True)
            self.btn_offline.set_sensitive(False)
        else:
            self.status_stack.set_visible_child_name("offline")
            self.btn_online.set_active(True)

    def get_source_mode(self):
        if self.btn_online.get_active():
            return "online"
        return "offline"


@Gtk.Template(filename=get_ui_path("user.ui"))
class UserPage(Adw.NavigationPage):
    __gtype_name__ = "UserPage"
    
    entry_fullname = Gtk.Template.Child()
    entry_hostname = Gtk.Template.Child()
    entry_username = Gtk.Template.Child()
    entry_password = Gtk.Template.Child()
    entry_confirm = Gtk.Template.Child()
    error_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_actions()
        
        entries = [
            self.entry_fullname, self.entry_hostname, 
            self.entry_username, self.entry_password, self.entry_confirm
        ]
        
        for entry in entries:
            entry.connect("notify::text", self.on_text_changed)

    def setup_actions(self):
        action_group = Gio.SimpleActionGroup()
        self.insert_action_group("user", action_group)
        
        action = Gio.SimpleAction.new("validate", None)
        action.connect("activate", self.on_validate_and_next)
        action_group.add_action(action)

    def on_text_changed(self, *args):
        if self.error_stack.get_visible_child_name() != "none":
            self.error_stack.set_visible_child_name("none")

    def on_validate_and_next(self, action, param):
        fullname = self.entry_fullname.get_text().strip()
        hostname = self.entry_hostname.get_text().strip()
        username = self.entry_username.get_text().strip()
        pwd = self.entry_password.get_text()
        confirm = self.entry_confirm.get_text()

        if not all([fullname, hostname, username, pwd, confirm]):
            self.error_stack.set_visible_child_name("empty")
            return

        if not hostname.isascii() or hostname[0].isdigit():
            self.error_stack.set_visible_child_name("ascii_host")
            return
            
        if not username.isascii() or username[0].isdigit():
            self.error_stack.set_visible_child_name("ascii_user")
            return

        if not pwd.isascii():
            self.error_stack.set_visible_child_name("ascii_pwd")
            return

        if " " in username:
            self.error_stack.set_visible_child_name("space_user")
            return
            
        if " " in hostname:
             self.error_stack.set_visible_child_name("space_host")
             return

        if pwd != confirm:
            self.error_stack.set_visible_child_name("mismatch")
            return
        
        win = self.get_native()
        if win:
            win.activate_action("win.next_step", None)
    
    def get_user(self):
        fullname = self.entry_fullname.get_text().strip()
        hostname = self.entry_hostname.get_text().strip()
        username = self.entry_username.get_text().strip()
        pwd = self.entry_password.get_text()

        return {"fullname": fullname,
                "hostname": hostname,
                "username": username,
                "password": pwd}

@Gtk.Template(filename=get_ui_path("encryption.ui"))
class EncryptionPage(Adw.NavigationPage):
    __gtype_name__ = "EncryptionPage"
    
    password_entry = Gtk.Template.Child()
    confirm_entry = Gtk.Template.Child()
    error_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_actions()
        
        self.password_entry.connect("notify::text", self.on_text_changed)
        self.confirm_entry.connect("notify::text", self.on_text_changed)

    def setup_actions(self):
        action_group = Gio.SimpleActionGroup()
        self.insert_action_group("encryption", action_group)
        
        action = Gio.SimpleAction.new("validate", None)
        action.connect("activate", self.on_validate_and_next)
        action_group.add_action(action)

    def on_text_changed(self, *args):
        if self.error_stack.get_visible_child_name() != "none":
            self.error_stack.set_visible_child_name("none")

    def show_error(self, message):
        self.error_label.set_label(message)
        self.error_label.set_visible(True)

    def on_validate_and_next(self, action, param):
        pwd = self.password_entry.get_text()
        confirm = self.confirm_entry.get_text()

        if not pwd:
            self.error_stack.set_visible_child_name("empty")
            return

        if pwd != confirm:
            self.error_stack.set_visible_child_name("mismatch")
            return

        if not pwd.isascii():
            self.error_stack.set_visible_child_name("ascii")
            return
        
        win = self.get_native()
        if win:
            win.activate_action("win.next_step", None)


    def get_password(self):
        return self.password_entry.get_text()


@Gtk.Template(filename=get_ui_path("partition.ui"))
class PartitionPage(Adw.NavigationPage):
    __gtype_name__ = "PartitionPage"
    
    btn_auto = Gtk.Template.Child()
    btn_manual = Gtk.Template.Child()
    content_stack = Gtk.Template.Child()
    
    disk_combo_auto = Gtk.Template.Child()
    
    btn_gnome_disks = Gtk.Template.Child()
    btn_refresh = Gtk.Template.Child()
    combo_efi = Gtk.Template.Child()
    combo_root = Gtk.Template.Child()
    
    switch_swap = Gtk.Template.Child()
    row_swap_size = Gtk.Template.Child()
    scale_swap = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.btn_auto.connect("toggled", self.on_mode_toggled)
        self.btn_manual.connect("toggled", self.on_mode_toggled)
        
        self.scale_swap.connect("value-changed", self.on_swap_changed)
        
        # Если выключен свич -> ползунок недоступен
        self.switch_swap.bind_property(
            "active", 
            self.row_swap_size, 
            "sensitive", 
            GObject.BindingFlags.DEFAULT
        )

        self.btn_refresh.connect("clicked", self.populate_disks)
        
        self.setup_page_actions()
        
        self.populate_disks(None)

    def setup_page_actions(self):
        action_group = Gio.SimpleActionGroup()
        self.insert_action_group("partition", action_group)
        
        action_gnome_disks = Gio.SimpleAction.new("open_gnome_disks", None)
        action_gnome_disks.connect("activate", self.on_open_disks)
        action_group.add_action(action_gnome_disks)

    def on_mode_toggled(self, widget):
        if self.btn_auto.get_active():
            self.content_stack.set_visible_child_name("page_auto")
        else:
            self.content_stack.set_visible_child_name("page_manual")

    def on_swap_changed(self, scale):
        value = int(scale.get_value())
        self.row_swap_size.set_subtitle(f"{value} GiB")

    def on_open_disks(self, action, param):
        subprocess.Popen(["gnome-disks"])
        
    def populate_disks(self, widget):
        disks_list = Gtk.StringList()
        partitions_list = Gtk.StringList()

        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            disks_list.append(f"/dev/{disk['name']} ({disk['size']})")
            if 'children' in disk:
                for partition in disk['children']:
                    partitions_list.append(f"/dev/{partition['name']} ({partition['size']}, {partition.get('fstype', 'N/A')})")

        self.disk_combo_auto.set_model(disks_list)
        self.combo_efi.set_model(partitions_list)
        self.combo_root.set_model(partitions_list)
        
    def get_config(self):
        """Сбор данных для установки"""
        if self.btn_auto.get_active():
            model = self.disk_combo_auto.get_model()
            idx = self.disk_combo_auto.get_selected()
            disk = model.get_string(idx) if model else None
            disk = disk.split(' ')[0]

            swap_size = int(self.scale_swap.get_value())

            return {"mode": "auto", "target": disk, 'swap_size': swap_size}
        else:
            model = self.combo_efi.get_model()
            idx = self.combo_efi.get_selected()
            efi_part = model.get_string(idx) if model else None
            efi_part = efi_part.split(' ')[0]

            model = self.combo_root.get_model()
            idx = self.combo_root.get_selected()
            root_part = model.get_string(idx) if model else None
            root_part = root_part.split(' ')[0]

            swap_enabled = self.switch_swap.get_active()
            swap_size = int(self.scale_swap.get_value()) if swap_enabled else 0

            return {
                "mode": "manual",
                "efi_part": efi_part,
                "root_part": root_part,
                "swap_size": swap_size,
            }


@Gtk.Template(filename=get_ui_path("kernel.ui"))
class KernelPage(Adw.NavigationPage):
    __gtype_name__ = "KernelPage"
    
    # Получаем доступ к кнопкам
    btn_hardened = Gtk.Template.Child()
    btn_lts = Gtk.Template.Child()
    btn_linux = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_selected_kernels(self) -> list:
        kernels = []
        if self.btn_hardened.get_active():
            kernels.append("linux-hardened")
        if self.btn_lts.get_active():
            kernels.append("linux-lts")
        if self.btn_linux.get_active():
            kernels.append("linux")
        return kernels



@Gtk.Template(filename=get_ui_path("desktop.ui"))
class DesktopPage(Adw.NavigationPage):
    __gtype_name__ = "DesktopPage"
    
    btn_gnome = Gtk.Template.Child()
    btn_kde = Gtk.Template.Child()
    btn_console = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_selected_de(self) -> str:
        """Возвращает идентификатор выбранного окружения"""
        if self.btn_gnome.get_active():
            return "gnome"
        elif self.btn_kde.get_active():
            return "kde"
        else:
            return "console"


@Gtk.Template(filename=get_ui_path("security.ui"))
class SecurityPage(Adw.NavigationPage):
    __gtype_name__ = "SecurityPage"
    
    btn_secure = Gtk.Template.Child()
    btn_compat = Gtk.Template.Child()
    btn_none = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_selected_mode(self) -> str:
        if self.btn_secure.get_active():
            return "secure_full"
        elif self.btn_compat.get_active():
            return "secure_compat"
        else:
            return "insecure"


@Gtk.Template(filename=get_ui_path("selection.ui"))
class SelectionPage(Adw.NavigationPage):
    __gtype_name__ = "SelectionPage"
    
    search_entry = Gtk.Template.Child()
    list_view = Gtk.Template.Child()

    def __init__(self, items, callback, **kwargs):
        super().__init__(**kwargs)
        self.items = sorted(items)
        self.callback = callback
        
        # Подключаем поиск
        self.search_entry.connect("search-changed", self.on_search_changed)
        
        # Заполняем список
        self.populate_list()

    def populate_list(self):
        for item_name in self.items:
            row = Adw.ActionRow(title=item_name)
            row.set_activatable(True)
            
            # Добавляем стрелочку паприколу
            icon = Gtk.Image.new_from_icon_name("go-next-symbolic")
            row.add_suffix(icon)
            
            # Обработка клика
            row.connect("activated", self.on_item_clicked, item_name)
            self.list_view.append(row)

    def on_item_clicked(self, row, item_name):
        if self.callback:
            self.callback(item_name)

    def on_search_changed(self, entry):
        text = entry.get_text().lower()
        
        # Фильтрация строк
        child = self.list_view.get_first_child()
        while child:
            if isinstance(child, Adw.ActionRow):
                # Если текст пустой или содержится в названии - показываем
                visible = not text or text in child.get_title().lower()
                child.set_visible(visible)
            child = child.get_next_sibling()

@Gtk.Template(filename=get_ui_path("timezone.ui"))
class TimezonePage(Adw.NavigationPage):
    __gtype_name__ = "TimezonePage"
    
    timezone_row = Gtk.Template.Child()
    current_time_row = Gtk.Template.Child()
    auto_sync_row = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.selected_tz_id = "Europe/Minsk"
        
        GLib.timeout_add_seconds(1, self.update_realtime_clock)
        
        self.timezone_row.connect("activated", self.open_region_selector)
        
        self.auto_sync_row.connect("notify::active", self.on_auto_sync_toggled)
        
        if self.auto_sync_row.get_active():
            self.start_auto_detection()
        else:
            self.update_ui_labels()

    def update_realtime_clock(self):
        """Вызывается каждую секунду системой GLib"""
        try:
            tz = GLib.TimeZone.new_identifier(self.selected_tz_id)
            if not tz:
                tz = GLib.TimeZone.new_utc()

            now = GLib.DateTime.new_now(tz)
            
            time_str = now.format("%H:%M")
            self.current_time_row.set_subtitle(time_str)
            
        except Exception:
            self.current_time_row.set_subtitle("--:--")
            
        return True 

    def on_auto_sync_toggled(self, widget, pspec):
        """Обработчик переключения свича"""
        is_active = widget.get_active()
        
        if is_active:
            self.start_auto_detection()
        else:
            self.timezone_row.set_sensitive(True)
            self.timezone_row.set_subtitle(self.selected_tz_id)

    def start_auto_detection(self):
        """Настройка UI и запуск потока определения"""
        self.timezone_row.set_sensitive(False)
        
        thread = threading.Thread(target=self._fetch_timezone_thread)
        thread.daemon = True
        thread.start()

    def _fetch_timezone_thread(self):
        detected_tz = None
        
        try:
            url = "https://ipwho.is/"
            with urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if data.get("success") is True:
                    detected_tz = data.get("timezone", {}).get("id")
        except Exception as e:
            print(f"Ошибка определения часового пояса: {e}")

        GLib.idle_add(self._on_detection_complete, detected_tz)

    def _on_detection_complete(self, detected_tz):
        """Вызывается в главном потоке после завершения запроса"""
        # Проверяем, не выключил ли юзер свич, пока шел запрос
        if not self.auto_sync_row.get_active():
            return

        if detected_tz:
            self.selected_tz_id = detected_tz
            self.timezone_row.set_subtitle(detected_tz)
        else:
            self.timezone_row.set_subtitle("Ошибка определения. Выберите вручную.")
            self.auto_sync_row.set_active(False)
            self.timezone_row.set_sensitive(True)

    def open_region_selector(self, widget):
        regions = list(TIMEZONES.keys())
        page = SelectionPage(
            items=regions,
            callback=self.on_region_selected
        )
        self.get_nav_view().push(page)
 
        
    def on_region_selected(self, region_name):
        """Шаг 2: Регион выбран -> Открываем список городов"""
        self.selected_region = region_name
        
        cities = TIMEZONES.get(region_name, [])
        page = SelectionPage(
            items=cities,
            callback=self.on_city_selected
        )
        self.get_nav_view().push(page)

    def on_city_selected(self, city_name):
        """Шаг 3: Город выбран -> Обновляем и закрываем"""
        self.selected_city = city_name
        self.update_label()
        self.update_info()

        self.get_nav_view().pop_to_page(self)

    def update_info(self):
        tz_name = f"{self.selected_region}/{self.selected_city}"
        self.selected_tz_id = tz_name
        self.timezone_row.set_subtitle(tz_name)
        

    def update_label(self):
        self.timezone_row.set_subtitle(f"{self.selected_region}/{self.selected_city}")

    def get_timezone(self) -> str:
        return self.selected_tz_id

    def get_nav_view(self):
        """Находит родительский NavigationView"""
        return self.get_ancestor(Adw.NavigationView)

    def update_ui_labels(self):
        self.timezone_row.set_subtitle(self.selected_tz_id)

class LanguageManager:
    """Класс для управления сменой языка"""
    
    # Карта: Индекс в DropDown -> Код локали
    LANG_MAP = {
        0: "ru_RU.UTF-8",
        1: "en_US.UTF-8"
    }

    @staticmethod
    def set_language(index):
        new_lang = LanguageManager.LANG_MAP.get(index, "en_US.UTF-8")
        
        # Если язык уже такой, ничего не делаем
        current = os.environ.get("LANG")
        if current and new_lang in current:
            return

        print(f"Switching language to {new_lang}...")
        
        os.environ["LANG"] = new_lang
        
        python = sys.executable
        os.execl(python, python, *sys.argv)


@Gtk.Template(filename=get_ui_path("welcome.ui"))
class WelcomePage(Adw.NavigationPage):
    __gtype_name__ = "WelcomePage"
    language_dropdown = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        current_lang = os.environ.get("LANG", "en_US.UTF-8")
        if "ru" in current_lang.lower():
            initial_index = 0
        else:
            initial_index = 1
        self.language_dropdown.set_selected(initial_index)

        self.set_version(VERSION)
        self.language_dropdown.connect("notify::selected", self.on_language_changed)
    
    def set_version(self, version):
        text = f"Secux Linux Installer {version}"
        self.status_page.set_description(text)
    
    def on_language_changed(self, widget, pspec):
        idx = widget.get_selected()
        LanguageManager.set_language(idx)



@Gtk.Template(filename=get_ui_path("window.ui"))
class InstallerWindow(Adw.ApplicationWindow):
    __gtype_name__ = "InstallerWindow"
    nav_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.welcome_page = WelcomePage()
        self.timezone_page = TimezonePage()
        self.security_page = SecurityPage()
        self.desktop_page = DesktopPage()
        self.kernel_page = KernelPage()
        self.partition_page = PartitionPage()
        self.encryption_page = EncryptionPage()
        self.user_page = UserPage()
        self.source_page = SourcePage()
        self.software_page = SoftwarePage()
        self.summary_page = SummaryPage()
        self.install_page = InstallPage()
        
        self.steps = [self.welcome_page, self.timezone_page, self.security_page, self.desktop_page, self.kernel_page,
                      self.partition_page, self.encryption_page, self.user_page, self.source_page, self.software_page,
                      self.summary_page, self.install_page]
        self.current_step_index = 0

        self.nav_view.push(self.steps[0])
        self.setup_actions()
        self.nav_view.connect("popped", self.on_page_popped)

    def setup_actions(self):
        action = Gio.SimpleAction.new("next_step", None)
        action.connect("activate", self.on_next_step)
        self.add_action(action)

    def on_next_step(self, action, param):
        next_index = self.current_step_index + 1
        if next_index < len(self.steps):
            page_to_open = self.steps[next_index]
            
            if isinstance(page_to_open, SummaryPage):
                page_to_open.populate_data(self)
            
            if isinstance(page_to_open, InstallPage):
                page_to_open.start_installation(self)

            self.current_step_index = next_index
            self.nav_view.push(page_to_open)
        else:
            self.close()

    def on_page_popped(self, nav_view, page):
        if page in self.steps:
            if self.current_step_index > 0:
                self.current_step_index -= 1

class SecuxLinuxInstaller(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.secux.installer",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = InstallerWindow(application=self)
        win.present()

if __name__ == "__main__":
    init_i18n()
    load_resources()
    print(_("Текущий язык: русский"))
    app = SecuxLinuxInstaller()
    app.run(sys.argv)
