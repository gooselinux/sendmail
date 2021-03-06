# package options
%define with_tls	yes
%define with_sasl2	yes
%define with_milter	yes
%define with_ldap	yes
%define enable_pie	yes

%define sendmailcf %{_datadir}/sendmail-cf
%define stdir %{_localstatedir}/log/mail
%define smshell /sbin/nologin
%define spooldir %{_localstatedir}/spool
%define maildir %{_sysconfdir}/mail

Summary: A widely used Mail Transport Agent (MTA)
Name: sendmail
Version: 8.14.4
Release: 8%{?dist}
License: Sendmail
Group: System Environment/Daemons
URL: http://www.sendmail.org/
Source0: ftp://ftp.sendmail.org/pub/sendmail/sendmail.%{version}.tar.gz
Source1: sendmail.init
Source2: sendmail.nm-dispatcher
Source3: sendmail.etc-mail-make
Source4: sendmail.sysconfig
Source5: sendmail.etc-mail-Makefile
Source6: sendmail-redhat.mc
Source8: sendmail.pam
Source9: sendmail-8.12.5-newconfig.readme
Source11: Sendmail-sasl2.conf
Source12: sendmail-etc-mail-access
Source13: sendmail-etc-mail-domaintable
Source14: sendmail-etc-mail-local-host-names
Source15: sendmail-etc-mail-mailertable
Source16: sendmail-etc-mail-trusted-users
Source17: sendmail-etc-mail-virtusertable
Patch3: sendmail-8.14.4-makemapman.patch
Patch4: sendmail-8.14.3-smrsh_paths.patch
Patch7: sendmail-8.13.7-pid.patch
Patch9: sendmail-8.12.7-hesiod.patch
Patch10: sendmail-8.12.7-manpage.patch
Patch11: sendmail-8.14.4-dynamic.patch
Patch12: sendmail-8.13.0-cyrus.patch
Patch13: sendmail-8.14.4-aliases_dir.patch
Patch14: sendmail-8.13.7-vacation.patch
Patch15: sendmail-8.14.1-noversion.patch
Patch16: sendmail-8.13.1-localdomain.patch
Patch17: sendmail-8.14.3-sharedmilter.patch
Patch18: sendmail-8.14.4-switchfile.patch
Patch20: sendmail-8.14.3-milterfdleaks.patch
Patch21: sendmail-8.14.3-ipv6-bad-helo.patch
Patch23: sendmail-8.14.4-sasl2-in-etc.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: tcp_wrappers-devel
BuildRequires: db4-devel
BuildRequires: hesiod-devel
BuildRequires: groff
BuildRequires: ghostscript
BuildRequires: m4
Provides: MTA smtpdaemon server(smtp)
Provides: %{_sbindir}/sendmail %{_bindir}/mailq %{_bindir}/newaliases
Provides: %{_bindir}/rmail /usr/lib/sendmail
Provides: %{_sysconfdir}/pam.d/smtp
Provides: %{_mandir}/man1/mailq.1.gz %{_mandir}/man1/newaliases.1.gz
Provides: %{_mandir}/man5/aliases.5.gz %{_mandir}/man8/sendmail.8.gz
Requires(pre): shadow-utils
Requires(preun): %{_sbindir}/alternatives chkconfig
Requires(post): %{_sbindir}/alternatives chkconfig coreutils
Requires(postun): %{_sbindir}/alternatives coreutils
Requires: initscripts
Requires: procmail
Requires: bash >= 2.0
Requires: setup >= 2.5.31-1
BuildRequires: setup >= 2.5.31-1
%if "%{with_tls}" == "yes"
BuildRequires: openssl-devel
%endif
%if "%{with_sasl2}" == "yes"
BuildRequires: cyrus-sasl-devel openssl-devel
Requires: %{_sbindir}/saslauthd
%endif
%if "%{with_ldap}" == "yes"
BuildRequires: openldap-devel openssl-devel
%endif


%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your email. Sendmail is a
behind-the-scenes program which actually moves your email over
networks or the Internet to where you want it to go.

If you ever need to reconfigure Sendmail, you will also need to have
the sendmail-cf package installed. If you need documentation on
Sendmail, you can install the sendmail-doc package.

%package doc
Summary: Documentation about the Sendmail Mail Transport Agent program
Group: Documentation
BuildArch: noarch
Requires: sendmail = %{version}-%{release}

%description doc
The sendmail-doc package contains documentation about the Sendmail
Mail Transport Agent (MTA) program, including release notes, the
Sendmail FAQ, and a few papers written about Sendmail. The papers are
provided in PDF and troff formats.

%package devel
Summary: Extra development include files and development files
Group: Development/Libraries
Requires: sendmail = %{version}-%{release}
Requires: sendmail-milter = %{version}-%{release}

%description devel
Include files and devel libraries for e.g. the milter addons as part
of sendmail.

%package cf
Summary: The files needed to reconfigure Sendmail
Group: System Environment/Daemons
Requires: sendmail = %{version}-%{release}
BuildArch: noarch
Requires: m4

%description cf
This package includes the configuration files you need to generate the
sendmail.cf file distributed with the sendmail package. You will need
the sendmail-cf package if you ever need to reconfigure and rebuild
your sendmail.cf file.

%package milter
Summary: The sendmail milter library
Group: System Environment/Libraries

%description milter
The sendmail Mail Filter API (Milter) is designed to allow third-party
programs access to mail messages as they are being processed in order to
filter meta-information and content.

This package includes the milter shared library.

%prep
%setup -q

%patch3 -p1 -b .makemapman
%patch4 -p1 -b .smrsh_paths
%patch7 -p1 -b .pid
%patch9 -p1 -b .hesiod
%patch10 -p1 -b .manpage
%patch11 -p1 -b .dynamic
%patch12 -p1 -b .cyrus
%patch13 -p1 -b .aliases_dir
%patch14 -p1 -b .vacation
%patch15 -p1 -b .noversion
%patch16 -p1 -b .localdomain

cp devtools/M4/UNIX/{,shared}library.m4
%patch17 -p1 -b .sharedmilter

%patch18 -p1 -b .switchfile
%patch20 -p1 -b .milterfdleaks
%patch21 -p1 -b .ipv6-bad-helo
%patch23 -p1 -b .sasl2-in-etc

