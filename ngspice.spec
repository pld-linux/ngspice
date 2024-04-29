#
# Conditional build:
%bcond_without	shared	# ngspice shared library
%bcond_without	x11	# ngspice app

Summary:	Ngspice circuit simulator
Summary(pl.UTF-8):	Symulator obwodów Ngspice
Name:		ngspice
Version:	42
Release:	2
License:	Modified BSD, MPL v2.0, LGPL v2+, GPL v2+
Group:		Applications/Engineering
Source0:	https://downloads.sourceforge.net/ngspice/%{name}-%{version}.tar.gz
# Source0-md5:	84ab9e67127f9732639195dd63b98a5e
Source1:	%{name}.desktop
Patch0:		%{name}-am.patch
URL:		https://ngspice.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	fftw3-devel >= 3
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
%if %{with x11}
BuildRequires:	fontconfig-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXt-devel
%endif
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ngspice is a mixed-level/mixed-signal circuit simulator. Its code is
based on three open source software packages: Spice3f5, Cider1b1 and
Xspice.

%description -l pl.UTF-8
Ngspice to symulator obwodów różnych poziomów/sygnałów. Kod jest
oparty na trzech projektach o otwartych źródłach: Spice3f5, Cider1b1
oraz Xspice.

%package common
Summary:	Common data and modules for ngspice engine
Summary(pl.UTF-8):	Wspólne dane i moduły dla silnika ngspice
Group:		Libraries
Conflicts:	ngspice < 42-2

%description common
Common data and modules for ngspice engine (either application or
library).

%description common -l pl.UTF-8
Wspólne dane i moduły dla silnika ngspice (zarówno w postaci
aplikacji, jak i biblioteki).

%package libs
Summary:	Shared nspice library
Summary(pl.UTF-8):	Biblioteka współczielona ngspice
Group:		Libraries
Requires:	%{name}-data = %{version}-%{release}

%description libs
Shared nspice library.

%description libs -l pl.UTF-8
Biblioteka współczielona ngspice.

%package devel
Summary:	Header files for ngspice library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ngspice
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for ngspice library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ngspice.

%prep
%setup -q
%patch0 -p1

find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
for kind in %{?with_shared:ngshared} %{?with_x11:x} ; do
install -d build-${kind}
cd build-${kind}
../%configure \
	--disable-silent-rules \
	--enable-cider \
	--enable-openmp \
	--enable-osdi \
	--enable-xspice \
	--with-${kind} \
	$([ "${kind}" = "x" ] && echo --with-readline)

%{__make}
cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

%if %{with x11}
%{__make} -C build-x install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
%endif

%if %{with shared}
%{__make} -C build-ngshared install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libngspice.la
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -R examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with x11}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ngspice
%{_desktopdir}/ngspice.desktop
%{_mandir}/man1/ngspice.1*
%endif

%files common
%defattr(644,root,root,755)
%doc ANALYSES AUTHORS BUGS ChangeLog DEVICES FAQ NEWS README
%dir %{_libdir}/ngspice
%attr(755,root,root) %{_libdir}/ngspice/*.cm
%{_datadir}/%{name}
%{_examplesdir}/%{name}-%{version}

%if %{with shared}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libngspice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libngspice.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libngspice.so
%{_pkgconfigdir}/ngspice.pc
%{_includedir}/ngspice
%endif
