Summary:	Client for Dynamic DNS Services
Summary(pl):	Klient dla serwisów dynamicznego DNS
Name:		ez-ipupdate
Version:	3.0.11b8
Release:	1
Group:		Networking
License:	GPL
Source0:	http://www.gusnet.cx/proj/ez-ipupdate/dist/%{name}-%{version}.tar.gz
# Source0-md5:	000211add4c4845ffa4211841bff4fb0
Source1:	%{name}.init
URL:		http://www.gusnet.cx/proj/ez-ipupdate/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	perl-base
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ez-ipupdate is a small utility for updating your host name for any of
the dynamic DNS service offered at:
 - http://www.ez-ip.net/
 - http://www.justlinux.com/
 - http://www.dhs.org/
 - http://www.dyndns.org/
 - http://www.ods.org/
 - http://gnudip.cheapnet.net/ (GNUDip)
 - http://www.dyn.ca/ (GNUDip)
 - http://www.tzo.com/
 - http://www.easydns.com/
 - http://www.dyns.cx/
 - http://www.hn.org/
 - http://www.zoneedit.com/

It is pure C and works on Linux, *BSD and Solaris.

Don't forget to create your own config file (in
/etc/ez-ipupdate.conf). You can find some example in
/usr/share/doc/%{name}-%{version}.

%description -l pl
ez-ipupdate to ma³e narzêdzie do uaktualniania nazwy hosta w dowolnym
serwisie dynamicznego DNS spo¶ród:
 - http://www.ez-ip.net/
 - http://www.justlinux.com/
 - http://www.dhs.org/
 - http://www.dyndns.org/
 - http://www.ods.org/
 - http://gnudip.cheapnet.net/ (GNUDip)
 - http://www.dyn.ca/ (GNUDip)
 - http://www.tzo.com/
 - http://www.easydns.com/
 - http://www.dyns.cx/
 - http://www.hn.org/
 - http://www.zoneedit.com/

Jest napisane w czystym C i dzia³a na Linuksie, *BSD oraz Solarisie.

Nie nale¿y zapomnieæ o utworzeniu w³asnego pliku konfiguracyjnego
(/etc/ez-ipupdate.conf). Przyk³ad mo¿na znale¼æ w katalogu
/usr/share/doc/%{name}-%{version}.

%prep
%setup -q

%build
install %{_datadir}/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%{__perl} -pi -e "s|\%{_prefix}\/local\/bin|\%{_prefix}\/bin|" *.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart >&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop >&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README CHANGELOG *.conf
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
