%define _unpackaged_files_terminate_build 0 

%define pkgname server-utils
# doesn't work yet, needs more nickle bindings
%define with_xkeystone 0

Summary: X.Org X11 X server utilities
Name: xorg-x11-server-utils
Version: 7.5
Release: 12
License: MIT
Group: User Interface/X
URL: http://www.x.org
Source: %{name}-%{version}.tar.gz

# NOTE: Each upstream tarball has its own "PatchN" section, taken from
# multiplying the "SourceN" line times 100.  Please keep them in this
# order.  Also, please keep each patch specific to a single upstream tarball,
# so that they don't have to be split in half when submitting upstream.
#
# iceauth section
#Patch0: 

BuildRequires: xorg-x11-xutils-dev
#BuildRequires: pkgconfig(xorg-macros)
BuildRequires: pkgconfig(xmu) pkgconfig(xext) pkgconfig(xrandr)
BuildRequires: pkgconfig(xxf86vm) pkgconfig(xrender) pkgconfig(xi)
BuildRequires: pkgconfig(xt) pkgconfig(xpm)
# xsetroot requires xbitmaps-devel (which was renamed now)
BuildRequires: xorg-x11-xbitmaps
# xsetroot
BuildRequires: libXcursor-devel
# xinput
BuildRequires: libXinerama-devel

# xrdb, sigh
#Requires: mcpp
# older -apps had xinput and xkill, moved them here because they're
# a) universally useful and b) don't require Xaw
#Conflicts: xorg-x11-apps < 7.6-4

%define DEF_SUBDIRS iceauth rgb sessreg xgamma xhost xkill xmodmap xrandr xrdb xrefresh xset xsetmode xsetpointer xsetroot xstdcmap
Provides: %{DEF_SUBDIRS}

%description
A collection of utilities used to tweak and query the runtime configuration
of the X server.

%if %{with_xkeystone}
%package -n xkeystone
Summary: X display keystone correction
Group: User Interface/X
Requires: nickle

%description -n xkeystone
Utility to perform keystone adjustments on X screens.
%endif

%prep
%setup -q

%build
# Build all apps
{
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        %configure \
            --disable-xprint \
            RSH=rsh \
            MANCONF="/etc/manpath.config"
	make
        popd
    done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/iceauth
%{_bindir}/sessreg
%{_bindir}/showrgb
%{_bindir}/xgamma
%{_bindir}/xhost
%{_bindir}/xkill
%{_bindir}/xmodmap
%{_bindir}/xrandr
%{_bindir}/xrdb
%{_bindir}/xrefresh
%{_bindir}/xset
%{_bindir}/xsetmode
%{_bindir}/xsetpointer
%{_bindir}/xsetroot
%{_bindir}/xstdcmap
%{_datadir}/X11/rgb.txt
#%{_mandir}/man1/iceauth.1*
#%{_mandir}/man1/sessreg.1*
#%{_mandir}/man1/showrgb.1*
#%{_mandir}/man1/xgamma.1*
#%{_mandir}/man1/xhost.1*
#%{_mandir}/man1/xinput.1*
#%{_mandir}/man1/xkill.1*
#%{_mandir}/man1/xmodmap.1*
#%{_mandir}/man1/xrandr.1*
#%{_mandir}/man1/xrdb.1*
#%{_mandir}/man1/xrefresh.1*
#%{_mandir}/man1/xset.1*
#%{_mandir}/man1/xsetmode.1*
#%{_mandir}/man1/xsetpointer.1*
#%{_mandir}/man1/xsetroot.1*
#%{_mandir}/man1/xstdcmap.1*

%if %{with_xkeystone}
%files -n xkeystone
%defattr(-,root,root,-)
%{_bindir}/xkeystone
%endif
