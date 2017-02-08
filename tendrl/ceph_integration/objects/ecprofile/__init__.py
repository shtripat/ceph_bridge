from tendrl.commons.etcdobj import EtcdObj
from tendrl.ceph_integration import objects


class ECProfile(objects.CephIntegrationBaseObject):
    def __init__(self, name=None, k=None,
                 m=None, plugin=None,
                 directory=None,
                 ruleset_failure_domain=None,
                 *args, **kwargs):
        super(ECProfile, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/ec_profiles/%s'
        self.name = name
        self.k = k
        self.m = m
        self.plugin = plugin
        self.directory = directory
        self.ruleset_failure_domain = ruleset_failure_domain
        self._etcd_cls = _ECProfile


class _ECProfile(EtcdObj):
    __name__ = 'clusters/%s/ec_profiles/%s'
    _tendrl_cls = ECProfile

    def render(self):
        self.__name__ = self.__name__ %\
            (tendrl_ns.tendrl_context.integration_id, self.name)
        return super(_ECProfile, self).render()
