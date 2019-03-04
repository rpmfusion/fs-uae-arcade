%global __python %{__python3}

Name:           fs-uae-arcade
Version:        2.8.3
Release:        9%{?dist}
Summary:        Fullscreen game browser for FS-UAE

#  The entire source code is GPLv2+ except oyoyo which is MIT
License:        GPLv2+ and MIT
URL:            http://fs-uae.net/
Source0:        http://fs-uae.net/fs-uae/stable/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml
# Remove six python library
# Patch from fs-uae-arcade
Patch0:         %{name}-2.8.3-remove_inbuilt_six.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       python3-qt5
Requires:       python3-six
Requires:       liberation-sans-fonts
Requires:       fs-uae = %{version}

# oyoyo is not in Fedora
Provides:       bundled(python3-oyoyo) = 0.0.0

%description
FS-UAE Arcade is a fullscreen Amiga game browser for FS-UAE.


%prep
%autosetup -p1

# In Python 3.7 async is a keyword, and so we can't have a module named async
# https://github.com/mcfletch/pyopengl/issues/14
# https://github.com/FrodeSolheim/fs-uae-arcade/issues/16
# https://src.fedoraproject.org/rpms/python-pyopengl/c/fcae096bceb00a47990317f437197e41ff023e95
mv OpenGL/GL/SGIX/async.py \
   OpenGL/GL/SGIX/async_.py

mv OpenGL/raw/GL/SGIX/async.py \
   OpenGL/raw/GL/SGIX/async_.py

sed -i -e 's/from OpenGL.raw.GL.SGIX.async/from OpenGL.raw.GL.SGIX.async_/g' \
    OpenGL/GL/SGIX/async_.py

# Remove bundled lib
rm -rf six

# Remove shebang from non executable scripts
FILES="fstd/adffile.py
  OpenGL/arrays/_buffers.py
  OpenGL/arrays/buffers.py
  arcade/res/update.py
  fsgs/amiga/adf.py
  fstd/adffile.py
  launcher/apps/__init__.py"
for pyfile in $FILES
do
  sed -i -e '/^#!/, 1d' $pyfile
done


%build
# EMPTY SECTION


%install
%make_install prefix=%{_prefix}

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install AppData file
install -d %{buildroot}%{_datadir}/metainfo
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/metainfo
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

# Symlink system font
rm %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Bold.ttf \
    %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf


%files 
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_pkgdocdir}
%license COPYING


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.8.3-8
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8.3-6
- Rebuilt for Python 3.7

* Sun May 20 2018 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-5
- Fixed AppData file (BZ #4845)
- Used new AppData directory
- Removed obsolete scriptlets

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-3
- Added a virtual provide to note oyoyo is bundled
- Amended License tag
- Added AppData file
- Removed six python library
- Unbundled font file

* Sat Sep 16 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-2
- Relaxed fs-uae requires

* Sat Sep 09 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-1
- Updated to new upstream version

* Sun Apr 03 2016 Andrea Musuruane <musuruan@gmail.com> - 2.6.2-1
- First release

