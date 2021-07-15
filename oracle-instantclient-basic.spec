# TODO:
# - mv .jar files to subpackage and add java dependencies
#
# NOTE:
# - see "URL:" for download links
# - if you want to build 32-bit version, you don't have to download Source2 and Source3
#   Just comment it out.
# - if you want to build 64-bit version, comment out Source0 and Source1

%define		vdir	%(echo %{version} | cut -f1-4 -d. | tr -d .)

Summary:	Oracle database client - common files
Summary(pl.UTF-8):	Klient bazy danych Oracle - wspólne pliki
Name:		oracle-instantclient-basic
Version:	19.10.0.0.0
Release:	0.1
License:	OTN (proprietary, re-distributable)
Group:		Applications/Databases
Source0:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-basic-linux-%{version}dbru.zip
# NoSource0-md5:	333d0ec0c3d390472de6c39c380e6f45
Source1:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-sdk-linux-%{version}dbru.zip
# NoSource1-md5:	076f8866146078ffe81353a857039b48
Source2:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-basic-linux.x64-%{version}dbru.zip
# NoSource2-md5:	88501585329ccbc7690aa20a105d2506
Source3:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-sdk-linux.x64-%{version}dbru.zip
# NoSource3-md5:	00aded152dcc2f26f4d8f44e6f7387d3
Source4:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-basic-linux.arm64-%{version}dbru.zip
# NoSource4-md5:	9898828fea2022366a812e13507b95f1
Source5:	https://download.oracle.com/otn_software/linux/instantclient/%{vdir}/instantclient-sdk-linux.arm64-%{version}dbru.zip
# NoSource5-md5:	ca2071b8734ed6d0c9805367d4076809
# http://duberga.net/dbd_oracle_instantclient_linux/oracle-instantclient-config
Source6:	oracle-instantclient-config.in
Source7:	oracle-instantclient.pc.in
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
NoSource:	4
NoSource:	5
URL:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html
BuildRequires:	sed
BuildRequires:	unzip
ExclusiveArch:	%{ix86} %{x8664} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_check_so	1
%define		no_install_post_strip		1

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
%setup -q -c -T -a 0 -a 1
%endif

%ifarch %{x8664}
%setup -q -c -T -a 2 -a 3
%endif

%ifarch aarch64
%setup -q -c -T -a 4 -a 5
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir}/sqlplus,%{_javadir}} \
	$RPM_BUILD_ROOT{%{_examplesdir}/%{name},%{_includedir}/oracle/client} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

cd instantclient_*

cp -p *.jar $RPM_BUILD_ROOT%{_javadir}
cp -pP *.so* $RPM_BUILD_ROOT%{_libdir}
cp -p genezi $RPM_BUILD_ROOT%{_bindir}/genezi
cp -p adrci $RPM_BUILD_ROOT%{_bindir}/adrci

%{__sed} -e 's|@@prefix@@|%{_prefix}|' \
	-e 's|@@libdir@@|%{_libdir}|' \
	-e 's|@@includedir@@|%{_includedir}/oracle/client|' \
	-e 's|@@version@@|%{version}|' %{SOURCE6} > \
		$RPM_BUILD_ROOT%{_bindir}/oracle-instantclient-config

%{__sed} -e 's|@@prefix@@|%{_prefix}|' \
	-e 's|@@libdir@@|%{_libdir}|' \
	-e 's|@@includedir@@|%{_includedir}/oracle/client|' \
	-e 's|@@version@@|%{version}|' %{SOURCE7} > \
		$RPM_BUILD_ROOT%{_pkgconfigdir}/oracle-instantclient.pc

cp -p sdk/ottclasses.zip $RPM_BUILD_ROOT%{_javadir}
cp -p sdk/ott $RPM_BUILD_ROOT%{_bindir}
cp -p sdk/include/* $RPM_BUILD_ROOT%{_includedir}/oracle/client
cp -p sdk/demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc instantclient_*/BASIC_{LICENSE,README}
%attr(755,root,root) %{_bindir}/adrci
%attr(755,root,root) %{_bindir}/genezi
%attr(755,root,root) %{_libdir}/libclntsh.so
%attr(755,root,root) %{_libdir}/libclntsh.so.*
%attr(755,root,root) %{_libdir}/libclntshcore.so.*
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libipc1.so
%attr(755,root,root) %{_libdir}/libmql1.so
%endif
%attr(755,root,root) %{_libdir}/libocci.so
%attr(755,root,root) %{_libdir}/libocci.so.*
%attr(755,root,root) %{_libdir}/libnnz19.so
%attr(755,root,root) %{_libdir}/libociei.so
%attr(755,root,root) %{_libdir}/libocijdbc19.so
%attr(755,root,root) %{_libdir}/liboramysql19.so
%{_javadir}/*.jar

%files devel
%defattr(644,root,root,755)
%doc instantclient_*/SDK_{LICENSE,README}
%attr(755,root,root) %{_bindir}/oracle-instantclient-config
%attr(755,root,root) %{_bindir}/ott
%{_pkgconfigdir}/oracle-instantclient.pc
%{_includedir}/oracle/client
%{_javadir}/*.zip
%{_examplesdir}/%{name}
