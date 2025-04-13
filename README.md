# 🛡️ Secux Linux Installer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Russian](https://img.shields.io/badge/README-in_Russian-red.svg)](README.ru.md)


Welcome to the installer for **Secux Linux**, a security-focused distribution based on the robust and flexible Arch Linux! 🐧🔒

This installer is designed to set up Secux Linux with a strong security posture right from the start, leveraging modern security technologies.

## ✨ Key Features

*   **✨ User-Friendly GUI:** Built with `customtkinter` for a clean and modern installation experience.
*   **🔒 Secure Installation Process:** Guides you through setting up a hardened Secux Linux system.
*   **🔑 Secure Boot Support:**
    *   Uses **custom keys** enrolled via `sbctl` if your system is in **Setup Mode** (most secure). ✅
    *   Falls back to **shim** if Secure Boot is enabled but not in Setup Mode, requiring a Machine Owner Key (MOK) enrollment on first boot. 🆗
*   **🧱 Unified Kernel Images (UKI):** Bundles the kernel, initrd, microcode, command line, and OS release info into a single, signed EFI executable (`systemd-ukify`). This enhances boot integrity.
*   **✍️ PCR Policy Signing:** Signs the UKI against specific TPM Platform Configuration Register (PCR) values, ensuring the boot components haven't been tampered with.
*   **🔐 Full Disk Encryption:** Uses LUKS on LVM to protect your data at rest.
*   **🛡️ Base for TPM Integration:**
    *   Allows unlocking the encrypted drive using the TPM via the [**Security Manager**](https://github.com/kolbanidze/secux-apps). 🔓
    *   The Security Manager verifies the boot process integrity (PCR measurements) before allowing the unlock.
*   **⚙️ Based on Arch Linux:** Benefit from a rolling-release model, extensive documentation (Arch Wiki), and the Arch User Repository (AUR).
*   **🔧 Customizable:** Choose your Desktop Environment (GNOME, KDE, or Console), Kernel(s) (`linux-hardened`, `lts`, `stable`), and additional applications.
*   **💾 Flexible Partitioning:** Offers both automatic (erase disk) and manual partitioning options.
*   **🌐 Online/Offline Modes:** Can install using packages from the internet or from a local repository (offline build, [Secux Linux Builder](https://github.com/kolbanidze/secux-iso).

## 🛡️ Security Features Deep Dive

Secux Linux aims to provide a secure computing environment by default. The installer implements several key security measures:

1.  **Bootloader (`systemd-boot`) & UKI:** Instead of a traditional bootloader chain, we use `systemd-boot` which directly loads signed Unified Kernel Images. UKIs bundle essential boot components, making the boot process less susceptible to modification.
2.  **Secure Boot:**
    *   **Goal:** Ensure only trusted code (signed bootloader, kernel) runs during boot.
    *   **Implementation:**
        *   If UEFI is in **Setup Mode**: You can secure your own secure boot keys. The installer generates custom Secure Boot keys (`sbctl`), enrolls them into the firmware, and signs all EFI binaries (bootloader, UKIs) with these keys. This gives you full control over boot trust.
        *   If UEFI has Secure Boot **Enabled (User Mode)** with Microsoft keys: The installer can use the `shim` bootloader (signed by Microsoft), which allows booting custom-signed binaries after enrolling a Machine Owner Key (MOK). The installer signs the UKIs and `systemd-boot` with a generated key and prompts you to enroll this key's certificate using `mokutil` (requires a password set during installation, entered during the *next* boot).
3.  **TPM & Boot Integrity Verification:**
    *   The Trusted Platform Module (TPM) is used for:
        *   **Measurements:** Firmware and boot components measure themselves and store these measurements in Platform Configuration Registers (PCRs).
        *   **Sealing:** The LUKS disk encryption key can be sealed to the TPM, tied to specific PCR values.
    *   [**Security Manager**](https://github.com/kolbanidze/secux-apps): This separate application (installable via the installer) allows you to configure TPM-based disk unlocking. This verifies the integrity of the entire boot chain.
4.  **PCR Policy Signing:** The UKI itself is generated with embedded signatures based on expected PCR values for the initrd phase (`ukify` + `PCRSignature:initrd`). This provides an additional layer of integrity checking early in the boot process.
5.  **Disk Encryption:** Standard LUKS full-disk encryption (on LVM) protects data confidentiality if the physical drive is compromised.
6.  **System Hardening:** Includes AppArmor profiles, basic UFW firewall rules, auditd rules, and security-focused kernel parameters (`sysctl.conf`).

## 🚀 Installation Process

The installer guides you through the following stages:

1.  👋 **Welcome:** Language selection, UI scaling, theme.
2.  🌍 **Timezone:** Select your region and time zone.
3.  🛡️ **Installation Type:** Choose Secure, Less Secure (shim), or Insecure (no SB handling).
4.  🖼️ **Desktop Environment:** Select GNOME, KDE, or Console (no GUI).
5.  🐧 **Kernel Selection:** Choose one or more kernels (`linux-hardened`, `linux-lts`, `linux`).
6.  💾 **Partitioning:**
    *   **Automatic:** Erase a selected disk and create EFI + LUKS/LVM partitions.
    *   **Manual:** Choose existing partitions for EFI and the root filesystem (which will be formatted for LUKS/LVM). Option to create a swapfile.
7.  🔑 **Encryption:** Set the password for the LUKS encrypted volume.
8.  👤 **Admin User:** Create your primary user account and password.
9.  🌐 **Network:** Choose Online or Offline package source (Offline requires `offline_installation.conf` to be present).
10. 📦 **Applications:** Select additional applications to install (Secux tools, browsers, office suite, etc.).
11. ✅ **Confirmation:** Review all settings before starting.
12. ⏳ **Installation:** Formatting, package installation, configuration, UKI generation, signing, etc.

## ✅ Requirements

*   **UEFI Firmware:** BIOS/Legacy boot is **not supported**.
*   **Secure Boot Capable System:** Required for Secure Boot features.
    *   **Setup Mode:** Required for the most secure (custom key) installation type.
*   **TPM 2.0 Chip:** Required for TPM-based disk unlocking via the Security Manager.
*   **64-bit CPU** (x86_64)
*   **RAM:** Minimum 2GB (4GB+ recommended).
*   **Disk Space:** Minimum 15-20GB (depends on selected DE and applications).
*   **Internet Connection:** Required for the Online installation mode.
*   **Installation Medium:** A USB drive flashed with the Secux Linux ISO.

## 🛠️ Usage

1.  Download the latest Secux Linux ISO image.
2.  Create a bootable USB drive using a tool like Ventoy, Rufus, or `dd`.
3.  Boot your computer from the USB drive (ensure UEFI mode is selected in your firmware settings).
4.  The graphical installer should launch automatically.
5.  Follow the on-screen instructions.

## 🔐 Secux Security Manager

For TPM-based disk unlocking (highly recommended), you need to install and configure the **Security Manager** after installation.
*   **Repository:** [kolbanidze/secux-apps](https://github.com/kolbanidze/secux-apps)
*   Automatically selected for installation during the "Applications" stage of this installer.

---

#### ℹ️ Includes integration for [KIRTapp](https://github.com/KIRT-king/test_app) (developed by my [partner](https://github.com/KIRT-king)), although it's not installed by default in the Secux Linux for various reasons.

---

## 🤝 Contributing

Contributions are welcome! If you find bugs or have suggestions, please open an issue on the GitHub repository. Pull requests are also appreciated.

## 📜 License

This project is licensed under the **MIT License**. See the LICENSE file for details.
