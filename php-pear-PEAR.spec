%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_pearname	%{_class}
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Name:		php-pear-%{_pearname}
Version:	0.90
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
BuildRequires:	rpm-php-pearprov
Requires:	php-pear
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
- Postawow± klasê PEAR
- Mechanizm obs³ugi b³êdów PEAR_Error
- PEAR installer do tworzenia, dystrybucji i instalowania pakietów

%package Command
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description Command
Command class for PEAR.

%description -l pl Command
Klasa Command dla PEARa.

%package OS
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description OS
OS_Guess class for PEAR.

%description -l pl OS
Klasa OS_Guess dla PEARa.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_pear_dir}/{%{_class}/{Command,Frontend},OS}

install %{_pearname}-%{version}/*.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}/OS/*.php $RPM_BUILD_ROOT%{php_pear_dir}/OS
install %{_pearname}-%{version}/%{_class}/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}
install %{_pearname}-%{version}/%{_class}/Command/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Command
install %{_pearname}-%{version}/%{_class}/Frontend/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Frontend

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{php_pear_dir}/*.php

%files Command
%defattr(644,root,root,755)
%dir %{php_pear_dir}/%{_class}/Command
%dir %{php_pear_dir}/%{_class}/Frontend
%{php_pear_dir}/%{_class}/*.php
%{php_pear_dir}/%{_class}/Command/*.php
%{php_pear_dir}/%{_class}/Frontend/*.php

%files OS
%defattr(644,root,root,755)
%dir %{php_pear_dir}/OS
%{php_pear_dir}/OS/*.php
