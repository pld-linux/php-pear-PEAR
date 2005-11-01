%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.2
Release:	2
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	15d947df0e18c352a1aeaa7ad655e595
Source1:	%{name}-template.spec
Patch0:		%{name}-memory.patch
Patch1:		%{name}-sysconfdir.patch
Patch2:		%{name}-rpmpkgname.patch
Patch3:		%{name}-rpmvars.patch
Patch5:		%{name}-cli.patch
URL:		http://pear.php.net/package/PEAR
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequries:	php(program)
BuildRequires:	php-pear >= 4:1.0-6
Requires:	php-cli
Requires:	php-pcre
Requires:	php-pear >= 4:1.0-5.5
Requires:	php-pear-Archive_Tar >= 1.1
Requires:	php-pear-Console_Getopt >= 1.2
Requires:	php-pear-XML_RPC >= 1.4.0
Requires:	php-xml
Requires:	php-zlib
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
%pear_package_setup
%patch0 -p2
%patch1 -p1
%patch2 -p1
%patch3 -p1
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
cp -a ./%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}

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
%{php_pear_dir}/*.php
%{php_pear_dir}/OS
%{php_pear_dir}/PEAR/*

%{php_pear_dir}/data/*
