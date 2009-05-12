%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		anki
Version:	0.9.9.7.9
Release:	1%{?dist}
Summary:	Flashcard program for using space repetition learning

Group:		Amusements/Games
# the file anki-%{version}/libanki/anki/features/chinese/unihan.db 
# was created out of  Unihan.txt from www.unicode.org (MIT license)
License:	GPLv3+ and MIT
URL:		http://www.ichi2.net/anki
Source0:	http://ichi2.net/anki/download/files/%{name}-%{version}.tgz

# Config change: don't check for new updates.
Patch0:		anki-0.9.9.7.8-noupdate.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python-devel, python-setuptools, python-sqlalchemy
BuildRequires:	PyQt4-devel
BuildRequires:	desktop-file-utils
Requires:	qt4, PyQt4
Requires:	python-sqlalchemy, python-simplejson, python-sqlite2
Requires:	python-matplotlib
Requires:	pygame
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

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog CREDITS README*
# libankiqt
%dir %{python_sitelib}/ankiqt
%{python_sitelib}/ankiqt/*.py*
%{python_sitelib}/ankiqt/ui
%{python_sitelib}/ankiqt/forms

# libanki
%dir %{python_sitelib}/anki
%{python_sitelib}/anki/*.py*
%{python_sitelib}/anki/importing
%{python_sitelib}/anki/features

# locale
%dir %{python_sitelib}/ankiqt/locale/
%dir %{python_sitelib}/anki/locale/
%lang(cs) %{python_sitelib}/*/locale/cs_*/
%lang(de) %{python_sitelib}/*/locale/de_*/
%lang(es) %{python_sitelib}/*/locale/es_*/
%lang(fi) %{python_sitelib}/*/locale/fi_*/
%lang(fr) %{python_sitelib}/*/locale/fr_*/
%lang(it) %{python_sitelib}/*/locale/it_*/
%lang(ja) %{python_sitelib}/*/locale/ja_*/
%lang(ko) %{python_sitelib}/*/locale/ko_*/
%lang(pl) %{python_sitelib}/*/locale/pl_*/
%lang(zh) %{python_sitelib}/*/locale/zh_*/
%lang(sv) %{python_sitelib}/*/locale/sv_*/
%lang(pt) %{python_sitelib}/*/locale/pt_*/
%lang(ee) %{python_sitelib}/*/locale/ee_*/
%lang(ee) %{python_sitelib}/*/locale/mn_*/

%{python_sitelib}/*egg-info
%{_bindir}/anki
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
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
