Name: tendrl-ceph-integration
Version: 0.0.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Tendrl bridge for Ceph Storage
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/ceph_integration

BuildRequires: python2-devel
BuildRequires: pytest
BuildRequires: systemd

Requires: python-etcd
Requires: python-dateutil
Requires: python-gevent
Requires: python-greenlet
Requires: pytz
Requires: python-msgpack
Requires: tendrl-bridge-common

%description
Tendrl bridge for Ceph Storage

%prep
%setup
# Remove the requirements file to avoid adding into
# distutils requiers_dist config
rm -rf {test-,}requirements.txt

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -p -D -m 0644 systemd/tendrl-cephd.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-cephd.service

%post
%systemd_post tendrl-cephd.service

%preun
%systemd_preun tendrl-cephd.service

%postun
%systemd_postun_with_restart tendrl-cephd.service

%check
py.test -v tendrl/ceph_integration/tests

%files -f INSTALLED_FILES
%doc README.rst
%license LICENSE
%{_unitdir}/tendrl-cephd.service

%changelog
* Wed Oct 26 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
