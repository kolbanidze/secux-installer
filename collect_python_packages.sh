#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <output_dir>"
    exit 1
fi

output_dir="$1"

mkdir -p "$output_dir"

pip download customtkinter face_recognition face_recognition_models -d "$output_dir"
