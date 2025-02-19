from subprocess import run

PACKAGES = "base linux linux-lts linux-hardened linux-headers linux-lts-headers linux-hardened-headers linux-firmware amd-ucode intel-ucode vim nano efibootmgr sudo plymouth python-pip python-dbus v4l-utils lvm2 networkmanager systemd-ukify sbsigntools efitools less git ntfs-3g gvfs gvfs-mtp xdg-user-dirs fwupd sbctl shim-signed mokutil networkmanager-openvpn gnome-tweaks gdm vlc firefox chromium tk python-pexpect python-pillow"

PACKAGES += " baobab epiphany evince gdm gnome-backgrounds gnome-calculator gnome-calendar gnome-characters gnome-clocks gnome-color-manager gnome-connections gnome-console gnome-contacts gnome-control-center gnome-disk-utility gnome-font-viewer gnome-keyring gnome-logs gnome-maps gnome-menus gnome-music gnome-remote-desktop gnome-session gnome-settings-daemon gnome-shell gnome-shell-extensions gnome-software gnome-system-monitor gnome-text-editor gnome-tour gnome-user-docs gnome-user-share gnome-weather grilo-plugins gvfs gvfs-afc gvfs-dnssd gvfs-goa gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs gvfs-onedrive gvfs-smb gvfs-wsdd loupe malcontent nautilus orca rygel simple-scan snapshot sushi tecla totem xdg-desktop-portal-gnome xdg-user-dirs-gtk yelp bluedevil breeze breeze-gtk breeze-plymouth discover drkonqi flatpak-kcm kactivitymanagerd kde-cli-tools kde-gtk-config kdecoration kdeplasma-addons kgamma kglobalacceld kinfocenter kmenuedit kpipewire krdp kscreen kscreenlocker ksshaskpass ksystemstats kwallet-pam kwayland kwin kwrited layer-shell-qt libkscreen libksysguard libplasma milou ocean-sound-theme oxygen oxygen-sounds plasma-activities plasma-activities-stats plasma-browser-integration plasma-desktop plasma-disks plasma-firewall plasma-integration plasma-nm plasma-pa plasma-sdk plasma-systemmonitor plasma-thunderbolt plasma-vault plasma-welcome plasma-workspace plasma-workspace-wallpapers plasma5support plymouth-kcm polkit-kde-agent powerdevil print-manager qqc2-breeze-style sddm-kcm systemsettings wacomtablet xdg-desktop-portal-kde xf86-video-vesa xorg-bdftopcf xorg-docs xorg-font-util xorg-fonts-100dpi xorg-fonts-75dpi xorg-fonts-encodings xorg-iceauth xorg-mkfontscale xorg-server xorg-server-common xorg-server-devel xorg-server-xephyr xorg-server-xnest xorg-server-xvfb xorg-sessreg xorg-setxkbmap xorg-smproxy xorg-x11perf xorg-xauth xorg-xbacklight xorg-xcmsdb xorg-xcursorgen xorg-xdpyinfo xorg-xdriinfo xorg-xev xorg-xgamma xorg-xhost xorg-xinput xorg-xkbcomp xorg-xkbevd xorg-xkbutils xorg-xkill xorg-xlsatoms xorg-xlsclients xorg-xmodmap xorg-xpr xorg-xprop xorg-xrandr xorg-xrdb xorg-xrefresh xorg-xset xorg-xsetroot xorg-xvinfo xorg-xwayland xorg-xwd xorg-xwininfo xorg-xwud"

PACKAGES += " vte4 base-devel cmake python-opencv python-numpy keepassxc libreoffice apparmor ufw "

deps = []

for i in PACKAGES.split(" "):
    process = run(f"pactree -u \"{i}\"", shell=True, capture_output=True)
    a = process.stdout.decode().split("\n")
    deps.append(a)

deps2=[]
for i in deps:
    for j in i:
        if len(j) != 0:
            deps2.append(j)

deps2 = list(set(deps2))

for i in range(len(deps2)):
    if "<" in deps2[i]: 
        deps2[i] = deps2[i].split("<")[0]
        continue
    if ">" in deps2[i]:
        deps2[i] = deps2[i].split(">")[0]
        continue
    if "=" in deps2[i]:
        deps2[i] = deps2[i].split("=")[0]

print(" ".join(deps2))