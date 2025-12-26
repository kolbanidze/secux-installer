#!/bin/bash

DOMAIN="secux-installer"
LOCALE_DIR="locales"

echo "1. Updating UI files..."
for file in blueprint/*.blp; do
    blueprint-compiler compile "$file" --output "ui/$(basename "$file" .blp).ui"
done

echo "2. Extracting strings..."
xgettext -k_ -L Python --from-code=UTF-8 -o $DOMAIN.pot main.py
xgettext -L Glade -j -o $DOMAIN.pot ui/*.ui

echo "3. Updating PO files..."
# msginit -l ru -o $LOCALE_DIR/ru/LC_MESSAGES/$DOMAIN.po -i $DOMAIN.pot --no-translator
# msginit -l en -o $LOCALE_DIR/en/LC_MESSAGES/$DOMAIN.po -i $DOMAIN.pot --no-translator

# Если файлы уже есть, обновляем их новыми строками из шаблона
msgmerge -U $LOCALE_DIR/ru/LC_MESSAGES/$DOMAIN.po $DOMAIN.pot
msgmerge -U $LOCALE_DIR/en/LC_MESSAGES/$DOMAIN.po $DOMAIN.pot

echo "Done. Now edit .po files and run compile_translations.sh"