for f in RELEASE_NOTES contrib/etrn.0; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
# generate redhat config file
cat > redhat.config.m4 << EOF
define(\`confMAPDEF', \`-DNEWDB -DNIS -DHESIOD -DMAP_REGEX -DSOCKETMAP -DNAMED_BIND=1')
define(\`confOPTIMIZE', \`\`\`\`${RPM_OPT_FLAGS}'''')
define(\`confENVDEF', \`-I%{_includedir}/db4 -I/usr/kerberos/include -Wall -DXDEBUG=0 -DTCPWRAPPERS -DNETINET6 -DHES_GETMAILHOST -DUSE_VENDOR_CF_PATH=1 -D_FFR_TLS_1')
define(\`confLIBDIRS', \`-L/usr/kerberos/%{_lib}')
define(\`confLIBS', \`-lnsl -lwrap -lhesiod -lcrypt -ldb -lresolv')
define(\`confMANOWN', \`root')
define(\`confMANGRP', \`root')
define(\`confMANMODE', \`644')
define(\`confMAN1SRC', \`1')
define(\`confMAN5SRC', \`5')
define(\`confMAN8SRC', \`8')
define(\`confSTDIR', \`%{stdir}')
define(\`STATUS_FILE', \`%{stdir}/statistics')
define(\`confLIBSEARCH', \`db resolv 44bsd')
EOF
#'

cat >> redhat.config.m4 << EOF
%ifarch ppc ppc64 s390x
APPENDDEF(\`confOPTIMIZE', \`-DSM_CONF_SHM=0')
%else
APPENDDEF(\`confOPTIMIZE', \`')
%endif
EOF

%if "%{enable_pie}" == "yes"
%ifarch s390 s390x sparc sparcv9 sparc64
%define _fpie -fPIE
%else
%define _fpie -fpie
%endif
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confOPTIMIZE', \`%{_fpie}')
APPENDDEF(\`confLIBS', \`-pie')
EOF
%endif

%if "%{with_tls}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DSTARTTLS')dnl
APPENDDEF(\`conf_sendmail_LIBS', \`-lssl -lcrypto')dnl
EOF
%endif

%if "%{with_sasl2}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confENVDEF', \`-DSASL=2')dnl
APPENDDEF(\`confLIBS', \`-lsasl2 -lcrypto')dnl
EOF
%endif

%if "%{with_milter}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DMILTER')dnl
EOF
%endif

%if "%{with_ldap}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confMAPDEF', \`-DLDAPMAP -DLDAP_DEPRECATED')dnl
APPENDDEF(\`confENVDEF', \`-DSM_CONF_LDAP_MEMFREE=1')dnl
APPENDDEF(\`confLIBS', \`-lldap -llber -lssl -lcrypto')dnl
EOF
%endif

DIRS="libsmutil sendmail mailstats rmail praliases smrsh makemap"

%if "%{with_milter}" == "yes"
DIRS="libmilter $DIRS"
%endif

for i in $DIRS; do
	pushd $i
	sh Build -f ../redhat.config.m4
	popd
done

make -C doc/op op.pdf

%install
rm -rf %{buildroot}

# create directories
for d in %{_bindir} %{_sbindir} %{_includedir}/libmilter \
	%{_libdir} %{_mandir}/man{1,5,8} %{maildir} %{stdir} %{spooldir} \
	%{_docdir}/sendmail-%{version} %{sendmailcf} %{_sysconfdir}/smrsh\
	%{spooldir}/clientmqueue %{_sysconfdir}/sysconfig %{_initrddir} \
	%{_sysconfdir}/pam.d %{_docdir}/sendmail-%{version}/contrib \
	%{_sysconfdir}/NetworkManager/dispatcher.d
do
	install -m 755 -d %{buildroot}$d
done
install -m 700 -d %{buildroot}%{spooldir}/mqueue

# create /usr/lib for 64 bit architectures
%if "%{_libdir}" != "/usr/lib"
install -m 755 -d %{buildroot}/usr/lib
%endif

nameuser=`id -nu`
namegroup=`id -ng`

Make() {
	make $@ \
		DESTDIR=%{buildroot} \
		LIBDIR=%{_libdir} \
		MANROOT=%{_mandir}/man \
		LIBMODE=0755 INCMODE=0644 \
		SBINOWN=${nameuser} SBINGRP=${namegroup} \
		UBINOWN=${nameuser} UBINGRP=${namegroup} \
		MANOWN=${nameuser} MANGRP=${namegroup} \
		INCOWN=${nameuser} INCGRP=${namegroup} \
		LIBOWN=${nameuser} LIBGRP=${namegroup} \
		GBINOWN=${nameuser} GBINGRP=${namegroup} \
		CFOWN=${nameuser} CFGRP=${namegroup} \
		CFMODE=0644 MSPQOWN=${nameuser}
}

OBJDIR=obj.$(uname -s).$(uname -r).$(uname -m)

Make install -C $OBJDIR/libmilter
Make install -C $OBJDIR/sendmail
Make install -C $OBJDIR/mailstats
Make force-install -C $OBJDIR/rmail
Make install -C $OBJDIR/praliases
Make install -C $OBJDIR/smrsh
Make install -C $OBJDIR/makemap

# replace absolute with relative symlinks
ln -sf ../sbin/makemap %{buildroot}%{_bindir}/makemap
for f in hoststat mailq newaliases purgestat ; do
	ln -sf ../sbin/sendmail.sendmail %{buildroot}%{_bindir}/${f}
done

# use /usr/lib, even for 64 bit architectures
ln -sf ../sbin/sendmail.sendmail %{buildroot}/usr/lib/sendmail.sendmail

# install docs for sendmail
install -p -m 644 FAQ %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 KNOWNBUGS %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 LICENSE %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 README %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 RELEASE_NOTES %{buildroot}%{_docdir}/sendmail-%{version}
gzip -9 %{buildroot}%{_docdir}/sendmail-%{version}/RELEASE_NOTES

# install docs for sendmail-doc
install -m 644 doc/op/op.pdf %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 sendmail/README %{buildroot}%{_docdir}/sendmail-%{version}/README.sendmail
install -p -m 644 sendmail/SECURITY %{buildroot}%{_docdir}/sendmail-%{version}
install -p -m 644 smrsh/README %{buildroot}%{_docdir}/sendmail-%{version}/README.smrsh
install -p -m 644 libmilter/README %{buildroot}%{_docdir}/sendmail-%{version}/README.libmilter
install -p -m 644 cf/README %{buildroot}%{_docdir}/sendmail-%{version}/README.cf
install -m 644 %{SOURCE9} %{buildroot}%{_docdir}/sendmail-%{version}/README.redhat
install -p -m 644 contrib/* %{buildroot}%{_docdir}/sendmail-%{version}/contrib
sed -i 's|/usr/local/bin/perl|%{_bindir}/perl|' %{buildroot}%{_docdir}/sendmail-%{version}/contrib/*.pl

# install the cf files for the sendmail-cf package.
cp -ar cf/* %{buildroot}%{sendmailcf}
# remove patch backup files
rm -rf %{buildroot}%{sendmailcf}/cf/Build.*
rm -rf %{buildroot}%{sendmailcf}/*/*.mc.*
rm -rf %{buildroot}%{sendmailcf}/*/*.m4.*

# install sendmail.mc with proper paths
install -m 644 %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc
sed -i -e 's|@@PATH@@|%{sendmailcf}|' %{buildroot}%{maildir}/sendmail.mc
touch -r %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc

# create sendmail.cf
cp %{buildroot}%{maildir}/sendmail.mc cf/cf/redhat.mc
sed -i -e 's|%{sendmailcf}|\.\.|' cf/cf/redhat.mc
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' cf/cf/redhat.mc
%endif
(cd cf/cf && m4 redhat.mc > redhat.cf)
install -m 644 cf/cf/redhat.cf %{buildroot}%{maildir}/sendmail.cf
install -p -m 644 cf/cf/submit.mc %{buildroot}%{maildir}/submit.mc

# remove our build info as it causes multiarch conflicts
sed -i '/##### built by.*on/,+3d' %{buildroot}%{maildir}/{submit,sendmail}.cf \
	%{buildroot}%{sendmailcf}/cf/submit.cf

install -p -m 644 %{SOURCE12} %{buildroot}%{maildir}/access
install -p -m 644 %{SOURCE13} %{buildroot}%{maildir}/domaintable
install -p -m 644 %{SOURCE14} %{buildroot}%{maildir}/local-host-names
install -p -m 644 %{SOURCE15} %{buildroot}%{maildir}/mailertable
install -p -m 644 %{SOURCE16} %{buildroot}%{maildir}/trusted-users
install -p -m 644 %{SOURCE17} %{buildroot}%{maildir}/virtusertable

# create db ghosts
for map in virtusertable access domaintable mailertable ; do
	touch %{buildroot}%{maildir}/${map}.db
	chmod 0644 %{buildroot}%{maildir}/${map}.db
done

touch %{buildroot}%{maildir}/aliasesdb-stamp

install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/sendmail
install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/sendmail
install -p -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail
install -p -m 755 %{SOURCE3} %{buildroot}%{maildir}/make
install -p -m 644 %{SOURCE5} %{buildroot}%{maildir}/Makefile

chmod 644 %{buildroot}%{maildir}/helpfile

# fix permissions to allow debuginfo extraction and stripping
chmod 755 %{buildroot}%{_sbindir}/{mailstats,makemap,praliases,sendmail,smrsh}
chmod 755 %{buildroot}%{_bindir}/rmail

%if "%{with_sasl2}" == "yes"
install -m 755 -d %{buildroot}%{_sysconfdir}/sasl2
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sasl2/Sendmail.conf
%endif
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/smtp.sendmail

# fix path for statistics file in man pages
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' %{buildroot}%{_mandir}/man*/*
%endif

# rename files for alternative usage
mv %{buildroot}%{_sbindir}/sendmail %{buildroot}%{_sbindir}/sendmail.sendmail
for i in mailq newaliases rmail; do
	mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i.sendmail
done
mv %{buildroot}%{_mandir}/man1/mailq.1 %{buildroot}%{_mandir}/man1/mailq.sendmail.1
mv %{buildroot}%{_mandir}/man1/newaliases.1 %{buildroot}%{_mandir}/man1/newaliases.sendmail.1
mv %{buildroot}%{_mandir}/man5/aliases.5 %{buildroot}%{_mandir}/man5/aliases.sendmail.5
mv %{buildroot}%{_mandir}/man8/sendmail.8 %{buildroot}%{_mandir}/man8/sendmail.sendmail.8


%clean
rm -rf %{buildroot}

%pre
getent group mailnull >/dev/null || \
  %{_sbindir}/groupadd -g 47 -r mailnull >/dev/null 2>&1
getent passwd mailnull >/dev/null || \
  %{_sbindir}/useradd -u 47 -g mailnull -d %{spooldir}/mqueue -r \
  -s %{smshell} mailnull >/dev/null 2>&1
getent group smmsp >/dev/null || \
  %{_sbindir}/groupadd -g 51 -r smmsp >/dev/null 2>&1
getent passwd smmsp >/dev/null || \
  %{_sbindir}/useradd -u 51 -g smmsp -d %{spooldir}/mqueue -r \
  -s %{smshell} smmsp >/dev/null 2>&1
exit 0

%postun
if [ "$1" -ge "1" ]; then
	%{_initrddir}/sendmail condrestart >/dev/null 2>&1
	mta=`readlink %{_sysconfdir}/alternatives/mta`
	if [ "$mta" == "%{_sbindir}/sendmail.sendmail" ]; then
		%{_sbindir}/alternatives --set mta %{_sbindir}/sendmail.sendmail
	fi
fi
exit 0

%post
/sbin/chkconfig --add sendmail
# Set up the alternatives files for MTAs.
%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.sendmail 90 \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.sendmail \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.sendmail \
	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.sendmail \
	--slave /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.sendmail \
	--slave %{_sysconfdir}/pam.d/smtp mta-pam %{_sysconfdir}/pam.d/smtp.sendmail \
	--slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man8/sendmail.sendmail.8.gz \
	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/mailq.sendmail.1.gz \
	--slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man1/newaliases.sendmail.1.gz \
	--slave %{_mandir}/man5/aliases.5.gz mta-aliasesman %{_mandir}/man5/aliases.sendmail.5.gz \
	--initscript sendmail

# Rebuild maps
{
	chown root %{_sysconfdir}/aliases.db %{maildir}/access.db \
		%{maildir}/mailertable.db %{maildir}/domaintable.db \
		%{maildir}/virtusertable.db
	SM_FORCE_DBREBUILD=1 %{maildir}/make
	SM_FORCE_DBREBUILD=1 %{maildir}/make aliases
} > /dev/null 2>&1

# Move existing SASL2 config to new location.
%if "%{with_sasl2}" == "yes"
[ -f %{_libdir}/sasl2/Sendmail.conf ] && touch -r %{_sysconfdir}/sasl2/Sendmail.conf \
  %{_libdir}/sasl2/Sendmail.conf ] && mv -f %{_libdir}/sasl2/Sendmail.conf \
  %{_sysconfdir}/sasl2 2>/dev/null || :
%endif
exit 0

%preun
if [ $1 = 0 ]; then
	%{_initrddir}/sendmail stop >/dev/null 2>&1
	/sbin/chkconfig --del sendmail
	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.sendmail
fi
exit 0

%post milter -p /sbin/ldconfig

%postun milter -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_docdir}/sendmail-%{version}
%doc %{_docdir}/sendmail-%{version}/FAQ
%doc %{_docdir}/sendmail-%{version}/KNOWNBUGS
%doc %{_docdir}/sendmail-%{version}/LICENSE
%doc %{_docdir}/sendmail-%{version}/README
%doc %{_docdir}/sendmail-%{version}/RELEASE_NOTES.gz
%{_bindir}/hoststat
%{_bindir}/makemap
%{_bindir}/purgestat
%{_sbindir}/mailstats
%{_sbindir}/makemap
%{_sbindir}/praliases
%attr(2755,root,smmsp) %{_sbindir}/sendmail.sendmail
%{_bindir}/rmail.sendmail
%{_bindir}/newaliases.sendmail
%{_bindir}/mailq.sendmail
%{_sbindir}/smrsh
/usr/lib/sendmail.sendmail

%{_mandir}/man8/rmail.8.gz
%{_mandir}/man8/praliases.8.gz
%{_mandir}/man8/mailstats.8.gz
%{_mandir}/man8/makemap.8.gz
%{_mandir}/man8/sendmail.sendmail.8.gz
%{_mandir}/man8/smrsh.8.gz
%{_mandir}/man5/aliases.sendmail.5.gz
%{_mandir}/man1/newaliases.sendmail.1.gz
%{_mandir}/man1/mailq.sendmail.1.gz

%dir %{stdir}
%dir %{_sysconfdir}/smrsh
%dir %{maildir}
%attr(0770,smmsp,smmsp) %dir %{spooldir}/clientmqueue
%attr(0700,root,mail) %dir %{spooldir}/mqueue

%config(noreplace) %verify(not size mtime md5) %{stdir}/statistics
%config(noreplace) %{maildir}/Makefile
%config(noreplace) %{maildir}/make
%config(noreplace) %{maildir}/sendmail.cf
%config(noreplace) %{maildir}/submit.cf
%config(noreplace) %{maildir}/helpfile
%config(noreplace) %{maildir}/sendmail.mc
%config(noreplace) %{maildir}/submit.mc
%config(noreplace) %{maildir}/access
%config(noreplace) %{maildir}/domaintable
%config(noreplace) %{maildir}/local-host-names
%config(noreplace) %{maildir}/mailertable
%config(noreplace) %{maildir}/trusted-users
%config(noreplace) %{maildir}/virtusertable

%ghost %{maildir}/aliasesdb-stamp
%ghost %{maildir}/virtusertable.db
%ghost %{maildir}/access.db
%ghost %{maildir}/domaintable.db
%ghost %{maildir}/mailertable.db

%{_initrddir}/sendmail
%config(noreplace) %{_sysconfdir}/sysconfig/sendmail
%config(noreplace) %{_sysconfdir}/pam.d/smtp.sendmail
%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail

%if "%{with_sasl2}" == "yes"
%config(noreplace) %{_sysconfdir}/sasl2/Sendmail.conf
%endif

%files cf
%defattr(-,root,root,-)
%doc %{sendmailcf}/README
%dir %{sendmailcf}
%{sendmailcf}/cf
%{sendmailcf}/domain
%{sendmailcf}/feature
%{sendmailcf}/hack
%{sendmailcf}/m4
%{sendmailcf}/mailer
%{sendmailcf}/ostype
%{sendmailcf}/sendmail.schema
%{sendmailcf}/sh
%{sendmailcf}/siteconfig

%files devel
%defattr(-,root,root,-)
%doc libmilter/docs/*
%dir %{_includedir}/libmilter
%{_includedir}/libmilter/*.h
%{_libdir}/libmilter.so

%files milter
%defattr(-,root,root,-)
%{_libdir}/libmilter.so.[0-9].[0-9]
%{_libdir}/libmilter.so.[0-9].[0-9].[0-9]

%files doc
%defattr(-,root,root,-)
%{_docdir}/sendmail-%{version}/README.cf
%{_docdir}/sendmail-%{version}/README.libmilter
%{_docdir}/sendmail-%{version}/README.redhat
%{_docdir}/sendmail-%{version}/README.sendmail
%{_docdir}/sendmail-%{version}/README.smrsh
%{_docdir}/sendmail-%{version}/SECURITY
%{_docdir}/sendmail-%{version}/op.pdf
%dir %{_docdir}/sendmail-%{version}/contrib
%attr(0644,root,root) %{_docdir}/sendmail-%{version}/contrib/*


%changelog
* Thu Jun 17 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-8
- sasl2 config moved from {_libdir}/sasl2 to {_sysconfdir}/sasl2

* Wed May 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-7
- fixed user/group creation (#594394)
- fixed changelog

* Fri Mar 05 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-6
- reverted from ghost to explicit provides

* Tue Mar 02 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-5
- used noreplace for sasl config
- used ghost instead of explicit provides
- deffattr changed to (-,root,root,-)

* Mon Feb 15 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-4
- release increased due to wrong tags in CVS

* Mon Feb 15 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-3
- fixed libresolv implicit DSO linking (#564647)
- fixed initscript LSB compliance (#561040)

* Thu Feb 04 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-2
- fixed typo in spec file
- fixed aliases_dir patch

* Tue Feb 02 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-1
- new version 8.14.4 (#552078)
- RPM attributes S, 5, T not recorded for statistics file
- adapted patches: makemapman, dynamic, switchfile (#552078)
- movefiles patch incorporated into aliases_dir patch
- dropped patches (fixed upstream): exitpanic, certcnnul

* Fri Jan 08 2010 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-10
- fix verification of SSL certificate with NUL in name (#553390, CVE-2009-4565)
- don't start service by default (#529686)

* Sun Jan 03 2010 Robert Scheck <robert@fedoraproject.org> 8.14.3-10
- handle IPv6:::1 in block_bad_helo.m4 like 127.0.0.1 (#549217)

* Tue Dec 15 2009 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-9
- fix milter file descriptors leaks (#485426)
- skip colon separator when parsing service name in ServiceSwitchFile
- return with non-zero exit code when free space is below MinFreeBlocks
- fix service stop/restart when only smclient is running
- fix submit.cf and helpfile permissions
- more merge review fixes (#226407)

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 8.14.3-8
- Use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 8.14.3-7
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-4
- build shared libmilter (#309281)
- drop static libraries
- convert RELEASE_NOTES to UTF-8

* Fri Dec 19 2008 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-3
- run newaliases only when necessary

* Wed Dec 03 2008 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-2
- add NM dispatcher script (#451575)
- print warning on service start when sendmail-cf is required (#447148)
- replace Makefile with shell script to avoid dependency on make (#467841)
- fix multiarch conflicts (#343161)
- preserve timestamps on config files
- gzip RELEASE_NOTES
- defuzz patches
- drop gcc2690 patch

* Tue Jul 22 2008 Thomas Woerner <twoerner@redhat.com> 8.14.3-1
- new version 8.14.3

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 8.14.2-5
- rebuild against db4-4.7

* Sat Mar 29 2008 Dennis Gilmore <dennis@ausil.us> 8.14.2-4
- add sparcv9 to the -fPIE list 

* Fri Feb  8 2008 Thomas Woerner <twoerner@redhat.com> 8.14.2-3
- added server(smtp) provide (rhbz#380621)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 8.14.2-2
 - Rebuild for deps

* Thu Nov 22 2007 Thomas Woerner <twoerner@redhat.com> 8.14.2-1
- new version 8.14.2

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4.2
- made init script fully lsb conform

* Wed Aug 29 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4.1
- fixed condrestart in init script to use exit instead of return

* Mon Aug 27 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4
- do not remove /etc/aliases.db on package removal (rhbz#223637)
- fixed remaining paths to certs directory in sendmail.mc file
- added contrib scripts to the doc package (rhbz#183723)
- added LSB header to init script (rhbz#247053)
- added plain login information for cyrus-sasl to access file
- fixed compile problem with glibc-2.6.90+
- fixed reoccuring m4 include problem (now using sinclude)

* Fri Jul 20 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-3
- do not accept localhost.localdomain as valid address from smtp

* Mon Apr 16 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-2
- readded chkconfig add for sendmail in post script
- dropped mysql support (useless without further patching)
- fixed executable permissions for /usr/sbin/makemap and /usr/sbin/smrsh
- dropped FFR_UNSAFE_SASL, because it has no effect anymore

* Thu Apr 12 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-1.1
- replaced prereq tags with requires() tags.

* Thu Apr 12 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-1
- new version 8.14.1
- spec file cleanup for merge review (rhbz#226407)
- dropped update support for sendmail versions prior to 8.12.0
- using pdf documentation

* Tue Feb  6 2007 Thomas Woerner <twoerner@redhat.com> 8.14.0-1
- new version 8.14.0
- adapted patches: makemapman, dynamic

* Tue Jan 23 2007 Florian La Roche <laroche@redhat.com>
- #205803 add sparc/sparc64 to -fPIE list
- change sendmail.cf reference into sendmail-cf package name

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-3.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Tue Nov 28 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-3
- added missing LDAP_DEPRECATED flag (#206288)

* Mon Sep 04 2006 Florian La Roche <laroche@redhat.com>
- unify sendmail.mc
- remove version information from sendmail helpfile

* Fri Sep  1 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-1
- new version 8.13.8 fixes CVE-2006-4434 (denial of service via a long header
  line)

* Thu Jul 20 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-3.1
- dropped chown of /etc/mail/authinfo.db (#199455)

* Tue Jul 18 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-3
- using new syntax for access database (#177566)
- fixed failure message while shutting down sm-client (#119429)
  resolution: stop sm-client before sendmail
- fixed method to specify persistent queue runners (#126760)
- removed patch backup files from sendmail-cf tree (#152955)
- fixed missing dnl on SMART_HOST define (#166680)
- fixed wrong location of aliases and aliases.db file in aliases man page
  (#166744)
- enabled CipherList config option for sendmail (#172352)
- added user chowns for /etc/mail/authinfo.db and move check for cf files
  (#184341)
- fixed Makefile of vacation (#191396)
  vacation is not included in this sendmail package
- /var/log/mail now belongs to sendmail (#192850)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.13.7-2.1
- rebuild

* Mon Jun 19 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-2
- dropped reference to Red Hat Linux in sendmail-redhat.mc (#176679)

* Mon Jun 19 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-1
- new version 8.13.7 (#195282)
- fixes CVE-2006-1173 (VU#146718): possible denial of service issue caused by
  malformed multipart messages (#195776)

* Wed Mar 22 2006 Thomas Woerner <twoerner@redhat.com> 8.13.6-1
- new version 8.13.6 (fixes VU#834865)
- dropped libmilter-sigwait patch (fixed in 8.13.6)

* Fri Feb 17 2006 Thomas Woerner <twoerner@redhat.com> 8.13.5-3
- fixed selinuxenabled path in initscript
- fixed error handling with sigwait (#137709)
  Thanks to Jonathan Kamens for the patch
- fixed prereq for cyrus-sasl: now using /usr/sbin/saslauthd
- appended 'dnl' to cert tags in sendmail.mc

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.13.5-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.13.5-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 8.13.5-2
- rebuilt against new openssl

* Mon Oct 10 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Mon Sep 19 2005 Thomas Woerner <twoerner@redhat.com> 8.13.5-1
- new version 8.13.5
- fixed email address in changelog

* Fri May  6 2005 Thomas Woerner <twoerner@redhat.com> 8.13.4-2
- using new certificates directory /etc/pki/tls/certs

* Wed Apr 27 2005 Thomas Woerner <twoerrner@redhat.com> 8.13.4-1.1
- added configuration example for Cyrus-IMAPd to sendmail.mc (#142001)
  Thanks to Alexander Dalloz

* Tue Apr 12 2005 Thomas Woerner <twoerner@redhat.com> 8.13.4-1
- new version 8.13.4
- added requires for the sendmail base package in sendmail-cf, sendmail-devel
  and sendmail-doc
- dropped upstream close_wait.p2 patch

* Thu Mar 17 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-2
- dropped direct support for bind: no bind in confLIBSEARCH anymore,
  using libresolv again

* Wed Mar 10 2005 Jason Vas Dias <jvdias@redhat.com> 8.13.3-1.2
- fix libbind include path - use /usr/include/bind/netdb.h, no
- /usr/include/netdb.h - bug: 150339

* Tue Mar  1 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-1.1
- fixed gcc4 build: use double quotes for confOPTIMIZE to avoid m4 confusion
  with ','
- fix for ppc: using tripple-quotes

* Wed Jan 26 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-1
- new version 8.13.3 with closewait.p2 patch

* Fri Dec 17 2004 Thomas Woerner <twoerner@redhat.com> 8.13.2-1
- new version 8.13.2
- thanks to Robert Scheck for adapting the patches

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 8.13.1-2.2
- rebuild against db-4.3.21.

* Tue Oct 26 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-2.1
- added missing BuildRequires for groff (#134778)
- added socketmap support (#131906)

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-2
- applied Sendmail Errata (2004-08-24): errata_cataddr (#131179)

* Mon Aug  2 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-1
- new version 1.13.1

* Wed Jun 30 2004 Thomas Woerner <twoerner@redhat.com> 8.13.0-1.1
- fixed init script to not complain missing sendmail-cf package (#126975)
- better message in /etc/mail/Makefile for missing sendmail-cf package.

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 8.13.0-1
- new version 8.13.0
- made /etc/mail/Makefile complain missing sendmail-cf package (#123348)
- fixed ownership of %%{_includedir}/libmilter (#73977)
- moved back to /usr/share/ssl/certs as certificate directory (see sendmail.mc)
- extended sendmail.mc for spam protection

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  15 2004 Dan Walsh <dwalsh@redhat.com> 8.12.11-4.6
- Fix selinuxenabled location

* Wed Apr  7 2004 Dan Walsh <dwalsh@redhat.com> 8.12.11-4.5
- Fix security context of pid file for selinux

* Fri Apr  2 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.4
- fixed alternatives slave for sendmail.sendmail

* Thu Apr  1 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.3
- set path to cyrus-imapd deliver

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.2
- fixed spec file

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.1
- added authinfo to possible sendmail maps: /etc/mail/Makefile (#119010)
- fixed minor version in changelog

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4
- new slave in alternatives for sendmail man page

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-3.2
- removed buildreq for gdbm-devel

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-3
- RH3.0E version: sasl1, no pie, old_setup (provide /etc/aliases)
- new switches for pie and old_setup

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-2.1
- new Sendmail.conf for sasl1 (#114726)

* Wed Jan 28 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-2
- added information for saslauthd and AUTH (#113463)
- fixed STATUS_FILE in sendmail-redhat.mc (#114302)
- reset mta after update if mta was sendmail (#114257)
- enabled pie for ia64 again

* Mon Jan 26 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.3
- removed /etc/aliases (now in setup)

* Thu Jan 22 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.2
- /usr/lib/sendmail is in alternatives, now
- removed trailing / from stdir
- fixed define for STATUS_FILE

* Wed Jan 21 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.1
- disabled pie for ia64

* Tue Jan 20 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1
- new version 8.12.11
- pie

* Mon Jan 12 2004 Thomas Woerner <twoerner@redhat.com> 8.12.10-7
- fc2 version (with sasl2)

* Mon Jan 12 2004 Thomas Woerner <twoerner@redhat.com> 8.12.10-6
- reverted to sasl1 for 3.0E: added with_sasl1
- spec file cleanup
- new location for statistics file (/var/log/)

* Sun Dec 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- Fix download url.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 8.12.10-5
- rebuild against db-4.2.52.
 
* Thu Dec 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix pam alternatives handling
- add patch from Jakub Jelinek for PIE

* Fri Dec 05 2003 Karsten Hopp <karsten@redhat.de> 8.12.10-3
- fix usage of RPM_OPT_FLAGS variable in spec file
- add makecert.sh script to -doc subpackage
- add cert paths to sendmail.mc

* Wed Nov 26 2003 Karsten Hopp <karsten@redhat.de> 
- fix alternatives (#109313)
- enable TLS

* Mon Oct 27 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add some more system account entries into /etc/aliases
- add example for a mixed IPv6/IPv4 setup

* Fri Oct 24 2003 Harald Hoyer <harald@redhat.de> 8.12.10-2
- added with_ options

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 8.12.10-1.2
- rebuild against db-4.2.42.
 
* Thu Sep 18 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.10

* Wed Sep 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add security patches for CAN-2003-0694 and CAN-2003-0681

* Mon Sep 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- move debug information from sendmail into debuginfo rpm
- on %%post make sure /etc/aliases.db and /etc/mail/*.db is correctly
  owned by root
- do not set confTRUSTED_USER to smmsp in sendmail-redhat.mc

* Fri Aug 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- run "make -C /etc/mail" (maybe generating new sendmail.cf, then newaliases
- added $SENDMAIL_OPTARG that could be set by /etc/sysconfig/sendmail #99224

* Wed Jul 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust rpm license tag to say "Sendmail"

* Fri Jul 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- enable pie only for a few archs
- enable full optims for s390 again, compiler seems to be fixed

* Mon Jun 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- apply patch from Ulrich Drepper to support -pie

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 31 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- make init script more robust #91879

* Sun May 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sendmail-cf requires m4, #90513

* Fri May  9 2003 Nalin Dahyabhai <nalin@redhat.com> 8.12.9-6
- move Sendmail.conf from /usr/lib/sasl to /usr/lib/sasl2 and change the
  default pwcheck method to "saslauthd"

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 8.12.9-5
- configure to use libsasl2 instead of libsasl to avoid linking with both
  (we also link to libldap, which now uses libsasl2)
- link with -ldb instead of -ldb-4.0 on all releases after RHL 7.3 instead
  of just 7.3 (all versions of db4-devel thereafter are expected to provide
  the right linking setup)

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add a "umask 022" before building the *.cf files in /etc/mail/Makefile

* Fri Apr 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- mark /etc/mail/Makefile as config(noreplace) #87688
- mark /etc/pam.d/smtp as config(noreplace) #87731

* Sun Mar 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.9

* Wed Mar 26 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- call make with the target "all" #86005
- add start/stop/restart as Makefile targets
- add another security patch

* Wed Mar 05 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add correct db4-devel requirements for newer releases
- completely re-do many ifdef code in the spec-file
- fix some issues building for older RHL releases

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.8

* Tue Feb 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add a confTRUSTED_USER line into sendmail.mc, submit.mc is already ok
- add patch from sendmail.org for cf/m4/proto.m4

* Mon Jan 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not reject all numeric login names if hesiod support is
  compiled in. #80060
- remove reference to non-existing man-pages #74552

* Sun Jan 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sendmail-8.12.7-etrn.patch from Jos Vos <jos@xos.nl>
- submit.mc: enable "use_ct_file" by default  #80519
- add _FFR_MILTER_ROOT_UNSAFE  #78223

* Sat Jan 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.7
- hack to make lib64 version work
- downgrade s390 optims to make it compile

* Mon Jan  6 2003 Nalin Dahyabhai <nalin@redhat.com>
- add openssl-devel as a build-time requirement
- preprocess the config file to add the right version of %%{_lib}
- add kerberos -I and -L flags to build configuration, needed for newer
  versions of libssl

* Wed Dec 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- always have a queue run interval for sm-msp-queue   #81424
- Jos Vos suggests adding another variable for sm-client queue-run

* Mon Dec 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add the following changes from Adrian Havill <havill@redhat.com>
  to our default sendmail.mc file:
	- added commented-out-by-default common AUTH/SSL examples
	- updated m4 example and rpm reference
	- added more comment documentation
	- add commented out confAUTO_REBUILD example
	- improve description about MASQUERADE_AS

* Mon Nov 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add to submit.mc: define(`_MTA_HOST_', `[127.0.0.1]')
  to deliver directly to localhost IP instead of going through DNS
