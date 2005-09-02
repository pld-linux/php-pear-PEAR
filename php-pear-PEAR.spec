%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		beta
%define		_pearname	%{_class}

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.0
%define		_pre b1
Release:	0.%{_pre}.2
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}%{_pre}.tgz
# Source0-md5:	fac6e8d80991ae3a63cb6a616958e833
Patch0:		%{name}-memory.patch
URL:		http://pear.php.net/package/PEAR/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	sed >= 4.0.0
Requires:	php-pear
Requires:	php-cli
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend-CLI
Obsoletes:	php-pear-PEAR-OS
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PEAR package contains:
- the PEAR installer, for creating, distributing and installing
  packages
- the alpha-quality PEAR_Exception PHP5 error handling mechanism
- the beta-quality PEAR_ErrorStack advanced error handling mechanism
- the PEAR_Error error handling mechanism
- the OS_Guess class for retrieving info about the OS where PHP is
  running on
- the System class for quick handling of common operations with files
  and directories
- the PEAR base class packages

In PEAR status of this package is: %{_status}.

%description -l pl
Pakiet PEAR zawiara:
- PEAR installer do tworzenia, dystrybucji i instalowania pakietów,
- mechanizm PEAR_Exception (w fazie alpha) do obs³ugi b³êdów PHP5,
- zaawansowany mechanizm PEAR_ErrorStack (w fazie beta) do obs³ugi
  b³êdów,
- mechanizm obs³ugi b³êdów PEAR_Error,
- klasê OS_Guess do pozyskiwania informacji na temat systemu
  operacyjnego,
- klasê System do szybkiej obs³ugi typowych operacji na plikach i
  katalogach,
- podstawow± klasy PEAR.

Ta klasa ma w PEAR status: %{_status}.

%prep
%setup -q -c -n %{name}-%{version}%{_pre}
%patch0 -p2

%build
# put proper paths
sed -i -e 's,@php_dir@,%{php_pear_dir},g' -e 's,@php_bin@,%{_bindir}/php,g' %{_pearname}-%{version}%{_pre}/scripts/*
# fix include path
sed -i -e 's,PEAR/PackageFile/Generator/v2/rw.php,PEAR/PackageFile/v2/rw.php,g' %{_pearname}-%{version}%{_pre}/PEAR/PackageFile/v2.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_pear_dir}/{%{_class}/{ChannelFile,Command,Downloader,Frontend,Installer/Role,PackageFile/{Generator,Parser,v2},Task,Validator},OS},%{_bindir}}

install %{_pearname}-%{version}%{_pre}/*.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}%{_pre}/*.dtd $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}%{_pre}/OS/*.php $RPM_BUILD_ROOT%{php_pear_dir}/OS
install %{_pearname}-%{version}%{_pre}/%{_class}/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}
install %{_pearname}-%{version}%{_pre}/%{_class}/ChannelFile/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/ChannelFile
install %{_pearname}-%{version}%{_pre}/%{_class}/Command/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Command
install %{_pearname}-%{version}%{_pre}/%{_class}/Downloader/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Downloader
install %{_pearname}-%{version}%{_pre}/%{_class}/Frontend/CLI.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Frontend
install %{_pearname}-%{version}%{_pre}/%{_class}/Installer/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Installer
install %{_pearname}-%{version}%{_pre}/%{_class}/Installer/Role/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Installer/Role
install %{_pearname}-%{version}%{_pre}/%{_class}/PackageFile/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/PackageFile
install %{_pearname}-%{version}%{_pre}/%{_class}/PackageFile/Generator/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/PackageFile/Generator
install %{_pearname}-%{version}%{_pre}/%{_class}/PackageFile/Parser/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/PackageFile/Parser
install %{_pearname}-%{version}%{_pre}/%{_class}/PackageFile/v2/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/PackageFile/v2
install %{_pearname}-%{version}%{_pre}/%{_class}/Task/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Task
install %{_pearname}-%{version}%{_pre}/%{_class}/Validator/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Validator
install %{_pearname}-%{version}%{_pre}/scripts/pearcmd.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}%{_pre}/scripts/peclcmd.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}%{_pre}/scripts/pear.sh $RPM_BUILD_ROOT%{_bindir}/pear
install %{_pearname}-%{version}%{_pre}/scripts/pecl.sh $RPM_BUILD_ROOT%{_bindir}/pecl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{php_pear_dir}/*
