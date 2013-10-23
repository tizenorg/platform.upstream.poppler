%define _unpackaged_files_terminate_build 0
%define full_iconv 0

%define major 43
%define glibmajor 8
%define qt4major 4
%define cppmajor 0
%define girmajor 0.18

%define libname		libpoppler
%define libnameglib	libpoppler-glib
%define libnameqt4	libpoppler-qt4
%define libnamecpp	libpoppler-cpp
%define libnamedev	libpoppler-devel
%define libnameglibdev	libpoppler-glib-devel
%define libnameqt4dev	libpoppler-qt4-devel
%define libnamecppdev   libpoppler-cpp-devel
%define libnamegir	libpoppler-gir

Name:		poppler
Summary: 	PDF rendering library
Group:		System/Libraries
Version:	0.24.1
Release:	1
License:	GPL-2.0+
URL:		http://poppler.freedesktop.org
Source:		%{name}-%{version}.tar.gz
Source1001: libpoppler-cpp.manifest
Source1002: libpoppler-glib.manifest
Source1003: libpoppler.manifest
Source1004: poppler-tools.manifest

BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:  pkgconfig(cairo-ft) >= 1.10.0
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(cairo-svg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gobject-2.0) >= 2.18
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRequires:	curl-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(lcms2)


%description
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package tools
Summary:        PDF Rendering Library Tools
License:        GPL-2.0
Group:          Productivity/Publishing/PDF
Requires:       %{libname} >= %{version}
# last version in openSUSE 11.1/SLE11
Provides:       poppler-tools = %{version}
Obsoletes:	xpdf-tools < 3.02-10mdv
Provides:	xpdf-tools
Obsoletes:	pdftohtml
Provides:	pdftohtml

%description tools
Poppler is a PDF rendering library, forked from the xpdf PDF viewer
developed by Derek Noonburg of Glyph and Cog, LLC.

%package -n %{libname}
Summary:	PDF rendering library
License:        GPL-2.0
Group:          System/Libraries
Provides:	poppler = %{version}
Conflicts:	%{_lib}poppler12
#Suggests:	poppler-data

%description -n %{libname}
Poppler is a PDF rendering library based on the xpdf-3.0 code base.

%package -n %{libnamedev}
Summary:	Development files for %{name}
License:        GPL-2.0
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{libname}-devel

%description -n %{libnamedev}
Development files for %{name}

%if %{full_iconv}
%package -n %{libnamecpp}
Summary:	PDF rendering library - C++ backend
Group:          System/Libraries
Provides:	poppler-cpp = %{version}

%description -n %{libnamecpp}
Poppler is a PDF rendering library based on the xpdf-3.0 code base.
This is the C++ backend version.
%endif

%package -n %{libnameglib}
Summary:	PDF rendering library - glib binding
License:        GPL-2.0+
Group:          System/Libraries
Provides:       poppler-glib = %{version}
Conflicts:	%{libname} < %{version}-%{release}

%description -n %{libnameglib}
Poppler is a PDF rendering library based on the xpdf-3.0 code base.

%package -n %{libnameglibdev}
Summary:	Development files for %{name}'s glib binding
License:        GPL-2.0
Group:		Development/C++
Provides:	%{name}-glib-devel = %{version}-%{release}
Requires:	%{libnameglib} = %{version}
Requires:	%{libnamedev} = %{version}
Conflicts:	%{libnamedev} < %{version}-%{release}
Obsoletes:	%{libnameglib}-devel

%description -n %{libnameglibdev}
Development files for %{name}'s glib binding.

%if %{full_iconv}
%package -n %{libnamecppdev}
Summary:	Development files for %{name}-cpp
Group:		Development/C++
Provides:	%{name}-cpp-devel = %{version}-%{release}
Requires:	%{libnamecpp} = %{version}
Requires:	%{libnamedev} = %{version}

%description -n %{libnamecppdev}
Development files for %{name}-cpp.
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .

