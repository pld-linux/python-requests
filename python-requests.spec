# TODO
# - bundled external libs? packages/ contains:
#   chardet/
#   chardet2/
#   oauthlib/
%define 	module	requests
Summary:	HTTP library for Python
Name:		python-%{module}
Version:	0.13.3
Release:	1
License:	ISC
Group:		Development/Languages/Python
Source0:	https://github.com/kennethreitz/requests/tarball/v%{version}-11-g52b55cc/%{name}-%{version}.tgz
# Source0-md5:	d4e0de0ecfc14128c3a878d9f82328a0
URL:		https://github.com/kennethreitz/requests
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Requests is an ISC Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the api is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks.

Things shouldn't be this way. Not in Python.

%prep
%setup -qc
mv *-%{module}-*/* .

# fix version in module
# tarball for 0.13.3 contains 0.13.2:
#./HISTORY.rst:0.13.2 (2012-06-28)
#./requests/__init__.py:__version__ = '0.13.2'
#./requests/__init__.py:__build__ = 0x001302
%{__sed} -i -e 's/0\.13\.2/0.13.3/; s/0x001302/0x001302/' requests/__init__.py

%build
ver=$(%{__python} -c "import requests; print requests.__version__")
test "$ver" = %{version}

%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst README.rst LICENSE  docs
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
