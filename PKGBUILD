pkgname=secux-installer
pkgver=0.6.2
pkgrel=1
pkgdesc="Secux Linux Installer"
arch=('x86_64')
url="https://github.com/kolbanidze/secux-installer"
license=('MIT')
depends=(python3 python-gobject gtk4 libadwaita)
makedepends=()
source=("secux-installer.tar.gz")
sha256sums=('a9fcd45dfb13a68017358a35d02ed9918d88ecc9c5e165023dac93d2c587092d')

package() {
  mkdir -p "$pkgdir/usr/local/bin/"
  mkdir -p "$pkgdir/etc/xdg/autostart"

  cp -a "$srcdir/secux-installer" "$pkgdir/usr/local/bin/"

  install -Dm644 "$srcdir/secux-installer/icons/org.secux.installer.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/org.secux.installer.svg"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/etc/xdg/autostart/secux-installer.desktop"
  install -Dm644 "$srcdir/secux-installer/scripts/secux-installer.desktop" "$pkgdir/usr/share/applications/secux-installer.desktop"
}
