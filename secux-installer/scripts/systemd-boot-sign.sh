#!/bin/bash
set -e

SYSTEMD_BOOT_SRC="/usr/lib/systemd/boot/efi/systemd-bootx64.efi"
SIGNED_FILE="${SYSTEMD_BOOT_SRC}.signed"
KEY="/etc/secureboot/sb.key"
CERT="/etc/secureboot/sb.crt"

TEMP_SIGNED=$(mktemp "${SIGNED_FILE}.XXXXXX")
trap 'rm -f -- "$TEMP_SIGNED"' EXIT
sbsign --key "$KEY" --cert "$CERT" --output "$TEMP_SIGNED" "$SYSTEMD_BOOT_SRC"
mv -f -- "$TEMP_SIGNED" "$SIGNED_FILE"

if [[ ${1:-} == --update ]]; then
    mountpoint /efi
    bootctl --esp-path=/efi --variables=no --graceful update
    sbverify --cert "$CERT" /efi/EFI/systemd/systemd-bootx64.efi
fi
