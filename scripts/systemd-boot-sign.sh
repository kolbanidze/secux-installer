#!/bin/bash
set -e

SYSTEMD_BOOT_SRC="/usr/lib/systemd/boot/efi/systemd-bootx64.efi"
TARGET_DIR="/efi/EFI/Linux"
TARGET_FILE="${TARGET_DIR}/grubx64.efi"
KEY="/etc/secureboot/sb.key"
CERT="/etc/secureboot/sb.crt"
TEMP_SIGNED="/tmp/systemd-bootx64.efi.signed"

if [ ! -f "$SYSTEMD_BOOT_SRC" ]; then
    echo "systemd-boot wasn't found at ${SYSTEMD_BOOT_SRC}"
    exit 1
fi

[ -d "$TARGET_DIR" ] || mkdir -p "$TARGET_DIR"

sbsign --key "$KEY" --cert "$CERT" --output "$TEMP_SIGNED" "$SYSTEMD_BOOT_SRC"

if [ -f "$TEMP_SIGNED" ]; then
    cp -fv "$TEMP_SIGNED" "$TARGET_FILE"
    rm -f "$TEMP_SIGNED"
    echo "systemd-boot signed and copied to ${TARGET_FILE}"
else
    echo "An error occured while signing systemd-boot"
    exit 1
fi
