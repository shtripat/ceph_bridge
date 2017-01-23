from tendrl.commons.etcdobj import EtcdObj
from tendrl.ceph_integration import objects


class Server(objects.CephIntegrationBaseObject):
    def __init__(self, fsid=None, fqdn=None,
                 hostname=None, managed=None, last_contact=None,
                 boot_time=None, ceph_version=None, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/Servers/%s'
        self.fsid = fsid
        self.fqdn = fqdn
        self.hostname = hostname
        self.managed = managed
        self.last_contact = last_contact
        self.boot_time = boot_time
        self.ceph_version = ceph_version
        self._etcd_cls = _Server


class _Server(EtcdObj):
    """A table of the _Server, lazily updated
    """
    __name__ = 'clusters/%s/Servers/%s'
    _tendrl_cls = Server

    def render(self):
        self.__name__ = self.__name__ % (self.fsid, self.fqdn)
        return super(_Server, self).render()