- submit.mc: exchange msp and use_ct_file to better enable it
- do not undefine UUCP_RELAY and BITNET_RELAY
- sendmail.mc: use LOCAL_DOMAIN instead of "Cw" directly
- sendmail.mc: add commented out MASQUERADE_AS example
- re-enable DAEMON variable for now

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- remove absolute path names from the PAM configuration, allowing it to be
  used by any arch on a multilib system

* Sun Nov 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix mailman alias  #75129

* Sat Nov 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.6

* Fri Oct 04 2002 Phil Knirsch <pknirsch@redhat.com> 8.12.5-7.2
- Drop optflags to default to build correctly on s390(x).

* Thu Sep 12 2002 Than Ngo <than@redhat.com> 8.12.5-7.1
- Added fix to build on x86_64

* Thu Aug 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- clean up some specfile cruft
- add more pseudo accounts to /etc/aliases

* Thu Jul 25 2002 Phil Knirsch <pknirsch@redhat.com>
- Only generate new cf files if the /usr/share/sendmail-cf/m4/cf.m4 exists.

* Wed Jul 24 2002 Phil Knirsch <pknirsch@redhat.com>
- Changed the behaviour in /etc/mail/Makefile to generate the sendmail.cf and
  submit.cf from the mc files if they changed.
