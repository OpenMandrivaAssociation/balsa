%define enable_gpgme 0
%{?_with_gpgme: %global enable_gpgme 1}
%define title Balsa
%define summary Balsa Mail Client

Summary:	%summary
Name:		balsa
Version:        2.3.19
Release:        %mkrel 1
License:	GPL
Group:		Networking/Mail

Source0:	http://balsa.gnome.org/%{name}-%{version}.tar.bz2

URL:		http://www.balsa.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	autoconf2.5
BuildRequires:  aspell-devel >= 0.50
BuildRequires:	libesmtp-devel
BuildRequires:  libgnomeprintui-devel >= 2.1.7
BuildRequires:  libgnomeui2-devel
# in balsa, gtkhtml 3.x is preferred over 2.x
BuildRequires:	libgtkhtml-3.8-devel
#BuildRequires:	gtkhtml2-devel
BuildRequires:	libltdl-devel
BuildRequires:	pcre-devel
BuildRequires:  scrollkeeper
BuildRequires:	sendmail-command
BuildRequires:	ImageMagick
BuildRequires:	libldap-devel
BuildRequires:	intltool
BuildRequires:  libltdl-devel
BuildRequires:	libgmime-devel >= 2.1.7
BuildRequires:	krb-devel
BuildRequires:  automake1.9

%if %enable_gpgme
BuildRequires:	gpgme-devel >= 0.4.2
%endif

Requires(post):         scrollkeeper >= 0.3
Requires(postun):         scrollkeeper >= 0.3

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Balsa is an e-mail reader.

This client is part of the GNOME desktop environment. It supports local
mailboxes, POP3 and IMAP.
 
*** Build options: ***
--with gpgme              Build with gpgme/GnuPG support

%prep
%setup -q

%build
%configure2_5x	\
	--with-gtkhtml \
	--with-gss=yes \
%if %enable_gpgme
	--with-gpgme \
%endif
	--with-ssl \
	--with-ldap=yes

make

%install
rm -rf %{buildroot}
%makeinstall_std GTK_UPDATE_ICON_CACHE="/usr/bin/gtk-update-icon-cache --ignore-theme-index"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{summary}
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Network;Email;X-MandrivaLinux-Internet-Mail;
EOF

# Icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 644 -D       gnome-balsa2.png %{buildroot}/%{_liconsdir}/%{name}.png
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

%postun
%{clean_scrollkeeper}
%{clean_desktop_database}

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING ChangeLog NEWS TODO
%config(noreplace) %{_sysconfdir}/sound/events/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/idl/*.idl
%{_datadir}/omf/*
%{_datadir}/sounds/*
%{_datadir}/icons/*
%{_libdir}/bonobo/servers/*.server
%{_mandir}/*/*
%ghost %{_datadir}/gnome/help/%{name}/*/%{name}.html

%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png


