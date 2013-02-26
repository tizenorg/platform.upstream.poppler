%define poppler_data_version 0.2.1
%define full_iconv 0
%bcond_with introspection

Name:           poppler
Version:        0.22.1
Release:        1
Url:            http://poppler.freedesktop.org/
Summary:        PDF Rendering Library
License:        GPL-2.0+
Group:          System/Libraries
Source:         http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
%if %{with introspection} 
BuildRequires:  gobject-introspection-devel
%endif
BuildRequires:  gettext-devel
BuildRequires:  libjpeg8-devel
BuildRequires:  libtiff-devel
BuildRequires:  update-desktop-files
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(cairo) >= 1.10.0
BuildRequires:  pkgconfig(cairo-ft) >= 1.10.0
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(cairo-svg)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gobject-2.0) >= 2.18
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libpng)

%description
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package -n libpoppler
Summary:        PDF Rendering Library
License:        GPL-2.0
Group:          System/Libraries

%description -n libpoppler
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%if %{full_iconv} 
%package -n libpoppler-cpp
Summary:        PDF Rendering Library
License:        GPL-2.0
Group:          System/Libraries

%description -n libpoppler-cpp
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.
%endif 

%package -n libpoppler-glib
Summary:        PDF Rendering Library - GLib Wrapper
License:        GPL-2.0+
Group:          System/Libraries
Requires:       libpoppler >= %{version}

%description -n libpoppler-glib
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package -n typelib-Poppler
Summary:        PDF Rendering Library - Introspection bindings
License:        GPL-2.0+
Group:          System/Libraries

%description -n typelib-Poppler
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

This package provides the GObject Introspection bindings for Poppler.


%package tools
Summary:        PDF Rendering Library Tools
License:        GPL-2.0
Group:          Development/Tools
Requires:       libpoppler >= %{version}

%description tools
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package -n libpoppler-devel
Summary:        PDF rendering library
License:        GPL-2.0
Group:          Development/Libraries
Requires:       libpoppler = %{version}
Requires:       libstdc++-devel

%description -n libpoppler-devel
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package -n libpoppler-glib-devel
Summary:        PDF rendering library - GLib Wrapper
License:        GPL-2.0
Group:          Development/Libraries
Requires:       libpoppler-glib = %{version}
%if %{with introspection} 
Requires:       typelib-Poppler = %{version}
%endif

%description -n libpoppler-glib-devel
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%prep
%setup -q -n poppler-%{version}

%build
autoreconf -fi
%configure\
	--enable-xpdf-headers\
	--disable-static\
	--enable-shared\
	--enable-zlib \
        --disable-gtk-test
make %{?_smp_mflags}

%install
%make_install

%post -n libpoppler -p /sbin/ldconfig

%post -n libpoppler-glib -p /sbin/ldconfig

%postun -n libpoppler -p /sbin/ldconfig

%postun -n libpoppler-glib -p /sbin/ldconfig

%if %{full_iconv}
%post -n libpoppler-cpp -p /sbin/ldconfig

%postun -n libpoppler-cpp -p /sbin/ldconfig
%endif 

%files -n libpoppler
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README README-XPDF TODO
%{_libdir}/libpoppler.so.*

%files -n libpoppler-glib
%defattr (-, root, root)
%{_libdir}/libpoppler-glib.so.*

%if %{with introspection} 
%files -n typelib-Poppler
%defattr (-, root, root)
%{_libdir}/girepository-1.0/Poppler-0.18.typelib
%endif

%files tools
%defattr (-, root, root)
%doc COPYING
%{_bindir}/*
%doc %{_mandir}/man1/*.*

%if %{full_iconv}
%files -n libpoppler-cpp
%defattr(-, root, root)
%{_libdir}/libpoppler-cpp.so.*
%endif 

%files -n libpoppler-devel
%defattr (-, root, root)
%{_includedir}/poppler
%exclude %{_includedir}/poppler/glib
%{_libdir}/libpoppler.so
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%if %{full_iconv}
%{_libdir}/libpoppler-cpp.so
%{_libdir}/pkgconfig/poppler-cpp.pc
%endif
%{_libdir}/pkgconfig/poppler-splash.pc
%files -n libpoppler-glib-devel
%defattr (-, root, root)
%{_includedir}/poppler/glib
%{_libdir}/libpoppler-glib.so
%{_libdir}/pkgconfig/poppler-glib.pc
%if %{with introspection} 
%{_datadir}/gir-1.0/Poppler-0.18.gir
%endif
%doc %{_datadir}/gtk-doc/html/poppler/
