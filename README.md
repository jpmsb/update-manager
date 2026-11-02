# Update Manager

System update viewer and manager for openSUSE Tumbleweed.

Ships a tray application, a systemd timer that checks for available updates, and an upgrade helper that can **self-update** this package from GitHub Releases.

## Package contents

| File | Role |
|------|------|
| `/usr/bin/update-viewer` | Main application, featuring a GUI and a tray |
| `/usr/bin/update-checker` | Root job used by the timer that checks for updates |
| `/usr/bin/update-system` | Script that performs the system upgrade |
| `/usr/lib/systemd/system/update-checker.{service,timer}` | Systemd unit and timer files |
| `/etc/xdg/autostart/update-viewer.desktop` | Autostart entry |

## Local packaging

To build the package locally you need `rpm-build` and `gettext-tools`.

```bash
VERSION="$(date -u +%Y.%m.%d.%H%M)"
scripts/build-source-tarball.sh "$VERSION"
mkdir -p ~/rpmbuild/SOURCES
cp "update-manager-${VERSION}.tar.gz" ~/rpmbuild/SOURCES/
rpmbuild --define "_version ${VERSION}" -ba SPECS/update-manager.spec
```

## Self-update

When `update-system` runs, it queries `https://api.github.com/repos/jpmsb/update-manager/releases/latest` and installs a newer RPM if available, then continues with `zypper dist-upgrade`.

Network or install failures are non-fatal for the system upgrade.

## License

GPL-3.0-or-later
