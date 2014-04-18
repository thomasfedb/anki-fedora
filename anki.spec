%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		anki
Version:	2.0.25
Release:	1%{?dist}
Summary:	Flashcard program for using space repetition learning

Group:		Amusements/Games
License:	AGPLv3+ and GPLv3+ and MIT and BSD
URL:		http://ankisrs.net/
Source0:	http://ankisrs.net/download/mirror/anki-%{version}.tgz
Source1:	anki.svg

# Config change: don't check for new updates.
Patch0:		anki-2.0.3-noupdate.patch
BuildRequires:	python2-devel, python-setuptools, python-sqlalchemy
BuildRequires:	desktop-file-utils, PyQt4, python-simplejson
Requires:	qt4, PyQt4
Requires:	python-sqlalchemy, python-simplejson
Requires:	python-matplotlib
Requires:	pygame, python-BeautifulSoup, python-httplib2
Requires:	pyaudio, sox
BuildArch:	noarch

%description
Anki is a program designed to help you remember facts (such as words
and phrases in a foreign language) as easily, quickly and efficiently
as possible. Anki is based on a theory called spaced repetition.

%prep
%setup -q
mv thirdparty/send2trash .
rm -rf thirdparty
%patch0 -p1 -b .noupdate

%build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
rm -f aqt/*.noupdate
rm -f aqt/*.fix-browserview
cp -R aqt %{buildroot}%{_datadir}/%{name}/
cp -R designer %{buildroot}%{_datadir}/%{name}/
cp -R anki %{buildroot}%{_datadir}/%{name}/
cp -R locale %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/%{name}/thirdparty
cp -R send2trash %{buildroot}%{_datadir}/%{name}/thirdparty/

install -d %{buildroot}%{_bindir}
install -m 755 runanki %{buildroot}%{_bindir}/anki

install -d %{buildroot}%{_pkgdocdir}
install -m 644 LICENSE* %{buildroot}%{_pkgdocdir}/
install -m 644 README* %{buildroot}%{_pkgdocdir}/

install -d %{buildroot}%{_datadir}/mime/packages
install -m 644 anki.xml %{buildroot}%{_datadir}/mime/packages

install -d %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/

install -d %{buildroot}%{_mandir}/man1
install -m 644 anki.1 %{buildroot}%{_mandir}/man1/

desktop-file-install \
  --remove-category=KDE \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

find %{buildroot} -type f -o -type l|sed '
s:'"%{buildroot}"'::
s:\(.*/share/anki/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
s:\(.*/share/anki/locale/qt_\)\([^.]\+\)\(\.qm\):%lang(\2) \1\2\3:
s:^\([^%].*\)::
s:%lang(C) ::
/^$/d' > anki.lang

find %{buildroot}/usr/share/anki/locale -type d|sed '
s:'"%{buildroot}"'::
s:\(.*\):%dir \1:' >>anki.lang

%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%doc LICENSE.* README*
%{_bindir}/anki
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/aqt/
%{_datadir}/%{name}/designer/
%{_datadir}/%{name}/anki/
%{_datadir}/%{name}/thirdparty/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/mime/packages/anki.xml
%{_mandir}/man1/%{name}.*

%changelog
* Fri Apr 18 2014 Christian Krause <chkr@fedoraproject.org> - 2.0.25-1
- Update to new upstream version 2.0.25 (BZ 1087211)

* Fri Jan 31 2014 Christian Krause <chkr@fedoraproject.org> - 2.0.22-1
- Update to new upstream version 2.0.22 (BZ 1057013)

* Tue Jan 14 2014 Christian Krause <chkr@fedoraproject.org> - 2.0.20-2
- Fix typo in changelog

* Tue Jan 14 2014 Christian Krause <chkr@fedoraproject.org> - 2.0.20-1
- Update to new upstream version 2.0.20 (BZ 1040134)

* Wed Nov 20 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.18-1
- Update to new upstream version 2.0.18 (BZ 1027704)

* Fri Nov 01 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.16-1
- Update to new upstream version 2.0.16

* Fri Oct 11 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.13-1
- Update to new upstream version 2.0.13

* Sun Aug 04 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.12-1
- Update to new upstream version 2.0.12 (BZ 989901)
- Install docs to %%{_pkgdocdir} (BZ 991962)
- Install additional LICENSE file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.11-1
- Update to new upstream version 2.0.11 (BZ 973523)

* Mon Jun 03 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.9-1
- Update to new upstream version 2.0.9 (BZ 970052)
- Remove patch (issue was fixed upstream)

* Mon Apr 01 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.8-2
- Add patch to fix filter selection in browser view:
  https://anki.lighthouseapp.com/projects/100923/tickets/729-browser-filter-tree-doesnt-filter

