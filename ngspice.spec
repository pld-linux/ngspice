# Conditional build:
%bcond_without	shared	# build as shared library

Summary:	Ngspice circuit simulator
Summary(pl.UTF-8):	Ngspice symulator obwodów
Name:		ngspice
Version:	42
Release:	1
License:	GPL
Group:		Applications
Source0:	https://sourceforge.net/projects/ngspice/files/ng-spice-rework/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	84ab9e67127f9732639195dd63b98a5e
Source1:	%{name}.desktop
URL:		http://ngspice.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ngspice is a mixed-level/mixed-signal circuit simulator. Its code is
based on three open source software packages: Spice3f5, Cider1b1 and
Xspice.

%description -l pl.UTF-8
Ngspice is a mixed-level/mixed-signal circuit simulator. Its code is
based on three open source software packages: Spice3f5, Cider1b1 and
Xspice.

%package devel
Summary:	Header files for ngspice library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ngspice
License:	GPL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ngspice library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ngspice.

%prep
%setup -q
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build

%configure \
	--disable-silent-rules \
	--enable-xspice \
	--enable-cider \
	--enable-openmp \
%if %{with shared}
	--with-ngshared
%else
	--enable-xgraph \
	--with-x \
	--with-readline=yes
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_desktopdir}

%if %{without shared}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
%endif
cp -R examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with shared}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc ANALYSES AUTHORS ChangeLog NEWS README
%dir %{_libdir}/ngspice
%attr(755,root,root) %{_libdir}/ngspice/*.cm
%{_examplesdir}/%{name}-%{version}
%{_datadir}/%{name}

%if %{without shared}
%attr(755,root,root) %{_bindir}/ngspice
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/ng*1*
%else
%attr(755,root,root) %{_libdir}/libngspice.so.0.0.*
%attr(755,root,root) %ghost %{_libdir}/libngspice.so.0
%endif

%files devel
%defattr(644,root,root,755)
%if %{with shared}
%{_libdir}/libngspice.so
%{_libdir}/libngspice.la
%{_pkgconfigdir}/*.pc
%{_includedir}/ngspice
%endif
