%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Tokyo Tyrant: network interface of Tokyo Cabinet
Name:		tokyotyrant
Version:	1.1.41
Release:	2
License:	LGPLv2.1+
Group:		System/Libraries
Url:		http://1978th.net/tokyotyrant/
Source0:	http://1978th.net/tokyotyrant/%{name}-%{version}.tar.gz
Patch0:		tokyotyrant-1.1.33-mdv_conf.diff
Patch1:		tokyotyrant-1.1.33-sonames.diff
BuildRequires:	bzip2-devel
BuildRequires:	lua-devel
BuildRequires:	pkgconfig(tokyocabinet)
BuildRequires:	pkgconfig(zlib)

%description
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

%files
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Tokyo Cabinet: a modern implementation of DBM
Group:		System/Libraries

%description -n %{libname}
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

%files -n %{libname}
%doc COPYING ChangeLog README THANKS doc/* ext/*.lua
%{_libdir}/tokyotyrant.so.%{major}*
%{_libdir}/ttskeldir.so
%{_libdir}/ttskelmock.so
%{_libdir}/ttskelnull.so
%{_libdir}/ttskelproxy.so

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Static library and header files for the tokyotyrant library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Tokyo Tyrant is a package of network interface to the DBM called Tokyo Cabinet.
Though the DBM has high performance, you might bother in case that multiple
processes share the same database, or remote processes access the database.
Thus, Tokyo Tyrant is provided for concurrent and remote connections to Tokyo
Cabinet. It is composed of the server process managing a database and its
access library for client applications.

This package contains the static library and its header files.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libtokyotyrant.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/tokyotyrant.pc
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%setup -q
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

%install
%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_datadir}/%{name}
rm -f doc/*~

