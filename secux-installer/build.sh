#!/bin/bash

mkdir -p ui

for file in blueprint/*.blp; do
    name=$(basename "$file" .blp)
    
    echo "Compiling $name.blp -> ui/$name.ui"
    
    blueprint-compiler compile "$file" --output "ui/$name.ui"
done

echo "Compiling resources.xml -> resources.gresource"
glib-compile-resources resources.xml --target=resources.gresource

echo "Done."