* Sun Feb 24 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.8-1
- Update to new upstream version 2.0.8

* Sat Feb 02 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.7-1
- Update to new upstream version 2.0.7

* Thu Jan 10 2013 Christian Krause <chkr@fedoraproject.org> - 2.0.4-1
- Update to anki-2.0.4 (based on work from Christophe Fergeau <cfergeau@redhat.com>)
- Update license to AGPLv3+
- Update noupdate patch
- Add man page
- Add post/postun scripts (needed for MimeType key in anki.desktop and for
  /usr/share/mime/packages/anki.xml)
- Spec file cleanup

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Christian Krause <chkr@fedoraproject.org> - 1.2.11-1
- Update to new upstream version 1.2.11 (BZ 819821)
- Remove patch (issue was fixed upstream)

* Wed Feb  8 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.9-4
- Remove python-sqlite2 dep as anki will work with the stdlib sqlite3 module

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.9-2
- Add and install  svg version of anki's icon
(extracted from anki-1.2.9/icons/anki-logo.svg)

* Thu Jun 30 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.9-1
- Update to new upstream version 1.2.9 (BZ 717584) to fix more
  compatibility issues with python-sqlalchemy-0.7.x
- Remove upstreamed patches
- Add patch to avoid unicode error messages on startup

* Tue Jun 28 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.8-2
- Fix FTBFS issue (BZ 715813)
- Adding two upstream patches to support python-sqlalchemy-0.7.x

* Tue Apr 05 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.8-1
- Update to new upstream version 1.2.8 (BZ 691342)

* Sun Feb 27 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.7-1
- Update to new upstream version 1.2.7 (BZ 678848)
- Add sox as requirement for audio recording (BZ 674493)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.6-1
- Update to new upstream version 1.2.6 (BZ 665163)

* Thu Jan 27 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.5-1
- Update to new upstream version 1.2.5 (BZ 665163)

* Sun Jan 23 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.4-1
- Update to new upstream version 1.2.4 (BZ 665163)

* Fri Jan 14 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.2-1
- Update to new upstream version 1.2.2 (BZ 665163)

* Tue Dec 14 2010 Christian Krause <chkr@fedoraproject.org> - 1.1.10-1
- Update to new upstream version 1.1.10 (BZ 655939)

* Sat Aug 21 2010 Christian Krause <chkr@fedoraproject.org> - 1.0.1-1
- Update to new upstream version 1.0.1

* Mon Aug 02 2010 Christian Krause <chkr@fedoraproject.org> - 1.0-1
- Update to new upstream version 1.0
- Use original upstream tgz since upstream doesn't ship the problematic
  example files anymore
- Remove upstreamed patches
- Update noupdate patch
- Add BR python-simplejson

* Sun Jul 25 2010 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.6-5
- Generalized generation of anki.lang to support any python 2.* release

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.9.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May 13 2010 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.6-3
- Add pyaudio as requirement for audio recording
- Add upstream patch to prevent anki hanging during audio recording

* Sun Feb 28 2010 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.6-2
- Add a patch to fix a crash when sys tray icon is enabled (BZ 567672)

* Fri Feb 19 2010 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.6-1
- Update to new upstream version
- Remove example files from upstream tarball due to unknown license
- Updated noupdate patch

* Wed Jan 20 2010 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.5-3.git20100120
- Update to git snapshot
- Includes fix for BZ 546331

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.5-1
- Update to new upstream version 0.9.9.8.5

* Thu Jul 02 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.8.4-1
- Update to new upstream version 0.9.9.8.4
- fix one %%lang tag

* Sun May 24 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.9b-1
- Update to new upstream version 0.9.9.7.9b to fix a syncing bug

* Tue May 12 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.9-1
- Update to new upstream version 0.9.9.7.9 to fix an update problem of the 
statusbar and of the titlebar

* Thu May 07 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.8-2
- Bump release

* Wed May 06 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.8-1
- Update to new upstream version 0.9.9.7.8

* Sat Apr 11 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.4-1
- Update to new upstream version 0.9.9.7.4 (BZ 494598)
- Require python-matplotlib instead of numpy (BZ 495232)

* Wed Apr 01 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.7.1-1
- Update to new upstream version 0.9.9.7.1
- Drop unihaninstall patch (applied upstream)
- Updated noupdate patch
- Use original upstream tgz since upstream doesn't ship the example files
anymore

* Sun Mar 01 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.6-4
- Bump release

* Fri Feb 27 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.6-3
- Proper packaging of locale files

* Fri Feb 13 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.6-2
- Fixed license field
- Install unihan.db

* Wed Feb 11 2009 Christian Krause <chkr@fedoraproject.org> - 0.9.9.6-1
- First spec file for anki
