from subprocess import run

# Hint:
#   pacman -Sg metapackage | awk '{print $2}' | paste -sd ' '

# OS, Apps and dependencies
PACKAGES = "base base-devel linux linux-lts linux-hardened linux-headers linux-lts-headers linux-hardened-headers linux-firmware amd-ucode intel-ucode vim nano efibootmgr sudo plymouth python-pip python-dbus v4l-utils lvm2 networkmanager systemd-ukify sbsigntools efitools less git ntfs-3g gvfs gvfs-mtp xdg-user-dirs fwupd sbctl shim-signed mokutil networkmanager-openvpn gnome-tweaks"

PACKAGES += " vlc firefox chromium libreoffice keepassxc"

PACKAGES += " tk python-pexpect python-pillow python-opencv python-numpy python-darkdetect python-packaging python-setuptools python-dotenv python-dlib"

# GNOME
PACKAGES += " baobab epiphany evince gdm gnome-backgrounds gnome-calculator gnome-calendar gnome-characters gnome-clocks gnome-color-manager gnome-connections gnome-console gnome-contacts gnome-control-center gnome-disk-utility gnome-font-viewer gnome-keyring gnome-logs gnome-maps gnome-menus gnome-music gnome-remote-desktop gnome-session gnome-settings-daemon gnome-shell gnome-shell-extensions gnome-software gnome-system-monitor gnome-text-editor gnome-tour gnome-user-docs gnome-user-share gnome-weather grilo-plugins gvfs gvfs-afc gvfs-dnssd gvfs-goa gvfs-google gvfs-gphoto2 gvfs-mtp gvfs-nfs gvfs-onedrive gvfs-smb gvfs-wsdd loupe malcontent nautilus orca rygel simple-scan snapshot sushi tecla totem xdg-desktop-portal-gnome xdg-user-dirs-gtk yelp"

# KDE
PACKAGES += " bluedevil breeze breeze-gtk breeze-plymouth discover drkonqi flatpak-kcm kactivitymanagerd kde-cli-tools kde-gtk-config kdecoration kdeplasma-addons kgamma kglobalacceld kinfocenter kmenuedit kpipewire krdp kscreen kscreenlocker ksshaskpass ksystemstats kwallet-pam kwayland kwin kwrited layer-shell-qt libkscreen libksysguard libplasma milou ocean-sound-theme oxygen oxygen-sounds plasma-activities plasma-activities-stats plasma-browser-integration plasma-desktop plasma-disks plasma-firewall plasma-integration plasma-nm plasma-pa plasma-sdk plasma-systemmonitor plasma-thunderbolt plasma-vault plasma-welcome plasma-workspace plasma-workspace-wallpapers plasma5support plymouth-kcm polkit-kde-agent powerdevil print-manager qqc2-breeze-style sddm-kcm spectacle systemsettings wacomtablet xdg-desktop-portal-kde"

PACKAGES += " accessibility-inspector akonadi-calendar-tools akonadi-import-wizard akonadiconsole akregator alligator angelfish arianna ark artikulate audex audiocd-kio audiotube blinken bomber bovo calligra cantor cervisia colord-kde dolphin dolphin-plugins dragon elisa falkon ffmpegthumbs filelight francis ghostwriter granatier grantlee-editor gwenview isoimagewriter itinerary juk k3b kaddressbook kajongg kalarm kalgebra kalk kalm kalzium kamera kamoso kanagram kapman kapptemplate kasts kate katomic kbackup kblackbox kblocks kbounce kbreakout kbruch kcachegrind kcalc kcharselect kclock kcolorchooser kcron kde-dev-scripts kde-dev-utils kde-inotify-survey kdebugsettings kdeconnect kdegraphics-thumbnailers kdenetwork-filesharing kdenlive kdepim-addons kdesdk-kio kdesdk-thumbnailers kdevelop kdevelop-php kdevelop-python kdf kdialog kdiamond keditbookmarks keysmith kfind kfourinline kgeography kget kgoldrunner kgpg kgraphviewer khangman khelpcenter kig kigo killbots kimagemapeditor kio-admin kio-extras kio-gdrive kio-zeroconf kirigami-gallery kiriki kiten kjournald kjumpingcube kleopatra klettres klickety klines kmag kmahjongg kmail kmail-account-wizard kmines kmix kmousetool kmouth kmplot knavalbattle knetwalk knights koko kolf kollision kolourpaint kompare kongress konqueror konquest konsole kontact kontrast konversation korganizer kpat krdc krecorder kreversi krfb kruler kshisen ksirk ksnakeduel kspaceduel ksquares ksudoku ksystemlog kteatime ktimer ktorrent ktouch ktrip ktuberling kturtle kubrick kwalletmanager kwave kweather kwordquiz lokalize lskat marble markdownpart massif-visualizer mbox-importer merkuro minuet neochat okular palapeli parley partitionmanager picmi pim-data-exporter pim-sieve-editor plasmatube poxml rocs signon-kwallet-extension skanlite skanpage skladnik step svgpart sweeper telly-skout tokodon umbrello yakuake zanshin"

# Xorg
PACKAGES += " xf86-video-vesa xorg-bdftopcf xorg-docs xorg-font-util xorg-fonts-100dpi xorg-fonts-75dpi xorg-fonts-encodings xorg-iceauth xorg-mkfontscale xorg-server xorg-server-common xorg-server-devel xorg-server-xephyr xorg-server-xnest xorg-server-xvfb xorg-sessreg xorg-setxkbmap xorg-smproxy xorg-x11perf xorg-xauth xorg-xbacklight xorg-xcmsdb xorg-xcursorgen xorg-xdpyinfo xorg-xdriinfo xorg-xev xorg-xgamma xorg-xhost xorg-xinput xorg-xkbcomp xorg-xkbevd xorg-xkbutils xorg-xkill xorg-xlsatoms xorg-xlsclients xorg-xmodmap xorg-xpr xorg-xprop xorg-xrandr xorg-xrdb xorg-xrefresh xorg-xset xorg-xsetroot xorg-xvinfo xorg-xwayland xorg-xwd xorg-xwininfo xorg-xwud"

PACKAGES += " vte4 apparmor ufw "

# Getting all dependencies
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

deps2.extend(["xorg", "gnome", "plasma"])

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