- Added a small README.redhat that descibed the new mc file behaviour and the
  split into sendmail.cf and submit.cf.

* Wed Jul 24 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- suggestions form Stephane Lentz:
	- add correct include statement into submit.mc (like sendmail.mc)
	- add commented out further suggestions into submit.mc
	- disable ident lookups

* Thu Jul 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix initscript for the second daemon and pidfile location #67910

* Mon Jul 01 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.5

* Thu Jun 27 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add further queue runs, slight spec-file cleanups

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.4, adjust smrsh patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Apr 13 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.3

* Tue Mar 26 2002 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Mar 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix alternatives --remove  #61737
- add sendmail/SECURITY as docu #61870, #61545

* Wed Mar 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add libsm.a #61270
- change from /etc/sendmail.cf to /etc/mail/sendmail.cf
- add milter patch

* Wed Mar 13 2002 Bill Nottingham <notting@redhat.com>
- ignore DAEMON=no; that configuration no longer functions

* Wed Mar 13 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- make sure more version information is in the cf file #54418
- do not use "-b" flag when patching in spec file
- require newer chkconfig version #61035
- fix preun script #60880
- add TMPF to access file creation #60956

* Sat Mar 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- mv include files to /usr/include/libmilter/ #60795
- do not use "-f" option to virtusertable #60196
- ad an example smarthost entry to config file #58298

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com> 8.12.2-5
- use alternatives --initscript support
- run chkconfig --add before alternatives

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 8.12.2-3
- run alternatives --remove in %%preun
- add some prereqs

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 8.12.2-2
- fix smmsp useradd invocation in %%pre
- switch back to db3 for storing db files

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 8.12.2-1
- update to 8.12.2 (adds STARTTLS support without need for sfio)
- don't forcibly strip binaries; let the build root handle it
- add creation of the smmsp account (51/51) in %%pre
- enable hesiod map support
- modify default config to use an MSP
- comment out 'O AutoRebuildAliases' in %%post, otherwise sendmail will
  fail to restart on upgrades

