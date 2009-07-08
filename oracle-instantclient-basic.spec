# TODO:
# - mv .jar files to subpackage and add java dependencies
#
# NOTE:
# - see "URL:" for download links
# - if you want to build 32-bit version, you don't have to download Source1.
#   Just comment it out.
# - if you want to build 64-bit version, comment out Source0

%define		major	11.1
%define		minor	0.7
%define		rel	0
Summary:	Oracle database client - common files
Summary(pl.UTF-8):	Klient bazy danych Oracle - wspólne pliki
Name:		oracle-instantclient-basic
Version:	%{major}.%{minor}.%{rel}
Release:	0.1
License:	OTN (proprietary, non-distributable)
Group:		Applications
Source0:	instantclient-basic-linux32-%{major}.%{minor}.zip
# NoSource0-md5:	df8595e0564721c6d0d898cad015bba8
Source1:	basic-%{major}.%{minor}%{rel}-linux-x86_64.zip
# NoSource1-md5:	f62dc38e4d10899a8adf24ad470b2f6a
NoSource:	0
NoSource:	1
URL:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		srcdir	instantclient_%(echo %{major} | tr . _)

%description
Oracle database client - common files.

%description -l pl.UTF-8
Klient bazy danych Oracle - wspólne pliki.

%prep
%ifarch %{ix86}
%setup -q -c -T -b 0
%endif

%ifarch %{x8664}
%setup -q -c -T -b 1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir}/sqlplus,%{_javadir}}

install %{srcdir}/*.jar $RPM_BUILD_ROOT%{_javadir}
install %{srcdir}/*.so.%{major} $RPM_BUILD_ROOT%{_libdir}
install %{srcdir}/*.so $RPM_BUILD_ROOT%{_libdir}
install %{srcdir}/genezi $RPM_BUILD_ROOT%{_bindir}/genezi
install %{srcdir}/adrci $RPM_BUILD_ROOT%{_bindir}/adrci

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.so.%{major}
%attr(755,root,root) %{_bindir}/genezi
%attr(755,root,root) %{_bindir}/adrci
%doc %{srcdir}/BASIC_README
