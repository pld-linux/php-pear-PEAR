%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		stable

%define		_pearname	%{_class}
Summary:	%{_pearname} - main php pear class
Summary(pl):	%{_pearname} - podstawowa klasa dla php pear
Name:		php-pear-%{_pearname}
Version:	1.0.1
Release:	1
Epoch:		1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
URL:		http://pear.php.net/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	sed
Requires:	php-pear
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(/usr/src/redhat/RPMS/i386/PEAR)'

%description
The PEAR package contains:
- the PEAR base class
- the PEAR_Error error handling mechanism
- the PEAR installer, for creating, distributing and installing
  packages

This class has in PEAR status: %{_status}

%description -l pl
Pakiet PEAR zawiara:
- Postawow± klasê PEAR
- Mechanizm obs³ugi b³êdów PEAR_Error
- PEAR installer do tworzenia, dystrybucji i instalowania pakietów

Ta klasa ma w PEAR status: %{_status}

%package Command
Summary:	%{_pearname}-Command - main php pear class
Summary(pl):	%{_pearname}-Command - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description Command
Command class for PEAR.

This class has in PEAR status: %{_status}

%description -l pl Command
Klasa Command dla PEARa.

Ta klasa ma w PEAR status: %{_status}

%package Frontend_CLI
Summary:	%{_pearname}-Frontend_CLI - main php pear class
Summary(pl):	%{_pearname}-Frontend_CLI - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description Frontend_CLI
Command Line Frontend for PEAR.

This class has in PEAR status: %{_status}

%description -l pl Frontend_CLI
Interfejs z linii poleceñ dla PEAR-a.

Ta klasa ma w PEAR status: %{_status}

%package OS
Summary:	%{_pearname}-OS - main php pear class
Summary(pl):	%{_pearname}-OS - podstawowa klasa dla php pear
Group:		Development/Languages/PHP

%description OS
OS_Guess class for PEAR.

This class has in PEAR status: %{_status}

%description -l pl OS
Klasa OS_Guess dla PEARa.

Ta klasa ma w PEAR status: %{_status}

%prep
%setup -q -c

%build
cd %{_pearname}-%{version}/scripts
sed -e "s/@prefix@/\/usr/" pear.in > pear.in.tmp
mv -f pear.in.tmp pear.in
sed -e "s/@pear_version@/%{version}/" pear.in > pear.in.tmp
mv -f pear.in.tmp pear.in

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_pear_dir}/{%{_class}/{Command,Frontend},OS},%{_bindir}}

install %{_pearname}-%{version}/*.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}/OS/*.php $RPM_BUILD_ROOT%{php_pear_dir}/OS
install %{_pearname}-%{version}/%{_class}/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}
install %{_pearname}-%{version}/%{_class}/Command/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Command
install %{_pearname}-%{version}/%{_class}/Frontend/CLI.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Frontend
install %{_pearname}-%{version}/scripts/pear.in $RPM_BUILD_ROOT%{_bindir}/pear

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{php_pear_dir}
%{php_pear_dir}/*.php

%files Command
%defattr(644,root,root,755)
%dir %{php_pear_dir}/%{_class}/Command
%dir %{php_pear_dir}/%{_class}/Frontend
%attr(755,root,root) %{_bindir}/pear
%{php_pear_dir}/%{_class}/*.php
%{php_pear_dir}/%{_class}/Command/*.php

%files Frontend_CLI
%defattr(644,root,root,755)
%{php_pear_dir}/%{_class}/Frontend/*.php

%files OS
%defattr(644,root,root,755)
%dir %{php_pear_dir}/OS
%{php_pear_dir}/OS/*.php
