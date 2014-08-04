# TODO
# - bootstrap fails if /usr/share/pear/.lock doesn't exist (just create it as 644)
# - should understand as php extension (php-pear-Auth):
#   pear/Auth can optionally use package "pecl/vpopmail" (version >= 0.2)
#   pear/Auth can optionally use package "pecl/kadm5" (version >= 0.2.3)
#
%define		_pearname	PEAR
%define		_status		stable
%define		php_name	php%{?php_suffix}
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	PEAR Base System
Summary(pl.UTF-8):	Podstawowy system PEAR
Name:		php-pear-%{_pearname}
Version:	1.9.5
Release:	1
Epoch:		1
License:	New BSD License
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	f44a56765988dafbe348828cac2562ca
Source1:	http://pear.php.net/get/Console_Getopt-1.2.3.tgz
# Source1-md5:	d7618327f9302a7191893768982de823
Source2:	http://pear.php.net/get/Structures_Graph-1.0.3.tgz
# Source2-md5:	d2d8db74818be5cb0af7def3fc285bfc
Patch0:		%{name}-sysconfdir.patch
Patch1:		ext-check.patch
Patch2:		%{name}-FHS.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	%{php_name}-pcre
BuildRequires:	%{php_name}-xml
BuildRequires:	/usr/bin/php
BuildRequires:	rpm-php-pearprov >= 4.4.2-30.1
BuildRequires:	rpmbuild(macros) >= 1.654
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Requires:	/usr/bin/php
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(xml)
Requires:	php(zlib)
Requires:	php-pear >= 4:1.2-1
Requires:	php-pear-Archive_Tar >= 1.3.11
Requires:	php-pear-Console_Getopt >= 1.2.3
Requires:	php-pear-Structures_Graph >= 1.0.4
Requires:	php-pear-XML_Util >= 1.2.3
Requires:	rpm-whiteout
Suggests:	php-pear-Net_FTP
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend_CLI
Obsoletes:	php-pear-PEAR-OS
Conflicts:	php-pear-PEAR_Frontend_Gtk < 0.4.0
Conflicts:	php-pear-PEAR_Frontend_Web < 0.5.0
Conflicts:	rpm-whiteout < 1.1
Conflicts:	rpmbuild(macros) < 1.563
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# PEAR_Command_Packaging is separate package
# PEAR_FTP is optional
%define		_noautoreq_pear PEAR/FTP.php Net/FTP.php XML/RPC.* PEAR/Command/Packaging.php

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
Requires:	php(core) >= %{php_min_version}

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
%define __build_dir %{_builddir}/%{_pearname}-%{version}%{?_rc}
%define	__php_include_path %{__build_dir}/%{_pearname}-%{version}%{?_rc}:%{__build_dir}/%(basename %{SOURCE1} .tgz):%{__build_dir}/%(basename %{SOURCE2} .tgz)
%define __pear php -dmemory_limit=-1 -doutput_buffering=1 -dinclude_path="%__php_include_path" %{__build_dir}/%{_pearname}-%{version}%{?_rc}/scripts/pearcmd.php

%setup -q -c -n %{_pearname}-%{version} -a1 -a2
%pear_package_setup -z -D -n %{_pearname}-%{version}%{?_rc}

%patch0 -p1
%patch1 -p1
%{?with_FHS:%patch2 -p1}

find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%build
D=$(pwd)
pearcmd() {
	%{__pear} -c ${D}/pearrc "$@"
}
pearcmd config-set doc_dir %{_docdir}
pearcmd config-set data_dir %{php_pear_dir}/data
pearcmd config-set php_dir %{php_pear_dir}
pearcmd config-set test_dir %{php_pear_dir}/tests
pearcmd config-set sig_bin %{_bindir}/gpg
pearcmd config-set cfg_dir %{_sysconfdir}/pear

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/pear,%{php_pear_dir},%{_bindir}}
%pear_package_install
cp -a pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

# -C and -q options were for php-cgi, in php-cli they're enabled by default.
%define php_exec exec /usr/bin/php -dinclude_path=%{php_pear_dir} -doutput_buffering=1
cat > $RPM_BUILD_ROOT%{_bindir}/pear <<'EOF'
#!/bin/sh
%php_exec -dopen_basedir="" -dmemory_limit=128M %{php_pear_dir}/pearcmd.php "$@"
EOF
cat > $RPM_BUILD_ROOT%{_bindir}/peardev <<'EOF'
#!/bin/sh
%php_exec -dopen_basedir="" -dmemory_limit=-1 %{php_pear_dir}/pearcmd.php "$@"
EOF
# This -dextension=pcre.so works with php-5.1, and patched php-cli >= 4:5.0.5-18.1, php4-cli >= 3:4.4.1-6.1
# -n is there because devs on #pear said this avoids locking problems when replacing in use libraries.
cat > $RPM_BUILD_ROOT%{_bindir}/pecl <<'EOF'
#!/bin/sh
%php_exec -dmemory_limit=64M -dsafe_mode=0 -n -dextension=xml.so %{php_pear_dir}/peclcmd.php "$@"
EOF
# for rpm to find interpreter
chmod +x $RPM_BUILD_ROOT%{_bindir}/*

%post
if [ -f %{_docdir}/%{name}-%{version}/optional-packages.txt ]; then
	cat %{_docdir}/%{name}-%{version}/optional-packages.txt
fi

# need to bootstrap for non-root user
if [ ! -f %{php_pear_dir}/.lock ]; then
	umask 2
	%{_bindir}/pear list > /dev/null
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc install.log optional-packages.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pear.conf
%dir %{_sysconfdir}/pear
%attr(755,root,root) %{_bindir}/pear
%attr(755,root,root) %{_bindir}/peardev
%attr(755,root,root) %{_bindir}/pecl
%{php_pear_dir}/.registry/pear.reg
%{php_pear_dir}/pearcmd.php
%{php_pear_dir}/peclcmd.php
%{php_pear_dir}/PEAR/*

# in -core subpackage
%exclude %{php_pear_dir}/PEAR/ErrorStack.php
%exclude %{php_pear_dir}/PEAR/Exception.php
%exclude %{php_pear_dir}/PEAR/FixPHP5PEARWarnings.php

%{php_pear_dir}/data/*

%files core
%defattr(644,root,root,755)
%{php_pear_dir}/PEAR.php
%{php_pear_dir}/PEAR5.php
%{php_pear_dir}/System.php
%{php_pear_dir}/OS
%dir %{php_pear_dir}/PEAR
%{php_pear_dir}/PEAR/ErrorStack.php
%{php_pear_dir}/PEAR/Exception.php
%{php_pear_dir}/PEAR/FixPHP5PEARWarnings.php
