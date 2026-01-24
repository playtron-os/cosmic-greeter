Name:           cosmic-greeter
Epoch:          1
Version:        %{getenv:COSMIC_GREETER_VERSION}
Release:        1%{?dist}
Summary:        COSMIC Greeter - Login manager for COSMIC desktop (Playtron fork)

License:        GPL-3.0-only
URL:            https://github.com/pop-os/cosmic-greeter

# No BuildRequires - binary is pre-built

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
%build

%install
# COSMIC_GREETER_SOURCE is set by the build script

# Binaries
install -Dm0755 "%{getenv:COSMIC_GREETER_SOURCE}/target/release/cosmic-greeter" "%{buildroot}%{_bindir}/cosmic-greeter"
install -Dm0755 "%{getenv:COSMIC_GREETER_SOURCE}/target/release/cosmic-greeter-daemon" "%{buildroot}%{_bindir}/cosmic-greeter-daemon"
install -Dm0755 "%{getenv:COSMIC_GREETER_SOURCE}/cosmic-greeter-start.sh" "%{buildroot}%{_bindir}/cosmic-greeter-start"

# D-Bus configuration
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/dbus/com.system76.CosmicGreeter.conf" "%{buildroot}%{_datadir}/dbus-1/system.d/com.system76.CosmicGreeter.conf"

# Systemd services
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/debian/cosmic-greeter.service" "%{buildroot}%{_unitdir}/cosmic-greeter.service"
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/debian/cosmic-greeter-daemon.service" "%{buildroot}%{_unitdir}/cosmic-greeter-daemon.service"

# sysusers.d - creates cosmic-greeter user
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/debian/cosmic-greeter.sysusers" "%{buildroot}%{_sysusersdir}/cosmic-greeter.conf"

# tmpfiles.d - creates /var/lib/cosmic-greeter and /run/cosmic-greeter
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/debian/cosmic-greeter.tmpfiles" "%{buildroot}%{_tmpfilesdir}/cosmic-greeter.conf"

# PAM configuration (use Fedora-compatible version, not Debian's @include style)
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/packaging/rpm/cosmic-greeter.pam" "%{buildroot}%{_sysconfdir}/pam.d/cosmic-greeter"

# greetd configuration
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/cosmic-greeter.toml" "%{buildroot}%{_sysconfdir}/greetd/cosmic-greeter.toml"

# Default background
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/res/background.jpg" "%{buildroot}%{_datadir}/backgrounds/cosmic/cosmic-greeter-background.jpg"

# License
install -Dm0644 "%{getenv:COSMIC_GREETER_SOURCE}/LICENSE" "%{buildroot}%{_datadir}/licenses/cosmic-greeter/LICENSE"

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
%{_unitdir}/cosmic-greeter.service
%{_unitdir}/cosmic-greeter-daemon.service
%{_sysusersdir}/cosmic-greeter.conf
%{_tmpfilesdir}/cosmic-greeter.conf
%config %{_sysconfdir}/pam.d/cosmic-greeter
%config(noreplace) %{_sysconfdir}/greetd/cosmic-greeter.toml
%{_datadir}/backgrounds/cosmic/cosmic-greeter-background.jpg

%changelog
* Wed Jan 21 2026 Playtron <dev@playtron.one> - 1.0.2-1
- Initial RPM package for Playtron fork

