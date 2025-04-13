#!/bin/bash

# Not required anymore. Secux Linux Builder downloads python packages automatically.
# Scheduled for removal.

if [ -z "$1" ]; then
    echo "Usage: $0 <output_dir>"
    exit 1
fi

output_dir="$1"

/usr/bin/mkdir -p "$output_dir"

/usr/bin/pip download customtkinter face_recognition face_recognition_models -d "$output_dir"
