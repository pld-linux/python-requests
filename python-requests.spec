#
# Conditional build:
%bcond_with	tests	# test target (tests not included in dist tarball as of 2.13.0)
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	bundled # bundled libraries
#
%define		urllib3ver	1.20
%define 	module	requests
Summary:	HTTP library for Python 2
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona 2
Name:		python-%{module}
Version:	2.13.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/16/09/37b69de7c924d318e51ece1c4ceb679bf93be9d05973bb30c35babd596e2/%{module}-%{version}.tar.gz
# Source0-md5:	921ec6b48f2ddafc8bb6160957baf444
Patch0:		%{name}-remove-nested-bundling-dep.patch
Patch1:		system-cert.patch
URL:		http://python-requests.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
%if %{without bundled}
BuildRequires:	python-chardet >= 2.3.0
BuildRequires:	python-urllib3 >= %{urllib3ver}
%endif
%if %{with tests}
BuildRequires:	python-pytest >= 2.8.0
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-httpbin >= 0.0.7
BuildRequires:	python-pytest-mock
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{without bundled}
BuildRequires:	python3-chardet >= 2.3.0
BuildRequires:	python3-urllib3 >= %{urllib3ver}
%endif
%if %{with tests}
BuildRequires:	python3-pytest >= 2.8.0
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-httpbin >= 0.0.7
BuildRequires:	python3-pytest-mock
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
Requires:	ca-certificates
Requires:	python-idna >= 2.0.0
Requires:	python-modules >= 1:2.6
%if %{without bundled}
Requires:	python-chardet >= 2.3.0
Requires:	python-urllib3 >= %{urllib3ver}
%endif
# for python2 only to get SNI working. python3 doesn't need this
Requires:	python-ndg-httpsclient
Requires:	python-pyasn1
Requires:	python-pyOpenSSL >= 0.14
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Requests is a HTTP library, written in Python, for human beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the API is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

This package contains Python 2.x module.

%description -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

Ten pakiet zawiera moduł dla Pythona 2.x.

%package -n python3-requests
Summary:	HTTP library for Python 3
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona 3
Group:		Development/Languages/Python
Requires:	ca-certificates
Requires:	python3-modules >= 1:3.2
%if %{without bundled}
Requires:	python3-chardet >= 2.3.0
Requires:	python3-idna >= 2.0.0
Requires:	python3-urllib3 >= %{urllib3ver}
%endif

%description -n python3-requests
Requests is a HTTP library, written in Python, for human beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the api is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

This package contains Python 3.x module.

%description -n python3-requests -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

Ten pakiet zawiera moduł dla Pythona 3.x.

%prep
%setup -q -n %{module}-%{version}
%{!?with_bundled:%patch0 -p1}
%patch1 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%{__rm} $RPM_BUILD_ROOT{%{py_sitescriptdir},%{py3_sitescriptdir}}/%{module}/cacert.pem
%{!?with_bundled:%{__rm} -r $RPM_BUILD_ROOT{%{py_sitescriptdir},%{py3_sitescriptdir}}/%{module}/packages}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-requests
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
