%define debug_package %{nil}

Name:      system-plugin
Summary:   Target specific system configuration files
Version:   0.1
Release:   1
Group:     System/Configuration
BuildArch: noarch
License:   Apache-2.0
Source0:   %{name}-%{version}.tar.bz2
Source1:   %{name}.manifest

Requires(post): /usr/bin/systemctl

%description
This package provides target specific system configuration files.

%package u3
Summary:  U3/XU3 specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-exynos = %{version}-%{release}

%description u3
This package provides U3/XU3 specific system configuration files.

%package n4
Summary:  Note4 specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-exynos = %{version}-%{release}

%description n4
This package provides Note4 specific system configuration files.

%package exynos
Summary:  Exynos specific system configuration files
Requires: %{name} = %{version}-%{release}

%description exynos
This package provides Exynos specific system configuration files.

%package spreadtrum
Summary:  Spreadtrum specific system configuration files
Requires: %{name} = %{version}-%{release}

%description spreadtrum
This package provides Spreadtrum specific system configuration files.

%package circle
Summary:  Circle specific system configuration files
Requires: %{name} = %{version}-%{release}

%description circle
This package provides Circle specific system configuration files.

%prep
%setup -q

%build
cp %{SOURCE1} .

%install
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/csa
mkdir -p %{buildroot}/initrd
install -m 644 units/resize2fs@.service %{buildroot}%{_unitdir}
install -m 644 units/tizen-system-env.service %{buildroot}%{_unitdir}

# csa mount
install -m 644 units/csa.mount %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
ln -s ../csa.mount %{buildroot}%{_unitdir}/local-fs.target.wants/csa.mount

# Resize partition for 3-parted target
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-system\\x2ddata.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-user.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-rootfs.service
# ugly temporary patch for initrd wearable
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dpartlabel-user.service

ln -s ../tizen-system-env.service %{buildroot}%{_unitdir}/basic.target.wants/tizen-system-env.service

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-exynos.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-spreadtrum.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# fstab
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab %{buildroot}%{_sysconfdir}
# ugly temporary patch for initrd wearable
install -m 644 etc/fstab_initrd %{buildroot}%{_sysconfdir}

%post
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/resize2fs@.service
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service

%files u3
%manifest %{name}.manifest
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab

%files n4
%manifest %{name}.manifest
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab

%files exynos
%manifest %{name}.manifest
%{_prefix}/lib/udev/rules.d/51-system-plugin-exynos.rules

%files circle
%manifest %{name}.manifest
/initrd
%{_sysconfdir}/fstab_initrd
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-user.service

# ugly temporary patch for initrd wearable
%post circle
rm %{_sysconfdir}/fstab
mv %{_sysconfdir}/fstab_initrd %{_sysconfdir}/fstab

%files spreadtrum
%manifest %{name}.manifest
/initrd
/csa
%{_prefix}/lib/udev/rules.d/51-system-plugin-spreadtrum.rules
%{_unitdir}/tizen-system-env.service
%{_sysconfdir}/fstab
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
