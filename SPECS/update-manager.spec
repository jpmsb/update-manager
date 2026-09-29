Name:           update-manager
Version:        %{?_version}%{!?_version:0}
Release:        1%{?dist}
Summary:        System update viewer with tray notifications
License:        GPL-3.0-or-later
Source0:        %{name}-%{version}.tar.gz
Requires:       bash
Requires:       curl
Requires:       python3
Requires:       python313-PyQt6
Requires:       python313-dbus-python
Requires:       PackageKit
BuildRequires:  gettext-tools
BuildArch:      noarch

%description
Desktop update viewer for openSUSE-based systems. Includes a systemd timer
that checks for available updates, a PyQt6 tray application, and a privileged
system upgrade helper that can self-update this package from GitHub Releases.

%prep
%setup -q

%build
for po in locale/*/LC_MESSAGES/update-viewer.po; do
  [ -f "$po" ] || continue
  msgfmt -o "${po%.po}.mo" "$po"
done

%install
rm -rf %{buildroot}
install -d %{buildroot}/usr/bin
install -d %{buildroot}/usr/lib/systemd/system
install -d %{buildroot}/etc/xdg/autostart
install -d %{buildroot}/usr/share/locale

install -m 0755 usr/bin/update-viewer %{buildroot}/usr/bin/update-viewer
install -m 0755 usr/bin/update-checker %{buildroot}/usr/bin/update-checker
install -m 0755 usr/bin/update-system %{buildroot}/usr/bin/update-system
ln -s update-system %{buildroot}/usr/bin/atualizar-sistema

install -m 0644 usr/lib/systemd/system/update-checker.service \
  %{buildroot}/usr/lib/systemd/system/update-checker.service
install -m 0644 usr/lib/systemd/system/update-checker.timer \
  %{buildroot}/usr/lib/systemd/system/update-checker.timer
install -m 0644 etc/xdg/autostart/update-viewer.desktop \
  %{buildroot}/etc/xdg/autostart/update-viewer.desktop

for mo in locale/*/LC_MESSAGES/update-viewer.mo; do
  [ -f "$mo" ] || continue
  lang=$(basename "$(dirname "$(dirname "$mo")")")
  install -d %{buildroot}/usr/share/locale/$lang/LC_MESSAGES
  install -m 0644 "$mo" %{buildroot}/usr/share/locale/$lang/LC_MESSAGES/update-viewer.mo
done

%post
if [ -x /usr/bin/systemctl ]; then
  systemctl daemon-reload >/dev/null 2>&1 || :
  systemctl enable --now update-checker.timer >/dev/null 2>&1 || :
fi

%postun
if [ "$1" -eq 0 ] && [ -x /usr/bin/systemctl ]; then
  systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
/usr/bin/update-viewer
/usr/bin/update-checker
/usr/bin/update-system
/usr/bin/atualizar-sistema
/usr/lib/systemd/system/update-checker.service
/usr/lib/systemd/system/update-checker.timer
/etc/xdg/autostart/update-viewer.desktop
/usr/share/locale/*/LC_MESSAGES/update-viewer.mo

%changelog
* Sun Sep 27 2026 Joao Pedro <jpmsb@users.noreply.github.com> - 0-1
- Initial GitHub packaging with dated releases and self-update
