# secux-installer

[![Russian](https://img.shields.io/badge/README-на_русском-red.svg)](README.ru.md)

This repository contains the source code of the Secux Linux graphical installer.

<p align="center">
    <img src="https://raw.githubusercontent.com/kolbanidze/secux-installer/refs/heads/main/welcome.png" width=384>
</p>

## Launch

The application launches automatically in the Secux Linux ISO image.

For a manual package update, use: `sudo pacman -Sy secux-installer`

For launching in a development or testing environment:
`python main.py`

### Technical Information
* The interface is written in Python using GTK 4 and Libadwaita.
* Interaction with the disk and the system is carried out through `subprocess` as root. For root access, `sudo` is used
* Dependencies:
    * `python-gobject`
    * `libadwaita`
    * `gtk4`

## Installation Stages

* Interface language
* Time zone
* Security level
    * Maximum security: only custom Secure Boot keys
    * Security with backward compatibility: trust in Microsoft, use of shim
    * No security((
* Desktop environment
    * GNOME
    * KDE
    * Console (for servers)
* Linux kernel
    * Linux hardened
    * Linux LTS
    * Linux
* Disk partitioning
* LUKS password selection
* Administrator user creation
* Installation source selection
    * Online
    * Offline
* Pre-installed software selection
* System installation