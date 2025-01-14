import os

def check_secure_boot_and_setup_mode():
    secure_boot_path = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
    setup_mode_path = "/sys/firmware/efi/efivars/SetupMode-8be4df61-93ca-11d2-aa0d-00e098032b8c"

    def read_efi_var(path):
        try:
            with open(path, "rb") as f:
                # EFI variable data starts after the first 4 bytes of metadata
                return ord(f.read()[4:5])  # Convert byte to int
        except FileNotFoundError:
            return None

    secure_boot = read_efi_var(secure_boot_path)
    setup_mode = read_efi_var(setup_mode_path)

    if secure_boot is None or setup_mode is None:
        print("Secure Boot or Setup Mode variables not found. Is the system EFI-enabled?")
        return (False, 0, 0)

    return (True, secure_boot, setup_mode)

if __name__ == "__main__":
    check_secure_boot_and_setup_mode()
