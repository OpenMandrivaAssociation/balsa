%define enable_gpgme 0
%{?_with_gpgme: %global enable_gpgme 1}
%define title Balsa
%define summary Graphical Mail Client

Summary:	%summary
Name:		balsa
Version:	2.4.7
Release:	%mkrel 2
License:	GPLv2+
Group:		Networking/Mail

Source0:	http://pawsa.fedorapeople.org/balsa/%{name}-%{version}.tar.bz2

URL:		http://pawsa.fedorapeople.org/balsa
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	aspell-devel >= 0.50
BuildRequires:	libesmtp-devel
BuildRequires:	libgnomeprintui-devel >= 2.1.7
BuildRequires:	libgnomeui2-devel
BuildRequires:	gnome-doc-utils
# in balsa, gtkhtml 3.x is preferred over 2.x
#BuildRequires:	gtkhtml-3.14-devel
#BuildRequires:	gtkhtml2-devel
BuildRequires:	libwebkitgtk-devel
BuildRequires:	libltdl-devel
BuildRequires:	pcre-devel
BuildRequires:	scrollkeeper
BuildRequires:	sendmail-command
BuildRequires:	imagemagick
BuildRequires:	libldap-devel
BuildRequires:	intltool
BuildRequires:	libltdl-devel
BuildRequires:	libgmime-devel >= 2.4.0
BuildRequires:	krb-devel
BuildRequires:	libnotify-devel
BuildRequires:	gtkspell-devel
BuildRequires:	unique-devel
BuildRequires:	libnm-glib-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	gtksourceview-devel

%if %enable_gpgme
BuildRequires:	gpgme-devel >= 0.4.2
%endif

Requires(post):		scrollkeeper >= 0.3
Requires(postun):	scrollkeeper >= 0.3

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

%description
Balsa is an e-mail reader.

This client is part of the GNOME desktop environment. It supports local
mailboxes, POP3 and IMAP.

*** Build options: ***
--with gpgme		Build with gpgme/GnuPG support

%prep
%setup -q
#autoreconf -fi

%build
%configure2_5x	\
	--with-unique \
	--with-gss=yes \
%if %enable_gpgme
	--with-gpgme \
%endif
	--with-ssl \
	--with-ldap=yes \
	--with-gtkspell \
	--with-canberra \
	--with-html-widget=webkit \
	--with-gtksourceview

make

%install
rm -rf %{buildroot}
%makeinstall_std GTK_UPDATE_ICON_CACHE="/usr/bin/gtk-update-icon-cache --ignore-theme-index"

# Icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 644 -D	gnome-balsa2.png %{buildroot}/%{_liconsdir}/%{name}.png
convert -geometry 32x32 gnome-balsa2.png %{buildroot}/%{_iconsdir}/%{name}.png
convert -geometry 16x16 gnome-balsa2.png %{buildroot}/%{_miconsdir}/%{name}.png

%find_lang %{name} --with-gnome

for i in %{buildroot}%{_datadir}/gnome/help/%{name}/*; do
  touch $i/%{name}.html
done

%clean
rm -fr %{buildroot}

%post
%update_scrollkeeper
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html
%{update_desktop_database}

%if %mdkversion>200900

%postun
%{clean_scrollkeeper}
%{clean_desktop_database}
%endif

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING ChangeLog NEWS TODO
%config(noreplace) %{_sysconfdir}/sound/events/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/omf/*
%{_datadir}/sounds/*
%{_mandir}/*/*
%ghost %{_datadir}/gnome/help/%{name}/*/%{name}.html

%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/48x48/mimetypes/*.png

