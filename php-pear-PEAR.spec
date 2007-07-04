# TODO
# - bootstrap fails if /usr/share/pear/.lock doesn't exist (just create it as 644)
# - should understand as php extension (php-pear-Auth):
#   pear/Auth can optionally use package "pecl/vpopmail" (version >= 0.2)
#   pear/Auth can optionally use package "pecl/kadm5" (version >= 0.2.3)
#
# Conditional build:
%bcond_with	FHS			# writable files in /var/lib/pear. NEEDS LOTS OF PATCHING AND CONVINCING UPSTREAM
#
# NOTE
# - macros needed to build this package are in SOURCES/php-pear-build-macros@DEVEL
%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}
#
%include	/usr/lib/rpm/macros.php
Summary:	PEAR Base System
Summary(pl.UTF-8):	Podstawowy system PEAR
Name:		php-pear-%{_pearname}
Version:	1.6.1
Release:	2
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	1476f0ec3917d68e3d7af1346a9a7b89
Source1:	http://pear.php.net/get/Console_Getopt-1.2.tgz
# Source1-md5:	8f9ec8253c04350bc01ee7ca941e24b6
Source2:	http://pear.php.net/get/Structures_Graph-1.0.2.tgz
# Source2-md5:	2664e2d024048f982e12fad4d1bfbb87
Patch0:		%{name}-sysconfdir.patch
Patch1:		%{name}-strict.patch
Patch5:		%{name}-FHS.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	/usr/bin/php
BuildRequires:	php(pcre)
BuildRequires:	php(xml)
BuildRequires:	rpm-php-pearprov >= 4.4.2-30.1
BuildRequires:	rpmbuild(macros) >= 1.375
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Requires:	/usr/bin/php
Requires:	php(pcre)
Requires:	php(xml)
Requires:	php(zlib)
Requires:	php-pear >= 4:1.0-14
Requires:	php-pear-Archive_Tar >= 1.1
Requires:	php-pear-Console_Getopt >= 1.2
Requires:	php-pear-Structures_Graph >= 1.0.2
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend-CLI
Obsoletes:	php-pear-PEAR-OS
#Suggests:	php-pear-Net_FTP
Conflicts:	php-pear-Archive_Tar = 1.3.0
Conflicts:	php-pear-PEAR_Frontend_Gtk < 0.4.0
Conflicts:	php-pear-PEAR_Frontend_Web < 0.5.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# PEAR_Command_Packaging is separate package
%define		_noautoreq	'pear(PEAR/FTP.php)' 'pear(Net/FTP.php)' 'pear(XML/RPC.*)' 'pear(PEAR/Command/Packaging.php)'
%if %{with FHS}
%define		_statedir		/var/lib/pear
%define		_registrydir	%{_statedir}/registry
%define		_channelsdir	%{_statedir}/.channels
%else
%define		_statedir		%{php_pear_dir}
%define		_registrydir	%{_statedir}/.registry
%define		_channelsdir	%{_statedir}/.channels
%endif

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

%description -l pl.UTF-8
Pakiet PEAR zawiara:
- PEAR installer do tworzenia, dystrybucji i instalowania pakietów,
- mechanizm PEAR_Exception (w fazie alpha) do obsługi błędów PHP5,
- zaawansowany mechanizm PEAR_ErrorStack (w fazie beta) do obsługi
  błędów,
- mechanizm obsługi błędów PEAR_Error,
- klasę OS_Guess do pozyskiwania informacji na temat systemu
  operacyjnego,
- klasę System do szybkiej obsługi typowych operacji na plikach i
  katalogach,
- podstawową klasy PEAR.

Ta klasa ma w PEAR status: %{_status}.

%package core
Summary:	PEAR core classes
Summary(pl.UTF-8):	Główne klasy PEAR-a
Group:		Development/Languages/PHP

%description core
This package includes PEAR core classes:
- PEAR class and PEAR_Error
- System
- OS_Guess
and classes for PHP 5:
- PEAR_ErrorStack and PEAR_Exception

%description core -l pl.UTF-8
Ten pakiet zawiera główne klasy PEAR-a:
- klasę PEAR i PEAR_Error
- System
- OS_Gueass
oraz klasy dla PHP 5:
- PEAR_ErrorStack i PEAR_Exception

%prep
%define __build_dir %{_builddir}/%{_class}-%{version}%{?_rc}
%define	__php_include_path %{__build_dir}/%{_class}-%{version}%{?_rc}:%{__build_dir}/%(basename %{SOURCE1} .tgz):%{__build_dir}/%(basename %{SOURCE2} .tgz)
%define __pear php -dmemory_limit=-1 -doutput_buffering=1 -dinclude_path="%__php_include_path" %{__build_dir}/%{_class}-%{version}%{?_rc}/scripts/pearcmd.php

%setup -q -c -n %{_pearname}-%{version} -a1 -a2
%pear_package_setup -z -D -n %{_pearname}-%{version}%{?_rc}

%patch0 -p1
%patch1 -p1
%{?with_FHS:%patch5 -p1}

