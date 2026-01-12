pkgname=secux-installer
pkgver=0.3.1
pkgrel=1
pkgdesc="Secux Linux Installer"
arch=('x86_64')
url="https://github.com/kolbanidze/secux-installer"
license=('MIT')
depends=(python3 python-gobject gtk4 libadwaita)
makedepends=()
source=("secux-installer.tar.gz")
sha256sums=('3bdfdd72ebcadda9ad41afd7b5c05ef88d8dca6fe3e4b38517ccc2e5014ef810')

package() {
  mkdir -p "$pkgdir/usr/local/bin/"
  mkdir -p "$pkgdir/etc/xdg/autostart"

  cp -a "$srcdir/secux-installer" "$pkgdir/usr/local/bin/"

  install -Dm644 "$srcdir/secux-installer/icons/org.secux.installer.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/org.secux.installer.svg"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/etc/xdg/autostart/secux-installer.desktop"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/usr/share/applications/secux-installer.desktop"
}
