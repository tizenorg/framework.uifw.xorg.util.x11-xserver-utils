Summary: X server utilities
Name: xorg-x11-xserver-utils
Version: 7.5
Release: 2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source0: %{name}-%{version}.tar.gz
Source1: xmodmap.service
Source2: xrdb.service
Source3: xset-autorepeat-lb.service
Source1001: packaging/xorg-x11-xserver-utils.manifest 

BuildRequires: pkgconfig(xorg-macros)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xaw7)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xmuu)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xxf86vm)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(inputproto)
BuildRequires: xbitmaps

%define DEF_SUBDIRS iceauth rgb sessreg xcmsdb xgamma xhost xmodmap xrandr xrdb xrefresh xset xsetmode xsetpointer xsetroot xstdcmap xvidtune

Provides: %{DEF_SUBDIRS}

%description
 An X client is a program that interfaces with an X server (almost always via
 the X libraries), and thus with some input and output hardware like a
 graphics card, monitor, keyboard, and pointing device (such as a mouse).
 .
 This package provides a miscellaneous assortment of X Server utilities
 that ship with the X Window System, including:
  - iceauth, a tool for manipulating ICE protocol authorization records;
  - rgb;
  - sessreg, a simple program for managing utmp/wtmp entries;
  - xcmsdb, a device color characteristic utility for the X Color Management
    System;
  - xgamma, a tool for querying and setting a monitor's gamma correction;
  - xhost, a very dangerous program that you should never use;
  - xmodmap, a utility for modifying keymaps and pointer button mappings in X;
  - xrandr, a command-line interface to the RandR extension;
  - xrdb, a tool to manage the X server resource database;
  - xrefresh, a tool that forces a redraw of the X screen;
  - xset, a tool for setting miscellaneous X server parameters;
  - xsetmode and xsetpointer, tools for handling X Input devices;
  - xsetroot, a tool for tailoring the appearance of the root window;
  - xstdcmap, a utility to selectively define standard colormap properties;
  - xvidtune, a tool for customizing X server modelines for your monitor.

%package lb
Summary:        Device-specific files for Lunchbox
Group:          User Interface/X
Requires:       %{name} = %{version}

%description lb
This package provides files for the X server utilities package that are
specific to Lunchbox devices.


%prep
%setup -q

%build
cp %{SOURCE1001} .
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
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

mkdir -p %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/systemd/user/
install -m 0644 %SOURCE2 %{buildroot}%{_libdir}/systemd/user/
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/user/
ln -s ../xmodmap.service %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants/xmodmap.service
ln -s ../xrdb.service %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants/xrdb.service
ln -s ../xset-autorepeat-lb.service %{buildroot}%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-lb.service


%docs_package

%files
%manifest xorg-x11-xserver-utils.manifest
%{_bindir}/*
%{_sysconfdir}/X11/app-defaults/*
%{_libdir}/systemd/user/xmodmap.service
%{_libdir}/systemd/user/xrdb.service
%{_libdir}/systemd/user/core-efl.target.wants/xmodmap.service
%{_libdir}/systemd/user/core-efl.target.wants/xrdb.service
%{_datadir}/X11/rgb.txt

%files lb
%manifest xorg-x11-xserver-utils.manifest
%{_libdir}/systemd/user/xset-autorepeat-lb.service
%{_libdir}/systemd/user/core-efl.target.wants/xset-autorepeat-lb.service
