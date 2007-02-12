Summary:	PHP/MySQL web front-end for Nagios 2.x
Summary(pl.UTF-8):	Oparty na PHP/MySQL interfejs WWW dla Nagiosa 2.x
Name:		nagios-nag2web
Version:	1.5.3
Release:	0.4
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/nag2web/nag2web-%{version}.tar.gz
# Source0-md5:	7aab78eb1d1547914166ba42f5e10660
Source1:	nag2web-apache.conf
Patch0:		nag2web-fixes.patch
Patch1:		nag2web-config.patch
URL:		http://www.nag2web.de/
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		nag2web
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
A PHP/MySQL web front-end for Nagios 2.x setup. With the ability to
add/remove/edit the config items. The web front-end for Nagios has the
ability to test the config. We want to build a simple possibility to
find and show all the features in Nagios.

%description -l pl.UTF-8
Oparty na PHP/MySQL interfejs WWW do konfiguracji Nagiosa 2.x. Ma
możliwość dodawania/usuwania/modyfikowania elementów konfiguracji oraz
testowania konfiguracji. Celem projektu jest umożliwienie łatwego
znalezienia i pokazania wszystkich możliwości Nagiosa.

%prep
%setup -q -n nag2web-%{version}
mv dbconfig.{php,inc}
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
cp -a *.php *.css $RPM_BUILD_ROOT%{_appdir}
cp -a help images lang $RPM_BUILD_ROOT%{_appdir}

install dbconfig.inc $RPM_BUILD_ROOT%{_sysconfdir}/dbconfig.php
ln -s %{_sysconfdir}/dbconfig.php $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
%banner %{name} -e <<'EOF'
Quickstart:
$ mysqladmin create nag2web
$ mysql -e "GRANT SELECT, INSERT, UPDATE, DELETE ON nag2web.* TO 'nag2web'@'localhost' IDENTIFIED BY 'nag2web'"
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_register apache %{_webapp}

%triggerin -- apache1 < 1.3.37-3, apache1-base >= 1.3.37-3
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL
%lang(de) %doc INSTALL-DE
%doc sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
