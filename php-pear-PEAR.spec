%include	/usr/lib/rpm/macros.php
%define		_class		PEAR
%define		_status		stable
%define		_pearname	%{_class}

Summary:	%{_pearname} - main PHP PEAR class
Summary(pl):	%{_pearname} - podstawowa klasa dla PHP PEAR
Name:		php-pear-%{_pearname}
Version:	1.3.5
Release:	1
Epoch:		1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
# Source0-md5:	8fead7fddb93f9b3cecd740823daafd2
URL:		http://pear.php.net/package/PEAR/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	sed
Requires:	php-pear
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this is in a comment
%define		_noautoreq	'pear(../PEAR/RunTest.php)'

%description
The PEAR package contains:
- the PEAR base class
- the PEAR_Error error handling mechanism
- the PEAR installer, for creating, distributing and installing
  packages

In PEAR status of this package is: %{_status}.

%description -l pl
Pakiet PEAR zawiara:
- Podstawow± klasê PEAR
- Mechanizm obs³ugi b³êdów PEAR_Error
- PEAR installer do tworzenia, dystrybucji i instalowania pakietów

Ta klasa ma w PEAR status: %{_status}.

%package Command
Summary:	%{_pearname}-Command - main PHP PEAR class
Summary(pl):	%{_pearname}-Command - podstawowa klasa dla PHP PEAR
Group:		Development/Languages/PHP

%description Command
Command class for PEAR.

In PEAR status of this package is: %{_status}.

%description Command -l pl
Klasa Command dla PEAR-a.

Ta klasa ma w PEAR status: %{_status}.

%package Frontend_CLI
Summary:	%{_pearname}-Frontend_CLI - main PHP PEAR class
Summary(pl):	%{_pearname}-Frontend_CLI - podstawowa klasa dla PHP PEAR
Group:		Development/Languages/PHP
Requires:	php-pear-Archive_Tar
Requires:	php-pear-Console_Getopt
Obsoletes:	php-pear-devel

%description Frontend_CLI
Command Line Frontend for PEAR.

In PEAR status of this package is: %{_status}.

%description Frontend_CLI -l pl
Interfejs z linii poleceñ dla PEAR-a.

Ta klasa ma w PEAR status: %{_status}.

%package OS
Summary:	%{_pearname}-OS - main PHP PEAR class
Summary(pl):	%{_pearname}-OS - podstawowa klasa dla PHP PEAR
Group:		Development/Languages/PHP

%description OS
OS_Guess class for PEAR.

In PEAR status of this package is: %{_status}.

%description OS -l pl
Klasa OS_Guess dla PEAR-a.

Ta klasa ma w PEAR status: %{_status}.

%prep
%setup -q -c

#%build
#cd %{_pearname}-%{version}/scripts
#sed -e "s#@php_bin@#php#" pear.sh > pear.sh.tmp
#mv -f pear.sh.tmp pear.sh
#sed -e "s#@pear_version@#%{_version}#" pear.sh > pear.sh.tmp
#mv -f pear.sh.tmp pear.sh
#sed -e "s#@php_dir@#%{php_pear_dir}#" pear.sh > pear.sh.tmp
#mv -f pear.sh.tmp pear.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_pear_dir}/{%{_class}/{Command,Frontend},OS},%{_bindir}}

install %{_pearname}-%{version}/*.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}/*.dtd $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}/OS/*.php $RPM_BUILD_ROOT%{php_pear_dir}/OS
install %{_pearname}-%{version}/%{_class}/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}
install %{_pearname}-%{version}/%{_class}/Command/*.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Command
install %{_pearname}-%{version}/%{_class}/Frontend/CLI.php $RPM_BUILD_ROOT%{php_pear_dir}/%{_class}/Frontend
install %{_pearname}-%{version}/scripts/pearcmd.php $RPM_BUILD_ROOT%{php_pear_dir}
install %{_pearname}-%{version}/scripts/pear.sh $RPM_BUILD_ROOT%{_bindir}/pear

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
%{php_pear_dir}/*.dtd

%files Frontend_CLI
%defattr(644,root,root,755)
%{php_pear_dir}/%{_class}/Frontend/*.php

%files OS
%defattr(644,root,root,755)
%dir %{php_pear_dir}/OS
%{php_pear_dir}/OS/*.php