* Wed Feb 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ifdefs around new alternative stuff to also be able
  to build this for older releases

* Fri Feb  1 2002 Bill Nottingham <notting@redhat.com> 8.11.6-12
- %%triggerpostun on older versions to make sure alternatives work on
  upgrades

* Thu Jan 31 2002 Bill Nottingham <notting@redhat.com> 8.11.6-11
- clean up alternatives somewhat, provide /usr/sbin/sendmail & friends

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 8.11.6-10
- Use alternatives

* Tue Jan 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix quotation in spec-file

* Thu Jan 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- integrate ugly logic to compile this src.rpm also on older Red Hat
  Linux releases
- clean up spec file and patches a bit
- add db4 support

* Wed Jan 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix another path to correct docu
- include sendmail/README in the docu
- compile with -D_FFR_WORKAROUND_BROKEN_NAMESERVERS, but do not
  enable this at runtime
- devel subpackage files owned by root now

* Fri Dec 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change "-q" to "-s" as option to make #57216
- move milter lib into separate "devel" sub-package
- add include files to devel sub-package #56064
- fix pointer in access file to docu #54351

* Mon Sep 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libmilter docu
- add support for userdb to /etc/mail/Makefile
- use "btree" database files if a userdb is used
- buildrequires tcp_wrappers

