#!/usr/bin/sh

# run this script after cloning the repository
# and setting up the Python virtual environment
# to generate additional necessary resources

# convert PyQt5 `.ui` files to Python code
cd src/main/python/ayab
pyuic5 firmware_flash_ui.ui -o firmware_flash_ui.py
pyuic5 main_gui.ui -o main_gui.py
pyuic5 menu_gui.ui -o menu_gui.py
pyuic5 mirrors.ui -o mirrors.py
pyuic5 prefs_gui.ui -o prefs_gui.py
pyuic5 engine/dock_gui.ui -o engine/dock_gui.py
pyuic5 engine/options_gui.ui -o engine/options_gui.py
pyuic5 engine/status_gui.ui -o engine/status_gui.py
cd -

# generate translation files
cd src/main/resources/base/ayab/translation
./ayab_trans.pl
cd -
