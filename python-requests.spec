# TODO
# - bundled external libs? packages/ contains:
#   chardet/
#   chardet2/
#   oauthlib/
#
# Conditional build:
%bcond_without	doc	# HTML documentation build
#
%define 	module	requests
Summary:	HTTP library for Python
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona
Name:		python-%{module}
Version:	1.1.0
Release:	0.1
License:	ISC
Group:		Development/Languages/Python
Source0:	https://github.com/kennethreitz/requests/tarball/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	89b4958831c4c3276ffe5d21ed53dec8
URL:		https://github.com/kennethreitz/requests
BuildRequires:	python >= 1:2.6
BuildRequires:	python3 >= 3.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Requests is an ISC Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the API is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

%description -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi, wydana na
licencji ISC.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

%package -n python3-requests
Summary:	HTTP library, written in Python, for human beings
Summary(pl.UTF-8):	Biblioteka HTTP library napisana w Pythonie dla ludzi
Group:		Development/Languages/Python

%description -n python3-requests
Requests is an ISC Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the api is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

%description -n python3-requests -l pl.UTF-8
Requests is an ISC Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the API is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

%prep
# kennethreitz-requests-1a7c91f
%setup -q -n kennethreitz-%{module}-1a7c91f

# avoid "distutils.errors.DistutilsByteCompileError: byte-compiling is disabled."
%{__sed} -i -e '/PYTHONDONTWRITEBYTECODE/d' setup.py

%build
ver=$(%{__python} -c "import requests; print requests.__version__")
test "$ver" = %{version}

mkdir py2-egg py3-egg
%{__python} setup.py build --build-base py2
%{__python3} setup.py build --build-base py3

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py \
	build --build-base py2 \
        install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__python3} setup.py  \
	build --build-base py3 \
        install \
        --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst LICENSE README.rst %{?with_doc:docs/_build/html}
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info

%files -n python3-requests
%defattr(644,root,root,755)
%doc AUTHORS.rst LICENSE README.rst %{?with_doc:docs/_build/html}
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
