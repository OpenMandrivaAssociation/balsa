#otherwise the ghost html files are really present
%define _files_listed_twice_terminate_build	0
%define enable_gpgme 1

Summary:	Graphical Mail Client
Name:		balsa
Version:	2.5.0
Release:	2
License:	GPLv2+
Group:		Networking/Mail
URL:		http://pawsa.fedorapeople.org/balsa
Source0:	http://pawsa.fedorapeople.org/balsa/%{name}-%{version}.tar.bz2

BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-doc-utils-devel
BuildRequires:	compface-devel
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	sendmail-command
BuildRequires:	aspell-devel >= 0.50
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
BuildRequires:	libesmtp-devel
BuildRequires:	libltdl-devel
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(gmime-2.6)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:  pkgconfig(gtkspell3-3.0)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(sqlite)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(enchant)
BuildRequires:	pkgconfig(libnm-glib-vpn)

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
	--with-sqlite \
	--with-compface \
	--disable-scrollkeeper

make

%install
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
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/sounds/*
%{_mandir}/man1/*
%ghost %{_datadir}/gnome/help/%{name}/*/%{name}.html

%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/48x48/mimetypes/*.png



%changelog
* Sat Feb 25 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.4.11-1
+ Revision: 780692
- new version 2.4.11

* Mon Jun 20 2011 Funda Wang <fwang@mandriva.org> 2.4.7-6
+ Revision: 686182
- rebuild for new webkit

* Thu Apr 14 2011 Funda Wang <fwang@mandriva.org> 2.4.7-5
+ Revision: 652917
- br webkit 1
- build with libnotify 0.7

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + John Balcaen <mikala@mandriva.org>
    - Fix BR for libcanberra-gtk-devel

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 2.4.7-2mdv2010.1
+ Revision: 537538
- rebuild

* Sat Feb 20 2010 Frederik Himpe <fhimpe@mandriva.org> 2.4.7-1mdv2010.1
+ Revision: 508704
- Update to new version 2.4.7
- Ensure to build with webkit and gtksourceview support

* Wed Feb 03 2010 Sandro Cazzaniga <kharec@mandriva.org> 2.4.6-1mdv2010.1
+ Revision: 499864
- Fix summary
- %if mdkversion > 200900 --> %%post
- Remove option --with-webkit because --with-webkit and --with-gtkhtml are mutually exclusive- Update to 2.4.6
- Fix rpmlint's warning

* Sat Jan 02 2010 Frederik Himpe <fhimpe@mandriva.org> 2.4.2-1mdv2010.1
+ Revision: 485240
- Needs libnm-glib-devel to build now
- Enable canberra, unique and webkit support
- update to new version 2.4.2

* Mon Nov 30 2009 Jérôme Brenier <incubusss@mandriva.org> 2.4.1-1mdv2010.1
+ Revision: 471721
- BR : libunique-devel -> unique-devel
- new version 2.4.1
- BuildRequires: gnome-doc-utils
- fix %%files section (duplicates and directories not to be included)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

  + Frederik Himpe <fhimpe@mandriva.org>
    - Update to new version 2.4.0
    - Remove patches which are not needed anymore, don't run autoreconf
    - BuildRequires: libunique-devel

  + Götz Waschk <waschk@mandriva.org>
    - new version
    - drop patch 0
    - patch for new gmime
    - bump gmime dep
    - fix URL

  + Jérôme Soyer <saispo@mandriva.org>
    - New upstream release

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Mon Sep 08 2008 Frederik Himpe <fhimpe@mandriva.org> 2.3.26-1mdv2009.0
+ Revision: 282725
- update to new version 2.3.26

* Tue Jul 15 2008 Jérôme Soyer <saispo@mandriva.org> 2.3.25-1mdv2009.0
+ Revision: 235930
- Add a patch to disable -DGTK_DISABLE_DEPRECATED temporary
  Build the latest version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Jérôme Soyer <saispo@mandriva.org> 2.3.20-1mdv2008.1
+ Revision: 119710
- New release

* Mon Sep 17 2007 Austin Acton <austin@mandriva.org> 2.3.19-2mdv2008.0
+ Revision: 88855
- drop old (duplicate) menu

* Thu Sep 06 2007 Austin Acton <austin@mandriva.org> 2.3.19-1mdv2008.0
+ Revision: 80570
- buildrequires
- build with gtk-spell
- new version
- fix menu categories

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sun Jan 07 2007 Pascal Terjan <pterjan@mandriva.org> 2.3.14-1mdv2007.0
+ Revision: 105327
- 2.3.14
- Import balsa

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.3.13-3mdv2007.0
- Rebuild with latest dbus

* Fri Jul 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.3.13-2mdv2007.0
- Rebuild with latest libgail

* Sun Jul 02 2006 Jerome Soyer <saispo@mandriva.org> 2.3.13-1mdv2007.0
- New release 2.3.13
- Remove Patch0

* Fri Mar 10 2006 Jerome Soyer <saispo@mandriva.org> 2.3.12-1mdk
- New release 2.3.12

* Thu Mar 09 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2.3.8-5mdk
- Again Rebuild for missing src.rpm

* Fri Mar 03 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2.3.8-4mdk
- Rebuild for missing src.rpm

* Tue Jan 24 2006 Jerome Soyer <saispo@mandriva.org> 2.3.8-3mdk
- rebuild with latest libgmime

* Tue Jan 24 2006 Jerome Soyer <saispo@mandriva.org> 2.3.8-1mdk
- 2.3.8

* Wed Jan 04 2006 Frederic Crozat <fcrozat@mandriva.com> 2.3.4-2mdk
- Rebuild with latest gtkhtml
- Remove yelp-pregenerate call
- fix prereq

* Fri Sep 09 2005 Andreas Hasenack <andreas@mandriva.com> 2.3.4-1mdk
- updated to version 2.3.4
- removed ldap patch, already applied
- removed lib64 patch which was *not* being applied (but the patch itself
  was lying around)
- enabled GSSAPI authentication (tested OK)
- ignore theme index in make install
- rebuilt with openldap-2.3.x

* Mon Jul 25 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.3.3-2mdk
- Rebuild

* Fri Jun 10 2005 Austin Acton <austin@mandriva.org> 2.3.3-1mdk
- New release 2.3.3
- patch to make ldap compile

* Thu Mar 10 2005 Jerome Soyer <saispo@mandrake.org> 2.3.0-1mdk
- New release

* Tue Feb 08 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.6-4mdk
- rebuild for ldap2.2_7

* Fri Feb 04 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.6-3mdk
- rebuilt against new openldap libs

* Thu Jan 06 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.6-2mdk 
- Rebuild with latest howl

* Mon Nov 22 2004 Jerome Soyer <saispo@mandrake.org> 2.2.6-1mdk
- 2.2.6

* Wed Nov 10 2004 Jerome Soyer <saispo@mandrake.org> 2.2.5-1mdk
- 2.2.5
- Disable intltoolize

* Sat Sep 25 2004 Jerome Soyer <saispo@mandrake.org> 2.2.4-1mdk
- 2.2.4

* Fri Aug 20 2004 Jerome Soyer <saispo@mandrake.org> 2.2.3-1mdk
- 2.2.3

* Thu Aug 12 2004 Jerome Soyer <saispo@mandrake.org>2.2.2-1mdk
- 2.2.2

* Wed Jul 21 2004 Pascal Terjan <pterjan@mandrake.org> 2.2.0-1mdk
- 2.2.0
- Drop patch2 (upstream)

* Tue Apr 20 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.17-1mdk
- 2.0.17

* Fri Mar 12 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.16-3mdk
- Rebuild against latest gal/gtkhtml

* Wed Jan 28 2004 Abel Cheung <deaddog@deaddog.org> 2.0.16-2mdk
- Fix buildrequires (thx Stefan's bot)

* Wed Jan 28 2004 Abel Cheung <deaddog@deaddog.org> 2.0.16-1mdk
- New version
- Remove patch0 (upstream)
- Remove old distro BuildRequires because they are wrong, please supply
  correct ones later on if desired
- Regen patch1

