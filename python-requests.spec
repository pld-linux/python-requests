#
# Conditional build:
%bcond_with	tests	# perform "make test"
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	bundled # bundled libraries
#
%define		urllib3ver	1.10.4
%define 	module	requests
Summary:	HTTP library for Python 2
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona 2
Name:		python-%{module}
Version:	2.7.0
Release:	2
License:	Apache2
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/r/requests/%{module}-%{version}.tar.gz
# Source0-md5:	29b173fd5fa572ec0764d1fd7b527260
URL:		http://python-requests.org
# find . -name '*.py' -exec sed -i -e 's#requests\.packages\.urllib3#urllib3#g' "{}" ";"
# find . -name '*.py' -exec sed -i -e 's#\.packages\.urllib3#urllib3#g' "{}" ";"
# find . -name '*.py' -exec sed -i -e 's#from \.packages import chardet#import charade as chardet#g' "{}" ";"
# + manual removal from setup.py
Patch0:		system-charade-and-urllib3.patch
Patch1:		system-cert.patch
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
%if %{without bundled}
BuildRequires:	python-charade
BuildRequires:	python-urllib3 >= %{urllib3ver}
%endif
%{?with_tests:BuildRequires:	python-pytest >= 2.3.4}
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{without bundled}
BuildRequires:	python3-charade
BuildRequires:	python3-urllib3 >= %{urllib3ver}
%endif
%{?with_tests:BuildRequires:	python3-pytest >= 2.3.4}
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	ca-certificates
Requires:	python-modules >= 1:2.6
%if %{without bundled}
Requires:	python-charade
Requires:	python-urllib3 >= %{urllib3ver}
%endif
# for python2 only to get SNI working. python3 doesn't need this
Requires:	python-ndg-httpsclient
Requires:	python-pyasn1
Requires:	python-pyOpenSSL
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
Requires:	python3-charade
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
%py_build -b py2 %{?with_tests:test}
%{?with_tests:cp requirements.txt test_requests.py py2; cd py2; PYTHONPATH=$(pwd)/lib %{__python} test_requests.py; cd ..}
%endif

%if %{with python3}
%py3_build -b py3 %{?with_tests:test}
%{?with_tests:cp requirements.txt test_requests.py py3; cd py3; PYTHONPATH=$(pwd)/lib %{__python3} test_requests.py; cd ..}
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
