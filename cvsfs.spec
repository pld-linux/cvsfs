Summary:	CVSFS - CVS filesystem
Summary(pl):	CVSFS - system plikowy CVS
Name:		cvsfs
Version:	1.1.4
%define		_rel 2
Release:	%{_rel}
License:	GPL
Group:		Tools
Source0:	ftp://download.sourceforge.net/pub/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:		cvsfs-Makefile.am.patch
URL:		http://sourceforge.net/projects/cvsfs/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CVS FS tools.

%description -l pl
Narzêdzia do obs³ugi CVS FS.

%package -n kernel-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu³ j±dra CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
Requires:	cvsfs
%{!?_without_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-cvsfs
CVS FS module.

%description -n kernel-cvsfs -l pl
Modó³ CVS FS.

%package -n kernel-smp-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu³ j±dra CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
Requires:	cvsfs
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-cvsfs
CVS FS module for SMP kernel.

%description -n kernel-smp-cvsfs -l pl
Modó³ CVS FS fla kernela SMP.

%prep
%setup -q
%patch0 -p0

%build
%{__aclocal}
%{__automake} --gnu --add-missing
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

%post -n kernel-cvsfs
/sbin/depmod -a

%postun -n kernel-cvsfs
/sbin/depmod -a

%post -n kernel-smp-cvsfs
/sbin/depmod -a

%postun -n kernel-smp-cvsfs
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-cvsfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}/fs/cvsfs.o

%files -n kernel-smp-cvsfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}smp/fs/cvsfs.o
