#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
#
%define		_kernelsrcdir		/usr/src/linux-2.4
Summary:	CVSFS - CVS filesystem
Summary(pl.UTF-8):	CVSFS - system plikowy CVS
Name:		cvsfs
Version:	1.1.9
%define	_rel	0.1
Release:	%{_rel}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cvsfs/%{name}-%{version}.tar.gz
# Source0-md5:	622365b1b94e85653cec013fa43504d3
Patch0:		%{name}-Makefile.am.patch
Patch1:		%{name}-PPC.patch
Patch2:		%{name}-AXP.patch
URL:		http://sourceforge.net/projects/cvsfs/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with userspace}
BuildRequires:	libstdc++-devel
%endif
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel24-headers}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides a package which presents the CVS contents as mountable
file system. It allows to view the versioned files as like they were
ordinary files on a disk. There is also a possibility to check in/out
some files for editing.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia prezentujące zawartość repozytorium CVS
jako montowalny system plików. CVSFS umożliwia przeglądanie
wersjonowanych plików w taki sposób, jakby były zwykłymi plikami na
dysku. Jest także możliwość pobrania i zapisania plików po
zmodyfikowaniu.

%package -n kernel24-cvsfs
Summary:	CVSFS Linux kernel module
Summary(pl.UTF-8):	Moduł jądra Linuksa CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}

%description -n kernel24-cvsfs
CVS FS Linux kernel module.

%description -n kernel24-cvsfs -l pl.UTF-8
Moduł jądra Linuksa CVS FS.

%package -n kernel24-smp-cvsfs
Summary:	CVSFS Linux SMP kernel module
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}

%description -n kernel24-smp-cvsfs
CVS FS module for Linux SMP kernel.

%description -n kernel24-smp-cvsfs -l pl.UTF-8
Moduł CVS FS dla jądra Linuksa SMP.

%prep
%setup -q
%patch0 -p0
%ifarch ppc
%patch1 -p1
%endif
%ifarch alpha
%patch2 -p1
%endif

%build
%{__aclocal}
%{__automake} --gnu
%{__autoconf}
%configure

%if %{with kernel}
%{__make} -C cvsfs \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -Wall -D__SMP__ -D__KERNEL_SMP=1" \
	INCLUDES="-I%{_kernelsrcdir}/include"
mv cvsfs/cvsfs.o cvsfs/cvsfs-smp.o
%{__make} -C cvsfs clean
%{__make} -C cvsfs \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -Wall" \
	INCLUDES="-I%{_kernelsrcdir}/include"
%endif

%if %{with userspace}
for d in cvsfsd cvsmnt cvsmount cvsumount include init tools ; do
	%{__make} -C $d
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/fs
install cvsfs/cvsfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs
install cvsfs/cvsfs-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/fs/cvsfs.o
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install cvsmnt/cvsmnt $RPM_BUILD_ROOT%{_sbindir}
install cvsmount/cvsmount $RPM_BUILD_ROOT%{_sbindir}
install cvsumount/cvsumount $RPM_BUILD_ROOT%{_sbindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel24-cvsfs
%depmod %{_kernel_ver}

%postun -n kernel24-cvsfs
%depmod %{_kernel_ver}

%post	-n kernel24-smp-cvsfs
%depmod %{_kernel_ver}smp

%postun -n kernel24-smp-cvsfs
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_sbindir}/*
%endif

%if %{with kernel}
%files -n kernel24-cvsfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/fs/cvsfs.o*

%files -n kernel24-smp-cvsfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/fs/cvsfs.o*
%endif
