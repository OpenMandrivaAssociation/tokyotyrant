%define	major 3
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Tokyo Tyrant: network interface of Tokyo Cabinet
Name:		tokyotyrant
Version:	1.1.33
Release:	%mkrel 1
Group:		System/Libraries
License:	LGPL
URL:		http://tokyocabinet.sourceforge.net/
Source0:	http://tokyocabinet.sourceforge.net/tyrantpkg/%{name}-%{version}.tar.gz
Patch0:		tokyotyrant-1.1.33-mdv_conf.diff
Patch1:		tokyotyrant-1.1.33-sonames.diff
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	zlib-devel
BuildRequires:	lua-devel
BuildRequires:	tokyocabinet-devel >= 1.4.31
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

%package -n	%{libname}
Summary:	Tokyo Cabinet: a modern implementation of DBM
Group:          System/Libraries
%define _provides_exceptions devel(ttskl
#ttskeldir
#ttskelmock
#ttskelnull
#ttskelproxy

%description -n	%{libname}
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

%package -n	%{develname}
Summary:	Static library and header files for the tokyotyrant library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname -d %{name} 1}

%description -n	%{develname}
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

This package contains the static library and its header files.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
rm -f configure
autoconf

%configure2_5x \
    --enable-lua \
    --with-tc=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-bzip=%{_prefix} \
    --with-lua=%{_prefix}

%make

#%%check
#make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_datadir}/%{name}
rm -f doc/*~


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING ChangeLog README THANKS doc/* ext/*.lua
%{_libdir}/*.so.%{major}*
%{_libdir}/ttskeldir.so
%{_libdir}/ttskelmock.so
%{_libdir}/ttskelnull.so
%{_libdir}/ttskelproxy.so

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libtokyotyrant.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/tokyotyrant.pc
%{_mandir}/man3/*

