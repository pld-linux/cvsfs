#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
Summary:	CVSFS - CVS filesystem
Summary(pl):	CVSFS - system plikowy CVS
Name:		cvsfs
Version:	1.1.9
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cvsfs/%{name}-%{version}.tar.gz
# Source0-md5:	622365b1b94e85653cec013fa43504d3
Patch0:		cvsfs-Makefile.am.patch
Patch1:		cvsfs-PPC.patch
Patch2:		cvsfs-AXP.patch
URL:		http://sourceforge.net/projects/cvsfs/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides a package which presents the CVS contents as mountable
file system. It allows to view the versioned files as like they were
ordinary files on a disk. There is also a possibility to check in/out
some files for editing.

%description -l pl
Ten pakiet zawiera narz�dzia prezentuj�ce zawarto�� repozytorium CVS
jako montowalny system plik�w. CVSFS umo�liwia przegl�danie
wersjonowanych plik�w w taki spos�b, jakby by�y zwyk�ymi plikami na
dysku. Jest tak�e mo�liwo�� pobrania i zapisania plik�w po
zmodyfikowaniu.

%package -n kernel-cvsfs
Summary:	CVSFS Linux kernel module
Summary(pl):	Modu� j�dra Linuksa CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	cvsfs

%description -n kernel-cvsfs
CVS FS Linux kernel module.

%description -n kernel-cvsfs -l pl
Modu� j�dra Linuksa CVS FS.

%package -n kernel-smp-cvsfs
Summary:	CVSFS Linux SMP kernel module
Summary(pl):	Modu� j�dra Linuksa SMP CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	cvsfs

%description -n kernel-smp-cvsfs
CVS FS module for Linux SMP kernel.

%description -n kernel-smp-cvsfs -l pl
Modu� CVS FS dla j�dra Linuksa SMP.

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

CXXFLAGS="-DMODULES -D__SMP__ -D__KERNEL_SMP=1" %{__make}

mv cvsfs/cvsfs.o cvsfs/cvsfs-smp.o

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/fs \
	$RPM_BUILD_ROOT%{_sbindir}

install cvsmnt/cvsmnt $RPM_BUILD_ROOT%{_sbindir}
install cvsmount/cvsmount $RPM_BUILD_ROOT%{_sbindir}
install cvsumount/cvsumount $RPM_BUILD_ROOT%{_sbindir}

install cvsfs/cvsfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs
install cvsfs/cvsfs-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/fs/cvsfs.o

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-cvsfs
%depmod %{_kernel_ver}

%postun -n kernel-cvsfs
%depmod %{_kernel_ver}

%post	-n kernel-smp-cvsfs
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-cvsfs
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-cvsfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/fs/cvsfs.o*

%files -n kernel-smp-cvsfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/fs/cvsfs.o*
