Summary:	CVSFS
Summary(pl):	CVSFS
Name:		cvsfs
Version:	1.0.9
%define		_rel 1
Release:	%{_rel}
License:	GPL
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
#BuildRequires:	autoconf
#BuildRequires:	automake

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define		_sysconfdir	/etc

%description

%description -l pl

%package -n kernel-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu³ j±dra CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-cvsfs

%description -n kernel-cvsfs -l pl

%package -n kernel-smp-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu³ j±dra CVSFS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-cvsfs

%description -n kernel-smp-cvsfs -l pl

%prep
%setup -q

%build
%configure2_13 

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

#gzip -9nf README* tcpdump.patch CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

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
