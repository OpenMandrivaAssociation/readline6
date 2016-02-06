%define	major 6
%define	libname	%mklibname readline %{major}
%define	libhist	%mklibname history %{major}
%define	devname	%mklibname readline%{major} -d
%define patchlevel 8

Summary:	Old version of a library for reading lines from a terminal
Name:		readline6
Version:	6.3
Release:	14
License:	GPLv2+
Group:		System/Libraries
Url:		http://tiswww.case.edu/php/chet/readline/rltop.html
Source0:	ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
# Upstream patches
%(for i in `seq 1 %{patchlevel}`; do echo Patch$i: ftp://ftp.gnu.org/pub/gnu/readline/readline-%{version}-patches/readline`echo %{version} |sed -e 's,\\.,,g'`-`echo 000$i |rev |cut -b1-3 |rev`; done)
Patch1000:	readline-4.3-no_rpath.patch
Patch1003:	readline-4.1-outdated.patch
Patch1004:	rl-header.patch
Patch1005:	rl-attribute.patch
Patch1006:	readline-6.0-fix-shared-libs-perms.patch
Patch1008:	readline-6.2-fix-missing-linkage.patch
BuildRequires:	ncurses-devel

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.

This is an old version of readline, provided for compatibility with legacy
applications only.

%package -n	%{libname}
Summary:	Old version of the shared libreadline library for readline
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Conflicts:	%{_lib}history < 6.2-13
Obsoletes:	%{_lib}history < 6.2-13

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked to readline.

This is an old version of readline, provided for compatibility with legacy
applications only.

%package -n	%{libhist}
Summary:	Old version of the shared libhistory library for readline
Group:		System/Libraries
Conflicts:	%{_lib}readline6 < 6.2-13
Obsoletes:	%{_lib}readline6 < 6.2-13

%description -n	%{libhist}
This package contains the libhistory library from readline.

%package	doc
Summary:	Readline documentation in GNU info format
Group:		Books/Computer books
Provides:	%{name}-doc = %{EVRD}
Obsoletes:	%{libname}-doc < %{EVRD}
BuildArch:	noarch

%description	doc
This package contains readline documentation in the GNU info format.

%package -n	%{devname}
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libhist} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%prep
%setup -qn readline-%{version}
# Upstream patches
%(for i in `seq 1 %{patchlevel}`; do echo %%patch$i -p0; done)

%apply_patches

sed -e 's#/usr/local#%{_prefix}#g' -i doc/texi2html
libtoolize --copy --force

%build
%configure \
	--enable-static=no \
	--with-curses \
	--enable-multibyte

%make

%install
%makeinstall_std
# put all libs in /lib because some package needs it
# before /usr is mounted
install -d %{buildroot}/%{_lib}
for l in libhistory.so libreadline.so; do
	rm %{buildroot}%{_libdir}/${l}
	mv %{buildroot}%{_libdir}/${l}.%{major}* %{buildroot}/%{_lib}
	ln -sr %{buildroot}/%{_lib}/${l}.%{major}.* %{buildroot}%{_libdir}/${l}
done

rm -rf %{buildroot}%{_docdir}/readline/{CHANGES,INSTALL,README} \
	%{buildroot}%{_prefix}/uclibc%{_docdir}/readline/{CHANGES,INSTALL,README}

# No devel files for compat libraries...
rm -rf \
	%{buildroot}%{uclibc_root}%{_libdir}/libhistory.so \
	%{buildroot}%{uclibc_root}%{_libdir}/libreadline.so \
	%{buildroot}%{_infodir}/history.info* \
	%{buildroot}%{_infodir}/readline.info* \
	%{buildroot}%{_infodir}/rluserman.info* \
	%{buildroot}%{_mandir}/man3/* \
	%{buildroot}%{_includedir}/readline \
	%{buildroot}%{_libdir}/libhistory.so \
	%{buildroot}%{_libdir}/libreadline.so

%files -n %{libhist}
/%{_lib}/libhistory.so.%{major}*

%files -n %{libname}
/%{_lib}/libreadline.so.%{major}*
