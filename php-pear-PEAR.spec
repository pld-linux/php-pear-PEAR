%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}
#
%include	/usr/lib/rpm/macros.php
Summary:	PEAR Base System
Summary(pl):	Podstawowy system PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.9
Release:	0.26
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	52257e23987717c474a3da87f161a272
Source1:	http://pear.php.net/get/Console_Getopt-1.2.tgz
# Source1-md5:	8f9ec8253c04350bc01ee7ca941e24b6
Source2:	%{name}-template.spec
Patch0:		%{name}-sysconfdir.patch
Patch1:		%{name}-rpmpkgname.patch
Patch2:		%{name}-rpmvars.patch
Patch3:		%{name}-old-api.patch
Patch4:		%{name}-specfile.patch
Patch5:		%{name}-FHS.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	php-cli
BuildRequires:	rpm-php-pearprov >= 4.4.2-30.1
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Requires:	/usr/bin/php
Requires:	php-pcre
Requires:	php-pear >= 4:1.0-12.3
Requires:	php-pear-Archive_Tar >= 1.1
Requires:	php-pear-Console_Getopt >= 1.2
Requires:	php-pear-XML_RPC >= 1.4.0
Requires:	php-xml
Requires:	php-zlib
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
%define		_statedir		/var/lib/pear
%define		pear_registry	%{_statedir}/registry

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

%package core
Summary:	PEAR core classes
Summary(pl):	G³ówne klasy PEAR-a
Group:		Development/Languages/PHP

%description core
This package includes PEAR core classes:
- PEAR class and PEAR_Error
- System
- OS_Guess
and classes for PHP 5:
- PEAR_ErrorStack and PEAR_Exception

%description core -l pl
Ten pakiet zawiera g³ówne klasy PEAR-a:
- klasê PEAR i PEAR_Error
- System
- OS_Gueass
oraz klasy dla PHP 5:
- PEAR_ErrorStack i PEAR_Exception

%prep
%define __build_dir %{_builddir}/%{_class}-%{version}
%define	__php_include_path %{__build_dir}/%{_class}-%{version}:%{__build_dir}/%(basename %{SOURCE1} .tgz)
%define __pear php -doutput_buffering=1 -dinclude_path="%__php_include_path" %{__build_dir}/%{_class}-%{version}/scripts/pearcmd.php
%pear_package_setup -z -a1

%patch0 -p1
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
	%{__pear} -c ${D}/pearrc "$@"
}
pearcmd config-set doc_dir %{_docdir} || exit
pearcmd config-set data_dir %{php_pear_dir}/data || exit
pearcmd config-set php_dir %{php_pear_dir} || exit
pearcmd config-set test_dir %{php_pear_dir}/tests || exit
pearcmd config-set sig_bin %{_bindir}/gpg || exit
cp $D/pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

%pear_package_install

install -d $RPM_BUILD_ROOT%{_statedir}/channels/.alias
install -d $RPM_BUILD_ROOT%{pear_registry}/{.channel.{__uri,pecl.php.net},channels/.alias}
touch $RPM_BUILD_ROOT%{_statedir}/.depdb{,lock}
touch $RPM_BUILD_ROOT%{_statedir}/channels/{__uri,{pear,pecl}.php.net}.reg
touch $RPM_BUILD_ROOT%{_statedir}/channels/.alias/{pear,pecl}.txt
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

sed -e '/^\$''Log: /,$d' %{SOURCE2} > $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec
echo '$''Log: $' >> $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec

%post
if [ ! -L %{php_pear_dir}/.registry ]; then
	if [ -d %{php_pear_dir}/.registry ]; then
		install -d %{pear_registry}
		mv -f %{php_pear_dir}/.registry/*.reg %{pear_registry}
		rmdir %{php_pear_dir}/.registry/.channel.* 2>/dev/null
		rmdir %{php_pear_dir}/.registry/* 2>/dev/null
		rmdir %{php_pear_dir}/.registry 2>/dev/null || mv -v %{php_pear_dir}/.registry{,.rpmsave}
	fi
	ln -s %{pear_registry} %{php_pear_dir}/.registry
fi

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

%dir %{_statedir}
%dir %{_statedir}/channels
%dir %{_statedir}/registry
%dir %{_statedir}/channels/.alias

%ghost %{_statedir}/channels/.alias/pear.txt
%ghost %{_statedir}/channels/.alias/pecl.txt
%ghost %{_statedir}/channels/pear.php.net.reg
%ghost %{_statedir}/channels/pecl.php.net.reg
%ghost %{_statedir}/channels/__uri.reg
%ghost %{_statedir}/registry/.channel.__uri
%ghost %{_statedir}/registry/.channel.pecl.php.net
%ghost %{_statedir}/.depdblock
%ghost %{_statedir}/.depdb
%ghost %{php_pear_dir}/.filemap
%ghost %{php_pear_dir}/.lock
%ghost %dir %{php_pear_dir}/.registry

%files core
%defattr(644,root,root,755)
%{php_pear_dir}/PEAR.php
%{php_pear_dir}/System.php
%{php_pear_dir}/OS
%dir %{php_pear_dir}/PEAR
%{php_pear_dir}/PEAR/ErrorStack.php
%{php_pear_dir}/PEAR/Exception.php
