%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		anki
Version:	1.0
Release:	1%{?dist}
Summary:	Flashcard program for using space repetition learning

Group:		Amusements/Games
# the file anki-%%{version}/libanki/anki/features/chinese/unihan.db 
# was created out of  Unihan.txt from www.unicode.org (MIT license)
License:	GPLv3+ and MIT
URL:		http://www.ichi2.net/anki
Source0:	http://anki.googlecode.com/files/%{name}-%{version}.tgz

# Config change: don't check for new updates.
Patch0:		anki-1.0-noupdate.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python-devel, python-setuptools, python-sqlalchemy
BuildRequires:	desktop-file-utils, PyQt4, python-simplejson
Requires:	qt4, PyQt4
Requires:	python-sqlalchemy, python-simplejson, python-sqlite2
Requires:	python-matplotlib
Requires:	pygame, python-BeautifulSoup
Requires:	pyaudio
BuildArch:	noarch

%description
Anki is a program designed to help you remember facts (such as words
and phrases in a foreign language) as easily, quickly and efficiently
as possible. Anki is based on a theory called spaced repetition.

%prep
%setup -q
%patch0 -p1 -b .noupdate 

%build
pushd libanki
%{__python} setup.py build
popd

%{__python} setup.py build


%install
rm -rf %{buildroot}
pushd libanki
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --remove-category=KDE \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

install -d %{buildroot}%{_datadir}/pixmaps
install -m 644 icons/anki.png %{buildroot}%{_datadir}/pixmaps/

find %{buildroot} -type f -o -type l|sed '
s:'"%{buildroot}"'::
s:\(.*/lib/python2\..*/site-packages/ankiqt/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
s:\(.*/lib/python2\..*/site-packages/anki/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
s:^\([^%].*\)::
s:%lang(C) ::
/^$/d' > anki.lang



%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog
%doc COPYING CREDITS README*
# libankiqt
%dir %{python_sitelib}/ankiqt
%{python_sitelib}/ankiqt/*.py*
%{python_sitelib}/ankiqt/ui
%{python_sitelib}/ankiqt/forms

# libanki
%dir %{python_sitelib}/anki
%{python_sitelib}/anki/*.py*
%{python_sitelib}/anki/importing

# locale
%dir %{python_sitelib}/ankiqt/locale/
%dir %{python_sitelib}/ankiqt/locale/*
%dir %{python_sitelib}/ankiqt/locale/*/LC_MESSAGES
%dir %{python_sitelib}/anki/locale/
%dir %{python_sitelib}/anki/locale/*
%dir %{python_sitelib}/anki/locale/*/LC_MESSAGES

%{python_sitelib}/*egg-info
%{_bindir}/anki
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
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
