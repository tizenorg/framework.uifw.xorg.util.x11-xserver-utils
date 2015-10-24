%define _unpackaged_files_terminate_build 0

%define pkgname server-utils
# doesn't work yet, needs more nickle bindings
%define with_xkeystone 0

Summary: X.Org X11 X server utilities
Name: xorg-x11-server-utils
Version: 7.5.2
Release: 12
License: MIT
Group: User Interface/X
URL: http://www.x.org
Source0: %{name}-%{version}.tar.gz
Source3: xset-autorepeat-lb.service
Source4: xset-autorepeat-i386.service

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
BuildRequires: pkgconfig(xt)
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

%define DEF_SUBDIRS xkill xrandr xrdb xset
Provides: %{DEF_SUBDIRS}
Provides: x11-xserver-utils = %{version}

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

%package lb
Summary:        Device-specific files for Lunchbox
Group:          User Interface/X
Requires:       %{name} = %{version}
Provides:       x11-xserver-utils-lb = %{version}

%description lb
This package provides files for the X server utilities package that are
specific to Lunchbox devices.

%package i386
Summary:        Device-specific files for i386
Group:          User Interface/X
Requires:       %{name} = %{version}
Provides:       x11-xserver-utils-i386 = %{version}

%description i386
This package provides files for the X server utilities package that are
specific to i386/emulator devices.


%prep
%setup -q

%build
# Build all apps
export CFLAGS+=" -D_GNU_SOURCE"
{
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        %reconfigure \
            --disable-xprint \
            RSH=rsh \
            MANCONF="/etc/manpath.config"
        make
        popd
    done
}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

mkdir -p %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/user/
install -m 0644 %SOURCE4 %{buildroot}%{_libdir}/systemd/user/
ln -s ../xset-autorepeat-lb.service %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-lb.service
ln -s ../xset-autorepeat-i386.service %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-i386.service

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%manifest xorg-x11-server-utils.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}
%doc
%{_bindir}/xkill
%{_bindir}/xrandr
%{_bindir}/xrdb
%{_bindir}/xset

%if %{with_xkeystone}
%files -n xkeystone
%defattr(-,root,root,-)
%{_bindir}/xkeystone
%endif

%files lb
%{_libdir}/systemd/user/xset-autorepeat-lb.service
%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-lb.service

%files i386
%{_libdir}/systemd/user/xset-autorepeat-i386.service
%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-i386.service
