%global __python %{__python3}

Name:           fs-uae-arcade
Version:        2.8.3
Release:        3%{?dist}
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
install -d %{buildroot}%{_datadir}/appdata
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/appdata
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

# Symlink system font
rm %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Bold.ttf \
    %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files 
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_pkgdocdir}
%license COPYING


%changelog
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
