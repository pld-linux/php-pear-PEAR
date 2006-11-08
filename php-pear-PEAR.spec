%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.6
Release:	5
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	0ef3f7a2b095c290e1915d99048b7644
Source1:	%{name}-template.spec
Patch0:		%{name}-sysconfdir.patch
Patch1:		%{name}-rpmpkgname.patch
Patch2:		%{name}-rpmvars.patch
Patch3:		%{name}-old-api.patch
Patch4:		%{name}-specfile.patch
Patch5:		%{name}-packagingroot.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	php-cli
BuildRequires:	php-pear-PEAR >= 1:1.4.0-0.b1.3
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Requires:	/usr/bin/php
Requires:	php-pcre
Requires:	php-pear >= 4:1.0-14
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

%define		_noautoreq	'pear(PEAR/FTP.php)' 'pear(Net/FTP.php)' 'pear(XML/RPC.*)'

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
%pear_package_setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
cd ./%{php_pear_dir}
%patch5 -p1

find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{php_pear_dir},%{_bindir}}

D=$(pwd)
pearcmd() {
	php -doutput_buffering=1 -dinclude_path=".:${D}%{php_pear_dir}" ${D}%{php_pear_dir}/pearcmd.php -c ${D}/pearrc "$@"
}
pearcmd config-set doc_dir %{_docdir} || exit
pearcmd config-set data_dir %{php_pear_dir}/data || exit
pearcmd config-set php_dir %{php_pear_dir} || exit
pearcmd config-set test_dir %{php_pear_dir}/tests || exit
pearcmd config-set sig_bin %{_bindir}/gpg || exit
cp $D/pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

%pear_package_install
install -d $RPM_BUILD_ROOT%{php_pear_dir}/{.registry/.channel.{__uri,pecl.php.net},.channels/.alias}
touch $RPM_BUILD_ROOT%{php_pear_dir}/.depdb{,lock}
touch $RPM_BUILD_ROOT%{php_pear_dir}/.channels/{__uri,{pear,pecl}.php.net}.reg
touch $RPM_BUILD_ROOT%{php_pear_dir}/.channels/.alias/{pear,pecl}.txt
touch $RPM_BUILD_ROOT%{php_pear_dir}/.filemap
touch $RPM_BUILD_ROOT%{php_pear_dir}/.lock

# -C and -q options were for php-cgi, in php-cli they're enabled by default.
%define php_exec exec /usr/bin/php -dinclude_path=%{php_pear_dir} -doutput_buffering=1
cat > $RPM_BUILD_ROOT%{_bindir}/pear <<'EOF'
#!/bin/sh
%php_exec -dmemory_limit=24M %{php_pear_dir}/pearcmd.php "$@"
EOF
cat > $RPM_BUILD_ROOT%{_bindir}/peardev <<'EOF'
#!/bin/sh
%php_exec -dmemory_limit=-1 %{php_pear_dir}/pearcmd.php "$@"
EOF
# This -dextension=pcre.so works with php-5.1, and patched php-cli >= 4:5.0.5-18.1, php4-cli >= 3:4.4.1-6.1
# -n is there because devs on #pear said this avoids locking problems when replacing in use libraries.
cat > $RPM_BUILD_ROOT%{_bindir}/pecl <<'EOF'
#!/bin/sh
%php_exec -dmemory_limit=24M -dsafe_mode=0 -n -dextension=pcre.so -dextension=xml.so %{php_pear_dir}/peclcmd.php "$@"
EOF
# for rpm to find interpreter
chmod +x $RPM_BUILD_ROOT%{_bindir}/*

sed -e '/^\$''Log: /,$d' %{SOURCE1} > $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec
echo '$''Log: $' >> $RPM_BUILD_ROOT%{php_pear_dir}/data/%{_class}/template.spec

%post
if [ ! -f %{php_pear_dir}/.lock ]; then
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
%{php_pear_dir}/.registry/*.reg
%{php_pear_dir}/pearcmd.php
%{php_pear_dir}/peclcmd.php
%{php_pear_dir}/PEAR/[!CE]*
%{php_pear_dir}/PEAR/ChannelFile*
%{php_pear_dir}/PEAR/Command*
%{php_pear_dir}/PEAR/Config.php
%{php_pear_dir}/PEAR/Common.php

%{php_pear_dir}/data/*

# registry
%dir %{php_pear_dir}/.channels
%dir %{php_pear_dir}/.channels/.alias

%ghost %{php_pear_dir}/.channels/.alias/pear.txt
%ghost %{php_pear_dir}/.channels/.alias/pecl.txt
%ghost %{php_pear_dir}/.channels/pear.php.net.reg
%ghost %{php_pear_dir}/.channels/pecl.php.net.reg
%ghost %{php_pear_dir}/.channels/__uri.reg
%ghost %{php_pear_dir}/.registry/.channel.__uri
%ghost %{php_pear_dir}/.registry/.channel.pecl.php.net
%ghost %{php_pear_dir}/.depdblock
%ghost %{php_pear_dir}/.depdb
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
