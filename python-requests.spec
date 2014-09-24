# Conditional build:
%bcond_without  python2         # build python 2 module
%bcond_without  python3         # build python 3 module
#
%define 	module	requests
Summary:	HTTP library for Python
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona
Name:		python-%{module}
Version:	2.4.1
Release:	1
License:	Apache2
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/r/requests/%{module}-%{version}.tar.gz
# Source0-md5:	931461f761c70708c46ea65b7889da58
URL:		http://python-requests.org
Patch0:		system-charade-and-urllib3.patch
Patch1:		system-cert.patch
%if %{with python2}
BuildRequires:	python-charade
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-urllib3 >= 1.9.1
%endif
%if %{with python3}
BuildRequires:	python3-charade
BuildRequires:	python3-modules >= 3.2
BuildRequires:	python3-urllib3 >= 1.9.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	ca-certificates
Requires:	python-charade
Requires:	python-modules >= 1:2.6
Requires:	python-urllib3 >= 1.9.1
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

%description -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

%package -n python3-requests
Summary:	HTTP library, written in Python, for human beings
Summary(pl.UTF-8):	Biblioteka HTTP library napisana w Pythonie dla ludzi
Group:		Development/Languages/Python
Requires:	ca-certificates
Requires:	python3-charade
Requires:	python3-modules >= 3.2
Requires:	python3-urllib3 >= 1.9.1

%description -n python3-requests
Requests is a HTTP library, written in Python, for human beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the api is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

%description -n python3-requests -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%{__python} setup.py build -b py2
%endif

%if %{with python3}
%{__python3} setup.py build -b py3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build -b py2 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py  \
	build -b py3 \
	install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%{__rm} -rf $RPM_BUILD_ROOT{%{py_sitescriptdir},%{py3_sitescriptdir}}/%{module}/{cacert.pem,packages}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-requests
%defattr(644,root,root,755)
%doc HISTORY.rst README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
