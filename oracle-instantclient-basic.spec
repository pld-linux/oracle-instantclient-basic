# TODO:
# - mv .jar files to subpackage and add java dependencies
#
# NOTE:
# - see "URL:" for download links
# - if you want to build 32-bit version, you don't have to download Source2 and Source3
#   Just comment it out.
# - if you want to build 64-bit version, comment out Source0 and Source1

%define		x86ver		11.2.0.1
%define		x8664ver	11.2.0.1.0-1

Summary:	Oracle database client - common files
Summary(pl.UTF-8):	Klient bazy danych Oracle - wspólne pliki
Name:		oracle-instantclient-basic
Version:	11.2.0.1.0
Release:	0.8
License:	OTN (proprietary, non-distributable)
Group:		Applications/Databases
Source0:	instantclient-basic-linux32-%{x86ver}.zip
# NoSource0-md5:	5d8bba5d245b885dc8a6fda5ec6e6442
Source1:	instantclient-sdk-linux32-%{x86ver}.zip
# NoSource1-md5:	374e1986621cb83ec90d4714c5430473
Source2:	oracle-instantclient11.2-basic-%{x8664ver}.x86_64.zip
# NoSource2-md5:	7d96ba339c3cb6d5ba5f2b40ed7ed02d
Source3:	oracle-instantclient11.2-sdk-%{x8664ver}.x86_64.zip
# NoSource3-md5:	ee46ae0ec92397cb9b0cef4f48e0eda7
# http://duberga.net/dbd_oracle_instantclient_linux/oracle-instantclient-config
Source4:	oracle-instantclient-config.in
Source5:	oracle-instantclient.pc.in
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
URL:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html
BuildRequires:	sed
BuildRequires:	unzip
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Orcale Database Instant Client Package - Basic.
All files required to run OCI, OCCI, and JDBC-OCI applications.

%description -l pl.UTF-8
Klient bazy danych Oracle - wspólne pliki.

%package devel
Summary:	SDK for Oracle Database Instant Client
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Oracle Database Instant Client Package - SDK.
Additional header files and an example makefile for developing
Oracle applications with Instant Client.

%prep
%ifarch %{ix86}
%setup -q -c -T -b 0 -b 1
%endif

%ifarch %{x8664}
%setup -q -c -T -b 2 -b 3
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir}/sqlplus,%{_javadir}} \
	$RPM_BUILD_ROOT{%{_examplesdir}/%{name},%{_includedir}/oracle/client} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

cd instantclient_*

install *.jar $RPM_BUILD_ROOT%{_javadir}
install *.so* $RPM_BUILD_ROOT%{_libdir}
install genezi $RPM_BUILD_ROOT%{_bindir}/genezi
install adrci $RPM_BUILD_ROOT%{_bindir}/adrci

%{__sed} -e 's|@@prefix@@|%{_prefix}|' \
	-e 's|@@libdir@@|%{_libdir}|' \
	-e 's|@@includedir@@|%{_includedir}/oracle/client|' \
	-e 's|@@version@@|%{version}|' %{SOURCE4} > \
		$RPM_BUILD_ROOT%{_bindir}/oracle-instantclient-config

%{__sed} -e 's|@@prefix@@|%{_prefix}|' \
	-e 's|@@libdir@@|%{_libdir}|' \
	-e 's|@@includedir@@|%{_includedir}/oracle/client|' \
	-e 's|@@version@@|%{version}|' %{SOURCE5} > \
		$RPM_BUILD_ROOT%{_pkgconfigdir}/oracle-instantclient.pc

install sdk/ottclasses.zip $RPM_BUILD_ROOT%{_javadir}
install sdk/ott $RPM_BUILD_ROOT%{_bindir}
install sdk/include/* $RPM_BUILD_ROOT%{_includedir}/oracle/client
install sdk/demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

cd $RPM_BUILD_ROOT%{_libdir}
for ff in lib*.so.* ; do
	ln -s $ff ${ff:%%.so.*}.so
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc instantclient_*/BASIC_README
%attr(755,root,root) %{_bindir}/adrci
%attr(755,root,root) %{_bindir}/genezi
%attr(755,root,root) %{_libdir}/libclntsh.so.*
%attr(755,root,root) %{_libdir}/libocci.so.*
%attr(755,root,root) %{_libdir}/libnnz11.so
%attr(755,root,root) %{_libdir}/libociei.so
%attr(755,root,root) %{_libdir}/libocijdbc11.so
%{_javadir}/*.jar

%files devel
%defattr(644,root,root,755)
%doc instantclient_*/sdk/SDK_README
%attr(755,root,root) %{_bindir}/oracle-instantclient-config
%attr(755,root,root) %{_bindir}/ott
%attr(755,root,root) %{_libdir}/libclntsh.so
%attr(755,root,root) %{_libdir}/libocci.so
%{_pkgconfigdir}/oracle-instantclient.pc
%{_includedir}/oracle/client
%{_javadir}/*.zip
%{_examplesdir}/%{name}
