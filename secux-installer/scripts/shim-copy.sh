#!/bin/bash
set -eo pipefail
TARGET_DIR="/efi/EFI/secux"
SOURCE_DIR="/usr/share/shim-signed"

mountpoint /efi
mkdir -p "$TARGET_DIR"
staging_dir=$(mktemp -d "$TARGET_DIR/.shim.XXXXXX")
trap 'rm -rf -- "$staging_dir"' EXIT

cp "$SOURCE_DIR/shimx64.efi" "$SOURCE_DIR/mmx64.efi" "$staging_dir/"
# Shim reads the first field of options.csv as a UTF-16LE EFI path.
printf '%s\n' '\EFI\systemd\systemd-bootx64.efi,' |
    iconv -f UTF-8 -t UTF-16LE > "$staging_dir/options.csv"
mv -fv -- "$staging_dir/mmx64.efi" "$staging_dir/shimx64.efi" "$staging_dir/options.csv" "$TARGET_DIR/"
