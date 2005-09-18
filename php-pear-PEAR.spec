%include	/usr/lib/rpm/macros.php
%include	/usr/lib/rpm/macros.pear
%define		_class		PEAR
%define		_status		beta
%define		_pearname	%{_class}
%define		_noautoreq	'pear(PEAR/FTP.php)'

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.0
%define		_pre b1
%define		_rel 3.20
Release:	0.%{_pre}.%{_rel}
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}%{_pre}.tgz
# Source0-md5:	fac6e8d80991ae3a63cb6a616958e833
Patch0:		%{name}-memory.patch
Patch1:		%{name}-sysconfdir.patch
URL:		http://pear.php.net/package/PEAR/
BuildRequires:	php-pear-build >= 0.3
Requires:	php-pear >= 4:1.0-5.5
Requires:	php-cli
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend-CLI
Obsoletes:	php-pear-PEAR-OS
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# displayed in %post
%define     _noautocompressdoc  optional-packages.txt

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
# TODO:
# PEAR: Optional feature remoteinstall available (adds the ability to install packages to a remote ftp server)
# PEAR: Optional feature webinstaller available (PEAR's web-based installer)
# PEAR: Optional feature gtkinstaller available (PEAR's PHP-GTK-based installer)
%pear_package_setup
%patch0 -p2
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{php_pear_dir},%{_bindir}}

D=%{_builddir}/%{name}-%{version}
pearcmd() {
	HOME=${D} php -d output_buffering=1 -d include_path=".:${D}%{php_pear_dir}" ${D}%{php_pear_dir}/pearcmd.php "$@"
}
pearcmd config-set doc_dir %{_docdir} || exit
pearcmd config-set data_dir %{php_pear_dir}/data || exit
pearcmd config-set php_dir %{php_pear_dir} || exit
pearcmd config-set test_dir %{php_pear_dir}/tests || exit
pearcmd config-set sig_bin %{_bindir}/gpg || exit
cp $D/.pearrc $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

cp -a ./%{php_pear_dir}/{.registry,*} $RPM_BUILD_ROOT%{php_pear_dir}
cp -a ./%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_docdir}/%{name}-%{version}/optional-packages.txt ]; then
	cat %{_docdir}/%{name}-%{version}/optional-packages.txt
fi

%files
%defattr(644,root,root,755)
%doc install.log optional-packages.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pear.conf
%attr(755,root,root) %{_bindir}/*
%{php_pear_dir}/.registry/*.reg
%{php_pear_dir}/*
