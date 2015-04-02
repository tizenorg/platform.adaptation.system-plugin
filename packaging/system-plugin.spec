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

Requires(post): systemd

%description
This package provides target specific system configuration files.

%package u3
Summary:  U3/XU3 specific system configuration files
Requires: %{name} = %{version}-%{release}

%description u3
This package provides U3/XU3 specific system configuration files.

%package exynos
Summary:  Exynos specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-u3 = %{version}-%{release}

%description exynos
This package provides Exynos specific system configuration files.

%prep
%setup -q

%build
cp %{SOURCE1} .

%install
# Copy whole fs files to buildroot
cp -rf fs/* %{buildroot}

mkdir -p %{buildroot}%{_unitdir}
install -m 644 units/resize2fs@.service %{buildroot}%{_unitdir}

# Resize partition for 3-parted target
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-system\\x2ddata.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-user.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-rootfs.service

%post
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/resize2fs@.service

%files u3
%manifest %{name}.manifest
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service

%files exynos
%manifest %{name}.manifest
%{_libdir}/udev/rules.d/51-system-plugin-exynos.rules
