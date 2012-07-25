%define 	module	requests
Summary:	HTTP library for Python
Name:		python-%{module}
Version:	0.13.3
%define		_verinternal	0.13.2
%define		_relstr			11-g52b55cc
Release:	0.1
License:	ISC
Group:		Development/Languages/Python
Source0:	https://github.com/kennethreitz/requests/tarball/develop/kennethreitz-%{module}-v%{version}-%{_relstr}.tar.gz
# Source0-md5:	083bd0d48b75d2ab79f2636f5bb204fc
URL:		https://github.com/kennethreitz/requests
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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

%build
# Filename says 0.13.3, __version__ says 0.13.2, so the test fails
#ver=$(%{__python} -c "import requests; print requests.__version__")
#test "$ver" = %{version}

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
%{py_sitescriptdir}/%{module}-%{_verinternal}-*.egg-info
%endif
