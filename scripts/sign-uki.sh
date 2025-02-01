#!/usr/bin/bash

KERNEL_FILE="$1"
UKI_FILE="$3"
KEY="/etc/secureboot/sb.key"
CERT="/etc/secureboot/sb.crt"

IMAGE_FILE="$KERNEL_FILE"
if [ -n "$KERNELDESTINATION" ] && [ -f "$KERNELDESTINATION" ]; then
    IMAGE_FILE="$KERNELDESTINATION"
fi
if [ -n "$UKI_FILE" ]; then
    IMAGE_FILE="$UKI_FILE"
fi

if [ -z "$IMAGE_FILE" ]; then
    echo "No kernel or UKI found for signing"
    exit 0
fi

echo "Signing $IMAGE_FILE"
sbsign --key "$KEY" --cert "$CERT" --output "$IMAGE_FILE" "$IMAGE_FILE"