Summary:	Disk Management Service
Name:		udisks2
Version:	2.0.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://udisks.freedesktop.org/releases/udisks-%{version}.tar.bz2
# Source0-md5:	c9e3e2031e775d6d7d935efc85c272bb
Patch0:		%{name}-udf.patch
URL:		http://www.freedesktop.org/wiki/Software/udisks
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libatasmart-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	udev-glib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/udisks2

%description
udisks provides a daemon, D-Bus API and command line tools for
managing disks and storage devices. This package is for the udisks 2.x
series.

%package libs
Summary:	udisks2 library
License:	LGPL v2+
Group:		Libraries

%description libs
This package contains udisks2 library, which provides access to the
udisks daemon.

%package devel
Summary:	Header files for udisks2 library
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for udisks2 library.

%package apidocs
Summary:	udisks2 API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for udisks2 library.

%prep
%setup -qn udisks-%{version}
%patch0 -p1

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}	\
	--with-udevdir=/usr/lib/udev	\
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS HACKING NEWS README
%attr(755,root,root) %{_bindir}/udisksctl
%dir %{_prefix}/lib/udisks2
%attr(755,root,root) %{_prefix}/lib/udisks2/udisksd
%attr(755,root,root) %{_sbindir}/umount.udisks2
/etc/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{systemdunitdir}/udisks2.service
/usr/lib/udev/rules.d/80-udisks2.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service
%{_datadir}/polkit-1/actions/org.freedesktop.udisks2.policy
%{_mandir}/man1/udisksctl.1*
%{_mandir}/man8/udisks.8*
%{_mandir}/man8/udisksd.8*
%attr(700,root,root) /var/lib/udisks2

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libudisks2.so.?
%attr(755,root,root) %{_libdir}/libudisks2.so.*.*.*
%{_libdir}/girepository-1.0/UDisks-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudisks2.so
%{_includedir}/udisks2
%{_pkgconfigdir}/udisks2.pc
%{_datadir}/gir-1.0/UDisks-2.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/udisks2

