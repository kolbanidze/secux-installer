#!/bin/bash

rm -f secux-installer.tar.gz
rm -f *.tar.zst
rm -f *.tar.zst.sig
rm -rf pkg src

tar --exclude='.git' \
    --exclude='secux-installer.tar.gz' \
    --exclude='pkg' \
    --exclude='src' \
    -czvf secux-installer.tar.gz secux-installer/
updpkgsums

makepkg -f --sign