%define		_kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	CVSFS
Summary(pl):	CVSFS
Name:		cvsfs
Version:	1.0.3
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.zip
Patch0:	%{name}-config.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description

%description -l pl

%package -n kernel%{smpstr}-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu� j�dra CVSFS
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
Prereq:		/sbin/depmod

%description -n kernel%{smpstr}-cvsfs

%description -n kernel%{smpstr}-cvsfs -l pl

%prep
%setup -q
%patch0 -p0

%build
%{__make} \
%if %{smp}
	KDEFS+=" -D__KERNEL_SMP=1"
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs 

install cvsmnt/cvsmnt $RPM_BUILD_ROOT%{_bindir}
install cvsmount/cvsmount $RPM_BUILD_ROOT%{_bindir}
install cvsmount/mount.cvsfs $RPM_BUILD_ROOT%{_bindir}
install cvsfs/cvsfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs
gzip -9nf ChangeLog README INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post
%postun

%post -n kernel%{smpstr}-cvsfs
/sbin/depmod -a

%postun -n kernel%{smpstr}-cvsfs
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc 
%attr(755,root,root) %{_bindir}/*

%files -n kernel%{smpstr}-cvsfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/fs/cvsfs.o
