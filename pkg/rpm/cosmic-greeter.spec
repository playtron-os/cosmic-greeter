Name:           cosmic-greeter
Epoch:          1
Version:        1.0.7
Release:        1%{?dist}
Summary:        COSMIC Greeter - Login manager for COSMIC desktop (Playtron fork)

License:        GPL-3.0-only
URL:            https://github.com/pop-os/cosmic-greeter
Source0:        %{name}-%{_arch}.tar.gz

Requires:       greetd
Requires:       greetd-selinux
Requires:       dbus
Requires:       fprintd-pam
Requires:       pam
Requires:       systemd

# Override the upstream cosmic-greeter
Provides:       cosmic-greeter = %{epoch}:%{version}-%{release}
Obsoletes:      cosmic-greeter < %{epoch}:%{version}

%description
Login greeter for the COSMIC desktop environment.
Provides a graphical login interface using greetd as the backend.
Includes the cosmic-greeter UI and cosmic-greeter-daemon.

%prep
%autosetup -n %{name} -p1

%build

%install
# Binaries
install -Dm0755 "usr/bin/cosmic-greeter" "%{buildroot}%{_bindir}/cosmic-greeter"
install -Dm0755 "usr/bin/cosmic-greeter-daemon" "%{buildroot}%{_bindir}/cosmic-greeter-daemon"
install -Dm0755 "usr/bin/cosmic-greeter-start" "%{buildroot}%{_bindir}/cosmic-greeter-start"

# D-Bus configuration
install -Dm0644 "usr/share/dbus-1/system.d/com.system76.CosmicGreeter.conf" "%{buildroot}%{_datadir}/dbus-1/system.d/com.system76.CosmicGreeter.conf"

# Systemd services
install -Dm0644 "usr/lib/systemd/system/cosmic-greeter.service" "%{buildroot}%{_prefix}/lib/systemd/system/cosmic-greeter.service"
install -Dm0644 "usr/lib/systemd/system/cosmic-greeter-daemon.service" "%{buildroot}%{_prefix}/lib/systemd/system/cosmic-greeter-daemon.service"

# sysusers.d - creates cosmic-greeter user
install -Dm0644 "usr/lib/sysusers.d/cosmic-greeter.conf" "%{buildroot}%{_prefix}/lib/sysusers.d/cosmic-greeter.conf"

# tmpfiles.d - creates /var/lib/cosmic-greeter and /run/cosmic-greeter
install -Dm0644 "usr/lib/tmpfiles.d/cosmic-greeter.conf" "%{buildroot}%{_prefix}/lib/tmpfiles.d/cosmic-greeter.conf"

# PAM configuration (use Fedora-compatible version, not Debian's @include style)
install -Dm0644 "etc/pam.d/cosmic-greeter" "%{buildroot}%{_sysconfdir}/pam.d/cosmic-greeter"

# greetd configuration
install -Dm0644 "etc/greetd/cosmic-greeter.toml" "%{buildroot}%{_sysconfdir}/greetd/cosmic-greeter.toml"

# Default background
install -Dm0644 "usr/share/backgrounds/cosmic/cosmic-greeter-background.jpg" "%{buildroot}%{_datadir}/backgrounds/cosmic/cosmic-greeter-background.jpg"

# License
install -Dm0644 "usr/share/licenses/cosmic-greeter/LICENSE" "%{buildroot}%{_datadir}/licenses/cosmic-greeter/LICENSE"

%post
%sysusers_create_package cosmic-greeter %{_sysusersdir}/cosmic-greeter.conf
%tmpfiles_create_package cosmic-greeter %{_tmpfilesdir}/cosmic-greeter.conf
%systemd_post cosmic-greeter.service
%systemd_post cosmic-greeter-daemon.service

%preun
%systemd_preun cosmic-greeter.service
%systemd_preun cosmic-greeter-daemon.service

%postun
%systemd_postun_with_restart cosmic-greeter-daemon.service

%files
%license %{_datadir}/licenses/cosmic-greeter/LICENSE
%{_bindir}/cosmic-greeter
%{_bindir}/cosmic-greeter-daemon
%{_bindir}/cosmic-greeter-start
%{_datadir}/dbus-1/system.d/com.system76.CosmicGreeter.conf
%{_prefix}/lib/systemd/system/cosmic-greeter.service
%{_prefix}/lib/systemd/system/cosmic-greeter-daemon.service
%{_prefix}/lib/sysusers.d/cosmic-greeter.conf
%{_prefix}/lib/tmpfiles.d/cosmic-greeter.conf
%config %{_sysconfdir}/pam.d/cosmic-greeter
%config(noreplace) %{_sysconfdir}/greetd/cosmic-greeter.toml
%{_datadir}/backgrounds/cosmic/cosmic-greeter-background.jpg

%changelog
* Tue Feb 03 2026 Playtron <dev@playtron.one> - 1.0.7-1
- Initial RPM package for Playtron fork

