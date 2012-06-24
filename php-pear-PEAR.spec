%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.5
Release:	1
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	be4300609e4d966a6d68d6ec95942180
Source1:	%{name}-template.spec
Patch0:		%{name}-memory.patch
Patch1:		%{name}-sysconfdir.patch
Patch2:		%{name}-rpmpkgname.patch
Patch3:		%{name}-rpmvars.patch
Patch4:		%{name}-cli.patch
Patch5:		%{name}-old-api.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	php-cli
BuildRequires:	php-pear >= 4:1.0-6
Requires:	php-cli
Requires:	php-pcre
Requires:	php-pear >= 4:1.0-5.5
Requires:	php-pear-Archive_Tar >= 1.1
Requires:	php-pear-Console_Getopt >= 1.2
Requires:	php-pear-XML_RPC >= 1.4.0
Requires:	php-xml
Requires:	php-zlib
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend-CLI
Obsoletes:	php-pear-PEAR-OS
Conflicts:	php-pear-Archive_Tar = 1.3.0
Conflicts:	php-pear-PEAR_Frontend_Web < 0.5.0
Conflicts:	php-pear-PEAR_Frontend_Gtk < 0.4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(PEAR/FTP.php)' 'pear(Net/FTP.php)'

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
- PEAR installer do tworzenia, dystrybucji i instalowania pakiet�w,
- mechanizm PEAR_Exception (w fazie alpha) do obs�ugi b��d�w PHP5,
- zaawansowany mechanizm PEAR_ErrorStack (w fazie beta) do obs�ugi
  b��d�w,
- mechanizm obs�ugi b��d�w PEAR_Error,
- klas� OS_Guess do pozyskiwania informacji na temat systemu
  operacyjnego,
- klas� System do szybkiej obs�ugi typowych operacji na plikach i
  katalogach,
- podstawow� klasy PEAR.

Ta klasa ma w PEAR status: %{_status}.

%package core
Summary:	PEAR core classes
Summary(pl):	G��wne klasy PEAR-a
Group:		Development/Languages/PHP

%description core
This package includes PEAR core classes:
- PEAR class and PEAR_Error
- System
- OS_Guess
and classes for PHP 5:
- PEAR_ErrorStack and PEAR_Exception

%description core -l pl
Ten pakiet zawiera g��wne klasy PEAR-a:
- klas� PEAR i PEAR_Error
- System
- OS_Gueass
oraz klasy dla PHP 5:
- PEAR_ErrorStack i PEAR_Exception

%prep
%pear_package_setup
%patch0 -p2
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{php_pear_dir},%{_bindir}}

D=$(pwd)
pearcmd() {
	php -d output_buffering=1 -d include_path=".:${D}%{php_pear_dir}" ${D}%{php_pear_dir}/pearcmd.php -c ${D}/pearrc "$@"
}
pearcmd config-set doc_dir %{_docdir} || exit
pearcmd config-set data_dir %{php_pear_dir}/data || exit
pearcmd config-set php_dir %{php_pear_dir} || exit
pearcmd config-set test_dir %{php_pear_dir}/tests || exit
pearcmd config-set sig_bin %{_bindir}/gpg || exit
cp $D/pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

%pear_package_install
install ./%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}

sed -e '/^\$''Log: /,$d' %{SOURCE1} > $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec
echo '$''Log: $' >> $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc install.log
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pear.conf
%attr(755,root,root) %{_bindir}/*
%{php_pear_dir}/.registry/*.reg
%{php_pear_dir}/pearcmd.php
%{php_pear_dir}/peclcmd.php
%{php_pear_dir}/PEAR/[!CE]*
%{php_pear_dir}/PEAR/ChannelFile*
%{php_pear_dir}/PEAR/Command*
%{php_pear_dir}/PEAR/Config.php
%{php_pear_dir}/PEAR/Common.php

%{php_pear_dir}/data/*

%files core
%defattr(644,root,root,755)
%{php_pear_dir}/PEAR.php
%{php_pear_dir}/System.php
%{php_pear_dir}/OS
%dir %{php_pear_dir}/PEAR
%{php_pear_dir}/PEAR/ErrorStack.php
%{php_pear_dir}/PEAR/Exception.php
