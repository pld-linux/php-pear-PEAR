%include	/usr/lib/rpm/macros.php
%define		_pearname	PEAR
Summary:	PEAR - main php pear class
Summary(pl):	PEAR - podstawowa klasa dla php pear
Name:		php-pear-%{_pearname}
Version:	0.90
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
PreReq:		php-zlib >= 4.2.0
URL:		http://pear.php.net/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PEAR package contains:
- the PEAR base class
- the PEAR_Error error handling mechanism
- the PEAR installer, for creating, distributing and installing
  packages

%description -l pl
Pakiet PEAR zawiara:
- Postawow� klas� PEAR
- Mechanizm obs�ugi b��d�w PEAR_Error
- PEAR installer do tworzenia, dystrybucji i instalowania pakiet�w

%package Command
Summary:	PEAR - main php pear class
Summary(pl):	PEAR - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description Command
Command class for PEAR.

%description -l pl Command
Klasa Command dla PEARa.

%package OS
Summary:	PEAR - main php pear class
Summary(pl):	PEAR - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description OS
OS_Guess class for PEAR.

%description -l pl OS
Klasa OS_Guess dla PEARa.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
cd %{_pearname}-%{version}

install -d $RPM_BUILD_ROOT%{php_pear_dir}/{%{_pearname}/{Command,Frontend},OS}

install *.php			$RPM_BUILD_ROOT%{php_pear_dir}
install PEAR/*.php		$RPM_BUILD_ROOT%{php_pear_dir}/%{_pearname}
install PEAR/Command/*.php	$RPM_BUILD_ROOT%{php_pear_dir}/%{_pearname}/Command
install PEAR/Frontend/*.php	$RPM_BUILD_ROOT%{php_pear_dir}/%{_pearname}/Frontend
install OS/*.php		$RPM_BUILD_ROOT%{php_pear_dir}/OS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{php_pear_dir}/*.php

%files Command
%defattr(644,root,root,755)
%dir %{php_pear_dir}/%{_pearname}
%dir %{php_pear_dir}/%{_pearname}/Command
%{php_pear_dir}/%{_pearname}/*.php
%{php_pear_dir}/%{_pearname}/Command/*.php
%{php_pear_dir}/%{_pearname}/Frontend/*.php

%files OS
%defattr(644,root,root,755)
%dir %{php_pear_dir}/OS
%{php_pear_dir}/OS/*.php
