%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	CVSFS
Summary(pl):	CVSFS
Name:		cvsfs
Version:	1.0.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.zip
Patch0:		%{name}-config.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
CVS fs.

%package -n kernel%{smpstr}-cvsfs
Summary:	CVSFS kernel module
Summary(pl):	Modu³ j±dra CVSFS
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
PreReq:		/sbin/depmod

%description -n kernel%{smpstr}-cvsfs
CVS fs kernel module.

%description -n kernel%{smpstr}-cvsfs -l pl
Modu³ j±dra CVS fs.

%prep
%setup -q
%patch0 -p0

%build
%{__make} \
%if %{smp}
	CFLAGS+=" -D__KERNEL_SMP=1"
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs

install cvsmnt/cvsmnt $RPM_BUILD_ROOT%{_bindir}
install cvsmount/cvsmount $RPM_BUILD_ROOT%{_bindir}
install cvsmount/mount.cvsfs $RPM_BUILD_ROOT%{_bindir}
install cvsumount/cvsmount $RPM_BUILD_ROOT%{_bindir}
install cvsfs/cvsfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs
gzip -9nf ChangeLog README INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{smpstr}-cvsfs
/sbin/depmod -a

%postun -n kernel%{smpstr}-cvsfs
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc ChangeLog.gz README.gz
%attr(755,root,root) %{_bindir}/*

%files -n kernel%{smpstr}-cvsfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/fs/cvsfs.o
