%global __python %{__python3}

Name:           fs-uae-arcade
Version:        3.1.63
Release:        8%{?dist}
Summary:        Fullscreen game browser for FS-UAE

#  The entire source code is GPLv2+ except oyoyo which is MIT
License:        GPLv2+ and MIT
URL:            http://fs-uae.net/
Source0:        http://fs-uae.net/files/FS-UAE-Arcade/Stable/%{version}/%{name}-%{version}.tar.xz
Source1:        %{name}.appdata.xml

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       python3-qt5
Requires:       python3-requests
Requires:       python3-pyopengl
Requires:       liberation-sans-fonts
Requires:       fs-uae

# oyoyo is not in Fedora
Provides:       bundled(python3-oyoyo) = 0.0.0

%description
FS-UAE Arcade is a fullscreen Amiga game browser for FS-UAE.


%prep
%autosetup

# Remove bundled OpenGL library
rm -rf OpenGL
sed -i -r "/OpenGL/d" setup.py

# Remove shebang from non executable scripts
FILES="arcade/res/update.py
  fsgs/amiga/adf.py
  fstd/adffile.py
  launcher/apps/__init__.py
  oyoyo/examplebot.py"
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
install -d %{buildroot}%{_metainfodir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Symlink system font
rm %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation-sans/LiberationSans-Bold.ttf \
    %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf


%files 
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_pkgdocdir}
%license COPYING


%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Aug 05 2023 Andrea Musuruane <musuruan@gmail.com> - 3.1.63-5
- Added new BR. Fix FTBFS.

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.1.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 25 2021 Andrea Musuruane <musuruan@gmail.com> - 3.1.63-1
- Updated to new upstream release

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 25 2020 Andrea Musuruane <musuruan@gmail.com> - 3.0.5-1
- Updated to new upstream release

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 30 2019 Andrea Musuruane <musuruan@gmail.com> - 3.0.2-1
- Updated to new upstream release

* Tue Aug 13 2019 Andrea Musuruane <musuruan@gmail.com> - 3.0.0-1
- Updated to new upstream release

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

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