%build
%configure \
    --prefix=/usr --localstatedir=/opt/var --sysconfdir=/opt/etc --datarootdir=/usr/share \
    --enable-shared --disable-static \
    --enable-libjpeg --disable-libopenjpeg --enable-libtiff \
    --enable-largefile \
    --enable-zlib --disable-libcurl \
    --enable-libpng \
    --enable-cairo-output \
    --enable-splash-output \
    --enable-poppler-glib \
%if %{full_iconv}
    --disable-poppler-cpp \
%endif
    --enable-introspection=auto \
    --disable-gtk-doc --disable-gtk-doc-html --disable-gtk-doc-pdf \
    --disable-poppler-qt4 --disable-poppler-qt5 \
    --disable-gtk-test \
    --enable-xpdf-headers \
    --enable-compile-warnings=yes \
    --enable-cms=lcms2 --without-x --with-font-configuration=fontconfig

make %{?_smp_mflags}

%install
%makeinstall
%{__cp} -a config.h %{buildroot}%{_includedir}/poppler/

rm %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}/usr/share/license
cp %{_builddir}/%{buildsubdir}/COPYING %{buildroot}/usr/share/license/%{libname}
%if %{full_iconv}
cp %{_builddir}/%{buildsubdir}/COPYING %{buildroot}/usr/share/license/%{libnamecpp}
%endif
cp %{_builddir}/%{buildsubdir}/COPYING %{buildroot}/usr/share/license/%{libnameglib}
cp %{_builddir}/%{buildsubdir}/COPYING %{buildroot}/usr/share/license/poppler-tools


%post -n libpoppler -p /sbin/ldconfig

%post -n libpoppler-glib -p /sbin/ldconfig

%postun -n libpoppler -p /sbin/ldconfig

%postun -n libpoppler-glib -p /sbin/ldconfig

%files -n poppler-tools
%manifest poppler-tools.manifest
/usr/share/license/poppler-tools
%exclude %{_bindir}/pdfdetach
%exclude %{_bindir}/pdffonts
%exclude %{_bindir}/pdfimages
%{_bindir}/pdfinfo
%{_bindir}/pdfseparate
%exclude %{_bindir}/pdftocairo
%exclude %{_bindir}/pdftohtml
%{_bindir}/pdftoppm
%{_bindir}/pdftops
%exclude %{_bindir}/pdftotext
%{_bindir}/pdfunite
%exclude %{_mandir}/man1/*

%files -n %{libname}
%manifest libpoppler.manifest
/usr/share/license/%{libname}
%{_libdir}/libpoppler.so.%{major}*

%files -n %{libnamedev}
%{_libdir}/libpoppler.so
%dir %{_includedir}/poppler/
%{_includedir}/poppler/config.h
%{_includedir}/poppler/[A-Z]*
%{_includedir}/poppler/fofi
%{_includedir}/poppler/goo
%{_includedir}/poppler/splash
%{_includedir}/poppler/poppler-config.h
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/pkgconfig/poppler.pc
%exclude %{_datadir}/gtk-doc/html/poppler/*

%files -n %{libnameglib}
%manifest libpoppler-glib.manifest
/usr/share/license/%{libnameglib}
%{_libdir}/libpoppler-glib.so.%{glibmajor}*

%files -n %{libnameglibdev}
%{_libdir}/libpoppler-glib.so
%{_libdir}/pkgconfig/poppler-glib.pc
%{_includedir}/poppler/glib/*.h

%if %{full_iconv}
%files -n %{libnamecpp}
%manifest libpoppler-cpp.manifest
/usr/share/license/%{libnamecpp}
%{_libdir}/libpoppler-cpp.so.%{cppmajor}*

%files -n %{libnamecppdev}
%{_libdir}/libpoppler-cpp.so
%{_libdir}/pkgconfig/poppler-cpp.pc
%{_includedir}/poppler/cpp
%endif


