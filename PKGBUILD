pkgname=secux-installer
pkgver=0.6.9
pkgrel=2
pkgdesc="Secux Linux Installer"
arch=('x86_64')
url="https://github.com/kolbanidze/secux-installer"
license=('MIT')
depends=(python3 python-gobject gtk4 libadwaita)
makedepends=()
source=("secux-installer.tar.gz")
sha256sums=('6e56044dee2e61720548191c702fafc0f512404eb1f3a6b61426c6ad05db42cb')

package() {
  mkdir -p "$pkgdir/usr/local/bin/"
  mkdir -p "$pkgdir/etc/xdg/autostart"

  cp -a "$srcdir/secux-installer" "$pkgdir/usr/local/bin/"

  install -Dm644 "$srcdir/secux-installer/icons/org.secux.installer.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/org.secux.installer.svg"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/etc/xdg/autostart/secux-installer.desktop"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/usr/share/applications/secux-installer.desktop"
}
