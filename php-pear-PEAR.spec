%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_pearname	%{_class}
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Name:		php-pear-%{_pearname}
Version:	0.90
Release:	4
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
URL:		http://pear.php.net/
BuildRequires:	rpm-php-pearprov
BuildRequires:	sed
Requires:	php-pear
# This is temporary empty class
Provides:	pear(stdClass)
# Temporary - this is not OK:
Provides:	pear(parent)
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
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Group:		Development/Languages/PHP
Requires:	pear(Frontend)

%description Command
Command class for PEAR.

%description -l pl Command
Klasa Command dla PEARa.

%package Frontend_CLI
Summary:	%{_class} - main php pear class
Summary(pl):	%{_class} - podstawowa klasa dla php pear
Group:		Development/Languages/PHP
Provides:	pear(Frontend)

%description Frontend_CLI
Command Line Frontend for PEAR.

%description -l pl Frontend_CLI
Interfejs z linii polece� dla PEAR-a.

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
