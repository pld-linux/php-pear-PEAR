%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		beta
%define		_pearname	%{_class}
%define		_noautoreq	'pear(PEAR/FTP.php)'

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.4.0
%define		_pre b1
%define		_rel 3.3
Release:	0.%{_pre}.%{_rel}
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}%{_pre}.tgz
# Source0-md5:	fac6e8d80991ae3a63cb6a616958e833
Patch0:		%{name}-memory.patch
URL:		http://pear.php.net/package/PEAR/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	sed >= 4.0.0
Requires:	php-pear >= 4:1.0-4
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
%pear_package_setup -n %{_pearname}-%{version}%{_pre}
%patch0 -p2

# don't know why this happens:
grep -rl "%{_builddir}/%{name}-%{version}" usr | xargs -r sed -i -e "s,%{_builddir}/%{name}-%{version},,"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT
cp -a usr $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{php_pear_dir}/.{channels,dep*,filemap,lock}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{php_pear_dir}/.registry/*.reg
%{php_pear_dir}/*
