from tendrl.commons.etcdobj import EtcdObj
from tendrl.commons import config as cmn_config

from tendrl.commons import objects


class Config(objects.BaseObject):
    internal = True
    def __init__(self, config=None, *args, **kwargs):
        self_defs = {}
        super(Config, self).__init__(*args, **kwargs)

        self.value = '_NS/ceph/config'
        self.data = config or cmn_config.load_config(
            'ceph-integration',
            "/etc/tendrl/ceph-integration/ceph-integration.conf.yaml")
        self._etcd_cls = _ConfigEtcd


class _ConfigEtcd(EtcdObj):
    """Config etcd object, lazily updated
        """
    __name__ = '_NS/ceph/config'
    _tendrl_cls = Config
