#
# Conditional build:
%bcond_with	tests	# test target [Pipfile file missing as of 2.19.1]
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define		urllib3_ver	1.21.1
%define		module		requests
%define		egg_name	requests
Summary:	HTTP library for Python 2
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona 2
Name:		python-%{module}
Version:	2.25.1
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/requests/
Source0:	https://files.pythonhosted.org/packages/source/r/requests/%{module}-%{version}.tar.gz
# Source0-md5:	514d6f7eba77ada0b8c98ec7818828db
Patch0:		system-cert.patch
URL:		http://python-requests.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PySocks >= 1.5.8
BuildRequires:	python-certifi >= 2017.4.17
BuildRequires:	python-chardet >= 3.0.2
BuildRequires:	python-chardet < 4
BuildRequires:	python-idna >= 2.5
BuildRequires:	python-idna < 3
BuildRequires:	python-pytest >= 3
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-httpbin >= 0.0.7
BuildRequires:	python-pytest-mock
BuildRequires:	python-pytest-xdist
BuildRequires:	python-urllib3 >= %{urllib3_ver}
BuildRequires:	python-urllib3 < 1.26
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.5.8
BuildRequires:	python3-certifi >= 2017.4.17
BuildRequires:	python3-chardet >= 3.0.2
BuildRequires:	python3-chardet < 4
BuildRequires:	python3-idna >= 2.5
BuildRequires:	python3-idna < 3
BuildRequires:	python3-pytest >= 3
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-httpbin >= 0.0.7
BuildRequires:	python3-pytest-mock
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-urllib3 >= %{urllib3_ver}
BuildRequires:	python3-urllib3 < 1.26
%endif
%endif
Suggests:	ca-certificates
# for python2 only to get SNI working. python3 doesn't need this
Requires:	python-cryptography >= 1.3.4
Requires:	python-pyOpenSSL >= 0.14
Requires:	python-urllib3 >= 1.22-2
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
Requires:	python3-modules >= 1:3.5
# for https
Requires:	python3-cryptography >= 1.3.4
Requires:	python3-pyOpenSSL >= 0.14
Requires:	python3-urllib3 >= 1.22-2
Suggests:	ca-certificates

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
%patch0 -p1

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

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HISTORY.md README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-requests
%defattr(644,root,root,755)
%doc HISTORY.md README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
