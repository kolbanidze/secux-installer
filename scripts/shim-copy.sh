#!/bin/bash
set -e
TARGET_DIR="/efi/EFI/secux"
SOURCE_DIR="/usr/share/shim-signed"

[ -d "$TARGET_DIR" ] || mkdir -p "$TARGET_DIR"

for file in shimx64.efi mmx64.efi; do
    if [ -f "${SOURCE_DIR}/${file}" ]; then
        cp -fv "${SOURCE_DIR}/${file}" "${TARGET_DIR}/${file}"
        echo "${file} was copied to ${TARGET_DIR}"
    else
        echo "File ${SOURCE_DIR}/${file} not found!"
        exit 1
    fi
done