* Fri Aug 31 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix libmilter support
- fix init script to use /etc/mail/Makefile #52932

* Sat Aug 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libmilter library

* Thu Aug 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.6
- correctly use /etc/mail/statistics

* Thu Aug 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change init script back to older conventions #51297
- remove DoS patch, not needed anymore #51247

* Mon Aug 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add option '-t' to procmail for local mail delivery

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- point to the map files in sendmail.cf as pointed out by
  David Beveridge <David@beveridge.com>

* Mon Jul 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add build requires #49695
- do not call "userdel"

* Tue Jul 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change sendmail.cf to "noreplace"

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.4

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.3
- add "localhost.localdomain" to the list of hostnames accepted
  for local delivery "Cw" in /etc/mail/sendmail.mc
- add patches from Pekka Savola <pekkas@netcore.fi>
	- Enable IPv6 at compile time, patch for glibc 2.2 from PLD
	- Add a commented-out IPv6 daemon .mc line to sendmail.mc
	- buildrequire: openldap-devel, cyrus-sasl-devel

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb 27 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add noreplace for /etc/sysconfig/sendmail and /etc/mail/sendmail.mc

* Wed Feb 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add changes from Christopher McCrory <chrismcc@pricegrabber.com>:
	- prepare /etc/mail/Makefile for more maps not shipped with this rpm
	- changed sendmail.mc to include some more commented out options,
	  so that people are directly pointed at important options
	- add /etc/pam.d/smtp for AUTH
	- add FEATURE(use_ct_file) and /etc/mail/trusted-users

