%define pkg_name tendrl-ceph-bridge
%define pkg_version 0.0.1
%define pkg_release 1

Name: %{pkg_name}
Version: %{pkg_version}
Release: %{pkg_release}%{?dist}
BuildArch: noarch
Summary: Tendrl bridge for Ceph Storage
Source0: %{pkg_name}-%{pkg_version}.tar.gz
Group:   Applications/System
License: LGPL2.1
Url: https://github.com/Tendrl/ceph_bridge

Requires: python-etcd >= 0.4.3
Requires: python-dateutil >= 2.4.2
Requires: python-gevent >= 1.0.2
Requires: python-greenlet >= 0.4.2
Requires: pytz
Requires: python-msgpack >= 0.4.5
Requires: python-taskflow >= 2.6.0
Requires: tendrl-bridge-common

%description
Tendrl bridge for Ceph Storage

%prep
%setup -n %{pkg_name}-%{pkg_version}
# Remove the requirements file to avoid adding into
# distutils requiers_dist config
rm -rf {test-,}requirements.txt

# Remove bundled egg-info
rm -rf %{pkg_name}.egg-info

%build
%{__python} setup.py build

# generate html docs
%if 0%{?rhel}==7
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -Dm 0644 tendrl-cephd.service $RPM_BUILD_ROOT/usr/lib/systemd/system/tendrl-cephd.service

%post
%systemd_post tendrl-cephd.service

%preun
%systemd_preun tendrl-cephd.service

%postun
%systemd_postun_with_restart tendrl-cephd.service

%files -f INSTALLED_FILES
%doc html README.rst
%license LICENSE
%{_usr}/lib/systemd/system/tendrl-cephd.service

%changelog
* Wed Oct 26 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
