#
# Conditional build:
%bcond_without	dotnet	# C# package
%bcond_without	java	# Java package
#
%ifnarch %{ix86} %{x8664} arm aarch64 ia64 mips ppc ppc64 s390x sparc sparcv9 sparc64
%undefine	with_dotnet
%endif
%ifarch i386
%undefine	with_dotnet
%endif
Summary:	WB - disk based (sorted) associative array package
Summary(pl.UTF-8):	WB - pakiet tablic asocjacyjnych przechowujących (posortowane) dane na dysku
Name:		wb
Version:	2b4
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://groups.csail.mit.edu/mac/ftpdir/scm/%{name}-%{version}.zip
# Source0-md5:	29c0e3e340ce3faeb80c80e1c15ad7b5
Patch0:		%{name}-info.patch
URL:		http://people.csail.mit.edu/jaffer/WB
%{?with_dotnet:BuildRequires:	mono-csharp}
BuildRequires:	scm
BuildRequires:	scm-slib
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
Requires:	scm
Requires:	scm-slib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WB is a disk based (sorted) associative-array package providing C,
SCM, Java, and C# libraries. These associative arrays consist of
variable length (0.B to 255.B) keys and values.

This package contains the libraries for C and SCM Scheme
implementation.

%description -l pl.UTF-8
WB to pakiet tablic asocjacyjnych przechowujących (posortowane) dane
na dysku z bibliotekami dla C, SCM-a, C# i Javy. Niniejsze tablice
asocjacyjne składają się z kluczy i wartości zmiennej długości (od 0.B
do 255.B).

Ten pakiet zawiera biblioteki dla C oraz implementacji SCM języka
Scheme.

%package devel
Summary:	C header files for WB library
Summary(pl.UTF-8):	Pliki nagłówkowe C dla biblioteki WB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
C header files for WB library.

%description devel -l pl.UTF-8
Pliki nagłówkowe C dla biblioteki WB.

%package static
Summary:	Static WB library
Summary(pl.UTF-8):	Statyczna biblioteka WB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static WB library.

%description static -l pl.UTF-8
Statyczna biblioteka WB.

%package -n dotnet-wb
Summary:	WB library for C#
Summary(pl.UTF-8):	Biblioteka WB dla C#
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mono

%description -n dotnet-wb
WB library for C#.

%description -n dotnet-wb -l pl.UTF-8
Biblioteka WB dla C#.

%package -n java-wb
Summary:	WB library for Java
Summary(pl.UTF-8):	Biblioteka WB dla Javy
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jre

%description -n java-wb
WB library for Java.

%description -n java-wb -l pl.UTF-8
Biblioteka WB dla Javy.

%prep
%setup -q -n wb
%patch0 -p1

%build
# not autoconf-generated
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

%{__make} -C c \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"

%if %{with dotnet}
%{__make} -C csharp
%else
# needed for info part
%{__make} csharp/Wb.cs
%endif

%if %{with java}
%{__make} java/wb.jar
%else
%{__make} java/wb/Scan.txi java/wb/Db.txi java/wb/Handle.txi java/wb/Segs.txi java/wb/Wbdefs.txi
%endif

%{__make} wb.info

%install
rm -rf $RPM_BUILD_ROOT

%{__make} installc install-info %{?with_dotnet:installdll} %{?with_java:installjar} \
	DESTDIR=$RPM_BUILD_ROOT

# let rpm autogenerate dependencies
chmod 755 $RPM_BUILD_ROOT%{_libdir}/wb/*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc ANNOUNCE ChangeLog README
%attr(755,root,root) %{_bindir}/wbcheck
%dir %{_libdir}/wb
%attr(755,root,root) %{_libdir}/wb/libwb.so
%attr(755,root,root) %{_libdir}/wb/wbscm.so
%attr(755,root,root) %{_libdir}/libwb.so
%{_libdir}/wb/*.scm
%{_infodir}/wb.info*

%files devel
%defattr(644,root,root,755)
%{_includedir}/wb
%{_includedir}/wbsys.h

%files static
%defattr(644,root,root,755)
%{_libdir}/wb/libwb.a
%{_libdir}/libwb.a

%if %{with dotnet}
%files -n dotnet-wb
%defattr(644,root,root,755)
%{_libdir}/wb/Wb.dll
%{_libdir}/Wb.dll
%endif

%if %{with java}
%files -n java-wb
%defattr(644,root,root,755)
%{_javadir}/wb.jar
%endif
