%define kernel_version %(uname -r)
%define module_dir updates
%global debug_package %{nil}

Summary: Driver for Realtek r8152
Name: kmod-r8152
Version: 2.20.1
Release: 1
License: GPL
Source: r8152-%{version}.tar.bz2

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod


%description
Realtek r8152 device drivers for the Linux Kernel version %{kernel_version}.

%prep
%autosetup -n r8152-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
mkdir -p %{buildroot}/etc/udev/rules.d
%{__make} RULEDIR=%{buildroot}/etc/udev/rules.d install_rules

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}

%postun
/sbin/depmod %{kernel_version}

%files
/lib/modules/%{kernel_version}/*/*.ko
/etc/udev/rules.d/50-usb-realtek-net.rules

%changelog
* Sun, 08 Jun 2025 Deokgyu Yang <secugyu@gmail.com> - 2.20.1
- Update Realtek r8152 driver to 2.20.1
- Enable compiling for intended kernel versions

* Tue Nov 12 2024 Andrew Lindh <andrew@netplex.net> - 2.19.2-1
- Vendor driver r8152-2.19.2
- Remove useless dire kernel warning about Private IOCTL
- Disable TX CSUM and TSO by default as it causes problems with XCP

* Thu Sep 28 2023 Andrew Lindh <andrew@netplex.net> - 2.17.1-1
- Vendor driver r8152-2.17.1
