%define rl_vers  5.2
Name:           readline
Version:        5.2
Release:        0
License:        GPL-2.0+
Summary:        The Readline Library
Url:            http://www.gnu.org/software/bash/bash.html
Group:          Base/Libraries
Source0:        readline-%{version}.tar.bz2
Source2:        baselibs.conf
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  ncurses-devel
Provides:       bash:/%{_libdir}/libreadline.so.5
%global         _sysconfdir /etc
%global         _incdir     %{_includedir}

%description
The readline library is used by the Bourne Again Shell (bash, the
standard command interpreter) for easy editing of command lines.  This
includes history and search functionality.

%package devel
Version:        5.2
Release:        0
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       libreadline = %{version}
Requires:       ncurses-devel
Provides:       bash:%{_libdir}/libreadline.a

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package -n libreadline
Summary:        The Readline Library

%description -n libreadline
The readline library is used by the Bourne Again Shell (bash, the
standard command interpreter) for easy editing of command lines.  This
includes history and search functionality.

%prep
%setup -q -n readline-%{version}

%build
  autoconf
  cflags ()
  {
      local flag=$1; shift
      case "%{optflags}" in
      *${flag}*) return
      esac
      if test -n "$1" && gcc -Werror $flag -S -o /dev/null -xc   /dev/null > /dev/null 2>&1 ; then
	  local var=$1; shift
	  eval $var=\${$var:+\$$var\ }$flag
      fi
  }
  echo 'int main () { return !(sizeof(void*) >= 8); }' | gcc -x c -o test64 -
  if ./test64 ; then
      LARGEFILE=""
  else
      LARGEFILE="-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
  fi
  rm -f ./test64
  CFLAGS="%{optflags} $LARGEFILE -D_GNU_SOURCE -DRECYCLES_PIDS -Wall -g"
  LDFLAGS=""
  cflags -std=gnu89              CFLAGS
  cflags -Wuninitialized         CFLAGS
  cflags -Wextra                 CFLAGS
  cflags -Wno-unprototyped-calls CFLAGS
  cflags -Wno-switch-enum        CFLAGS
  cflags -ftree-loop-linear      CFLAGS
  cflags -pipe                   CFLAGS
  cflags -Wl,--as-needed         LDFLAGS
  cflags -Wl,-O,2                LDFLAGS
  CC=gcc
  CC_FOR_BUILD="$CC"
  CFLAGS_FOR_BUILD="$CFLAGS"
  LDFLAGS_FOR_BUILD="$LDFLAGS"
  export CC_FOR_BUILD CFLAGS_FOR_BUILD LDFLAGS_FOR_BUILD CFLAGS LDFLAGS CC
  ./configure --build=%{_target_cpu}-tizen-linux	\
	--prefix=%{_prefix}			\
	--with-curses			\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}
  make
  make documentation
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so.5
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so.5

%install
  make install htmldir=%{_defaultdocdir}/readline DESTDIR=%{buildroot}
  make install-shared libdir=/%{_libdir} linkagedir=%{_libdir} DESTDIR=%{buildroot}
  rm -rf %{buildroot}%{_defaultdocdir}/bash
  rm -rf %{buildroot}%{_defaultdocdir}/readline
  chmod 0755 %{buildroot}/%{_libdir}/libhistory.so.%{rl_vers}
  chmod 0755 %{buildroot}/%{_libdir}/libreadline.so.%{rl_vers}
  rm -f %{buildroot}/%{_libdir}/libhistory.so.%{rl_vers}*old
  rm -f %{buildroot}/%{_libdir}/libreadline.so.%{rl_vers}*old
  # remove unpackaged files
  #rm -fv %{buildroot}%{_libdir}/libhistory.so.*
  #rm -fv %{buildroot}%{_libdir}/libreadline.so.*
  rm -fv %{buildroot}%{_mandir}/man3/history.3*
  rm -fv %{buildroot}%{_infodir}/*.info*

%post -n libreadline -p /sbin/ldconfig

%postun -n libreadline -p /sbin/ldconfig


%files -n libreadline
%defattr(-,root,root)
%license COPYING
%{_libdir}/libhistory.so.5
%{_libdir}/libhistory.so.%{rl_vers}
%{_libdir}/libreadline.so.5
%{_libdir}/libreadline.so.%{rl_vers}

%files devel
%defattr(-,root,root)
%{_incdir}/readline/
%{_libdir}/libhistory.a
%{_libdir}/libhistory.so
%{_libdir}/libreadline.a
%{_libdir}/libreadline.so
%doc %{_mandir}/man3/readline.3.gz

%changelog