find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%build
D=$(pwd)
pearcmd() {
	%{__pear} -c ${D}/pearrc "$@"
}
pearcmd config-set doc_dir %{_docdir} || exit
pearcmd config-set data_dir %{php_pear_dir}/data || exit
pearcmd config-set php_dir %{php_pear_dir} || exit
pearcmd config-set test_dir %{php_pear_dir}/tests || exit
pearcmd config-set sig_bin %{_bindir}/gpg || exit

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{php_pear_dir},%{_bindir}}
%pear_package_install
cp pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

install -d $RPM_BUILD_ROOT%{_channelsdir}/.alias
install -d $RPM_BUILD_ROOT%{_registrydir}/{.channel.{__uri,pecl.php.net},channels/.alias}
touch $RPM_BUILD_ROOT%{_statedir}/.depdb{,lock}
touch $RPM_BUILD_ROOT%{_channelsdir}/{__uri,{pear,pecl}.php.net}.reg
touch $RPM_BUILD_ROOT%{_channelsdir}/.alias/{pear,pecl}.txt
touch $RPM_BUILD_ROOT%{php_pear_dir}/.filemap
touch $RPM_BUILD_ROOT%{php_pear_dir}/.lock

# -C and -q options were for php-cgi, in php-cli they're enabled by default.
%define php_exec exec /usr/bin/php -dinclude_path=%{php_pear_dir} -doutput_buffering=1
cat > $RPM_BUILD_ROOT%{_bindir}/pear <<'EOF'
#!/bin/sh
%php_exec -dopen_basedir="" -dmemory_limit=24M %{php_pear_dir}/pearcmd.php "$@"
EOF
cat > $RPM_BUILD_ROOT%{_bindir}/peardev <<'EOF'
#!/bin/sh
%php_exec -dopen_basedir="" -dmemory_limit=-1 %{php_pear_dir}/pearcmd.php "$@"
EOF
# This -dextension=pcre.so works with php-5.1, and patched php-cli >= 4:5.0.5-18.1, php4-cli >= 3:4.4.1-6.1
# -n is there because devs on #pear said this avoids locking problems when replacing in use libraries.
cat > $RPM_BUILD_ROOT%{_bindir}/pecl <<'EOF'
#!/bin/sh
%php_exec -dmemory_limit=24M -dsafe_mode=0 -n -dextension=pcre.so -dextension=xml.so %{php_pear_dir}/peclcmd.php "$@"
EOF
# for rpm to find interpreter
chmod +x $RPM_BUILD_ROOT%{_bindir}/*

%post
%if %{with FHS}
if [ ! -L %{php_pear_dir}/.registry ]; then
	if [ -d %{php_pear_dir}/.registry ]; then
		install -d %{_registrydir}
		mv -f %{php_pear_dir}/.registry/*.reg %{_registrydir}
		rmdir %{php_pear_dir}/.registry/.channel.* 2>/dev/null
		rmdir %{php_pear_dir}/.registry/* 2>/dev/null
		rmdir %{php_pear_dir}/.registry 2>/dev/null || mv -v %{php_pear_dir}/.registry{,.rpmsave}
	fi
	ln -s %{_registrydir} %{php_pear_dir}/.registry
fi
%endif

if [ ! -f %{php_pear_dir}/.lock ]; then
	umask 2
	%{_bindir}/pear list > /dev/null
fi

if [ -f %{_docdir}/%{name}-%{version}/optional-packages.txt ]; then
	cat %{_docdir}/%{name}-%{version}/optional-packages.txt
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc install.log optional-packages.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pear.conf
%attr(755,root,root) %{_bindir}/*
%{php_pear_dir}/.registry/pear.reg
%{php_pear_dir}/pearcmd.php
%{php_pear_dir}/peclcmd.php
%{php_pear_dir}/PEAR/[!CE]*
%{php_pear_dir}/PEAR/ChannelFile*
%{php_pear_dir}/PEAR/Command*
%{php_pear_dir}/PEAR/Config.php
%{php_pear_dir}/PEAR/Common.php

%{php_pear_dir}/data/*

%if %{with FHS}
%dir %{_statedir}
%dir %{_registrydir}
%ghost %dir %{php_pear_dir}/.registry
%endif
%dir %{_channelsdir}
%dir %{_channelsdir}/.alias

%ghost %{_channelsdir}/.alias/pear.txt
%ghost %{_channelsdir}/.alias/pecl.txt
%ghost %{_channelsdir}/pear.php.net.reg
%ghost %{_channelsdir}/pecl.php.net.reg
%ghost %{_channelsdir}/__uri.reg
%ghost %{_registrydir}/.channel.__uri
%ghost %{_registrydir}/.channel.pecl.php.net
%ghost %{_statedir}/.depdblock
%ghost %{_statedir}/.depdb
%ghost %{php_pear_dir}/.filemap
%ghost %{php_pear_dir}/.lock

%files core
%defattr(644,root,root,755)
%{php_pear_dir}/PEAR.php
%{php_pear_dir}/System.php
%{php_pear_dir}/OS
%dir %{php_pear_dir}/PEAR
%{php_pear_dir}/PEAR/ErrorStack.php
%{php_pear_dir}/PEAR/Exception.php
