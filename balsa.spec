%define enable_gpgme 0

Summary:	Graphical Mail Client
Name:		balsa
Version:	2.4.11
Release:	1
License:	GPLv2+
Group:		Networking/Mail
URL:		http://pawsa.fedorapeople.org/balsa
Source0:	http://pawsa.fedorapeople.org/balsa/%{name}-%{version}.tar.bz2

BuildRequires:	gnome-doc-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	sendmail-command
BuildRequires:	aspell-devel >= 0.50
BuildRequires:	krb5-devel
BuildRequires:	libldap-devel
BuildRequires:	libesmtp-devel
BuildRequires:	libltdl-devel
# in balsa, gtkhtml 3.x is preferred over 2.x
#BuildRequires:	gtkhtml-3.14-devel
#BuildRequires:	gtkhtml2-devel
BuildRequires:	pkgconfig(gmime-2.6)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(gtkspell-2.0)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libgnomeprintui-2.2)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(webkit-1.0)
%if %enable_gpgme
BuildRequires:	gpgme-devel >= 0.4.2
%endif

%description
Balsa is an e-mail reader.

This client is part of the GNOME desktop environment. It supports local
mailboxes, POP3 and IMAP.

*** Build options: ***
--with gpgme		Build with gpgme/GnuPG support

%prep
%setup -q

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
	--with-gtksourceview \
	--disable-scrollkeeper

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

%post
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html

%files -f %{name}.lang
%doc README COPYING ChangeLog NEWS TODO
%config(noreplace) %{_sysconfdir}/sound/events/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/omf/*
%{_datadir}/sounds/*
%{_mandir}/man1/*
%ghost %{_datadir}/gnome/help/%{name}/*/%{name}.html

%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/48x48/mimetypes/*.png

