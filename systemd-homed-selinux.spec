# vim: sw=4:ts=4:et
# General maintainer notes:
#   Fedora guideliens for packaging of SELinux rules:
#     https://fedoraproject.org/wiki/SELinux/IndependentPolicy
#   RHEL instructions regarding Troubleshooting problems related to SELinux:
#     https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/troubleshooting-problems-related-to-selinux_using-selinu

# defining macros needed by SELinux
%global selinuxtype targeted
%global modulename systemd-homed

Name:		systemd-homed-selinux
Version:	0.3.0
Release:	1%{?dist}
Summary:	SELinux policy module for systemd-homed

Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/richiedaze/homed-selinux
Source0:	systemd-homed.if
Source1:	systemd-homed.te
Source2:	systemd-homed.fc
Source3:	Makefile


Requires: selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildArch:	noarch
BuildRequires:	make
BuildRequires:	selinux-policy-devel
%{?selinux_requires}

%description
This package installs and sets up the SELinux policy security module for systemd-homed.

%build
make

%clean
make clean

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
# install policy modules
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
install -D -p -m 0644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license LICENSE

%changelog
* Tue May 14 2024 Joakim Nohlgård <joakim@nohlgard.se> 0.3.0-1
- Initial version