* Fri Feb 16 2001 Tim Powers <timp@redhat.com>
- don't obsolete postfix and exim, only conflict (for RHN purposes)

* Thu Feb 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- obsolete and conflict with exim and postfix

* Wed Feb 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix devision by zero bug in #20395
- mv /usr/lib/sendmail-cf /usr/share/sendmail-cf

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n tweaks to initscript

* Wed Feb 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- aliases.db should be owned by group root

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- prepare for startup-script translation

* Tue Jan 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- enable daemon mode again, but only listen to the loopback device
  instead of all devices.
- do not include check.tar with old anti-spam rules 

* Fri Jan 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix configuration of /etc/aliases

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix interoperation problems with communigate pro
- disable msa

* Thu Jan 04 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to (security release) 8.11.2
- build also on RHL 6.x #16061
- include smrsh man-page #17901
- use the "-f" flag for makemap to preserve case for virtusertable
  and userdb in /etc/mail/Makefile - suggested by Harald Hoyer
- fix /usr/doc -> usr/share/doc in docu #20611
- wrong path in sendmail.mc #20691
- tcp-wrapper support wasn't enabled correctly #21642
- do not expose user "root" when masquerading like in older releases #21643
- disable the VRFY and EXPN smtp commands #21801
- disable queue-runs for normal users (restrictqrun privacy flag)
- fix typo in sendmail.mc #21880, #22682
- disable daemon mode to see what needs fixing

* Mon Oct 02 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.1

* Fri Sep 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply fixes for LDAP maps being closed too soon

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- provide /usr/lib/sasl/Sendmail.conf so that people know we can use it (#16064)

* Mon Aug  7 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- enable listening on the smtp port again

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix "missing find_m4.sh" problem by defining M4=/usr/bin/m4 (#14767)

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- okay, enable LDAP support again
- enable SMTP auth support via Cyrus SASL

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable the LDAP support until we can remove the sendmail->OpenLDAP->perl dep
- fix prereq

* Tue Jul 25 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to sendmail 8.11.0
- add LDAP support

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul  9 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- require procmail
- add further aliases

* Sat Jul  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d
- fix typo

* Tue Jul  4 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- ignore error from useradd

* Fri Jun 30 2000 Than Ngo <than@redhat.de>
- FHS fixes
- /etc/rc.d/init.d -> /etc/init.d
- fix initscript

* Fri Jun 23 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change to /usr/share/man

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- turn off daemon behaviour by default

* Mon Jun 18 2000 Bill Nottingham <notting@redhat.com>
- rebuild, fix dependencies

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- prereq /usr/sbin/useradd

* Fri May 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- enable MAP_REGEX
- enable tcp_wrapper support

* Thu May 18 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix etc/mail/aliases -> /etc/aliases in sendmail-redhat.mc

* Wed May  3 2000 Bill Nottingham <notting@redhat.com>
- update to 8.10.1
- fix build without sendmail installed
- add 'mailnull' user

* Wed Mar 15 2000 Bill Nottingham <notting@redhat.com>
- update to 8.10.0
- remove compatiblity chkconfig links
- add a mailnull user for sendmail to use

* Thu Feb 17 2000 Cristian Gafton <gafton@redhat.com>
- break the hard link for makemap and create it as a symlnk (#8223)

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix location of mailertable (Bug #6035)

* Sat Feb  5 2000 Bill Nottingham <notting@redhat.com>
- fixes for non-root builds (#8178)

* Wed Feb  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change perms on /etc/sysconfig/sendmail from 0755 to 0644
- allow compressed man-pages

* Thu Dec 02 1999 Cristian Gafton <gafton@redhat.com>
- add patch to prevent the DoS when rebuilding aliases

* Wed Sep  1 1999 Jeff Johnson <jbj@redhat.com>
- install man pages, not groff output (#3746).
- use dnl not '#' in m4 comment (#3749).
- add FEATURE(mailtertable) to the config -- example file needs this (#4649).
- use db2 not db1.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- add 127.0.0.1 to /etc/mail/access to avoid IDENT: relay problem (#3178).

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in preun, not postun (#3982)

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Jul 02 1999 Cristian Gafton <gafton@redhat.com>
- fixed typo bug in comment in the default .mc file (#2812)

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- fox the awk scripts in the postinstall
- enable FEATURE(accept_unresolvable_domains) by default to make laptop
  users happy.

* Sun Apr 18 1999 Cristian Gafton <gafton@redhat.com>
- make the redhat.mc be a separate source files. Sanitize patches that used
  to touch it.
- install redhat.mc as /etc/sendmail.mc so that people can easily modify
  their sendmail.cf configurations.

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- fixed virtusertable patch
- make smrsh look into /etc/smrsh

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- remove noreplace attr from sednmail.cf.

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- provide a more sane /etc/mail/access default config file
- use makemap to initializa the empty databases, not touch
- added a small, but helpful /etc/mail/Makefile

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- correxct dangling symlinks.
- check for map file existence in %%post.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- improved 8.9.3 config from Mike McHenry <mmchen@minn.net>

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- version 8.9.3

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- use the libdb1 stuff correctly

* Mon Sep 21 1998 Michael K. Johnson <johnsonm@redhat.com>
- Allow empty QUEUE in /etc/sysconfig/sendmail for those who
  want to run sendmail in daemon mode without processing the
  queue regularly.

* Thu Sep 17 1998 Michael K. Johnson <johnsonm@redhat.com>
- /etc/sysconfig/sendmail

* Fri Aug 28 1998 Jeff Johnson <jbj@redhat.com>
- recompile statically linked binary for 5.2/sparc

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscripts

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added a rmail patch

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- argh!  Fixed some of the db1 handling that had to be added for glibc 2.1

* Fri Oct 24 1997 Donnie Barnes <djb@redhat.com>
- added support for db1 on SPARC

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- various spec file cleanups
- changed group to Networking/Daemons (from Daemons).  Sure, it runs on
  non networked systems, but who really *needs* it then?

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- made /etc/mail/deny.db a ghost
- removed preun that used to remove deny.db (ghost handles that now)
- NOTE: upgrading from the sendmail packages in 4.8, 4.8.1, and possibly
  4.9 (all Red Hat betas between 4.2 and 5.0) could cause problems.  You
  may need to do a makemap in /etc/mail and a newaliases after upgrading
  from those packages.  Upgrading from 4.2 or prior should be fine.

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- made aliases.db a ghost

* Tue Sep 23 1997 Donnie Barnes <djb@redhat.com>
- fixed preuninstall script to handle aliases.db on upgrades properly

* Mon Sep 15 1997 Donnie Barnes <djb@redhat.com>
- fixed post-install output and changed /var/spool/mqueue to 755

* Thu Sep 11 1997 Donnie Barnes <djb@redhat.com>
- fixed /usr/lib/sendmail-cf paths

* Tue Sep 09 1997 Donnie Barnes <djb@redhat.com>
- updated to 8.8.7
- added some spam filtration
- combined some makefile patches
- added BuildRoot support

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- marked initscript symlinks as missingok
- run newalises after creating /var/spool/mqueue

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc, udated release to -6 (skipped -5!)

* Tue Apr 01 1997 Erik Troan <ewt@redhat.com>
- Added -nsl on the Alpha (for glibc to provide NIS functions).

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Added nis support.
