import logging
import os

from tendrl.commons.etcdobj import EtcdObj
from tendrl.commons.utils import cmd_utils

from tendrl.ceph_integration import objects

LOG = logging.getLogger(__name__)


class TendrlContext(objects.CephIntegrationBaseObject):
    def __init__(self, integration_id=None, node_id=None,
                 sds_name=None, sds_name=None, *args, **kwargs):
        super(TendrlContext, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/TendrlContext'

        # integration_id is the Tendrl generated cluster UUID
        self.cluster_id = integration_id or \
            self._get_local_integration_id(node_id)
        self.sds_name = sds_name or self._get_sds_name()
        self.sds_version = sds_name or self._get_sds_version()
        self._etcd_cls = _TendrlContextEtcd

    def _get_local_integration_id(self, node_id):
        try:
            tendrl_context_path = "~/.tendrl/" + self.value % node_id \
                + "integration_id"
            if os.path.isfile(tendrl_context_path):
                with open(tendrl_context_path) as f:
                    integration_id = f.read()
                    if integration_id:
                        LOG.info(
                            "GET_LOCAL: "
                            "tendrl_ns.ceph_integration.objects.TendrlContext"
                            ".integration_id==%s" % integration_id)
                        return integration_id
        except AttributeError:
            return None

    def _get_sds_version(self):
        cmd = cmd_utils.Command("ceph --version")
        out, err, rc = cmd.run(config['tendrl_ansible_exec_file'])
        if out["rc"] == 0:
            nvr = out['stdout']
            return nvr.split()[2].split("-")[0]
        return None

    def _get_sds_name(self):
        cmd = cmd_utils.Command("ceph --version")
        out, err, rc = cmd.run(config['tendrl_ansible_exec_file'])
        if out["rc"] == 0:
            nvr = out['stdout']
            return nvr.split()[0]


class _TendrlContextEtcd(EtcdObj):
    """A table of the tendrl context, lazily updated
    """
    __name__ = 'clusters/%s/TendrlContext'
    _tendrl_cls = TendrlContext

    def render(self):
        self.__name__ = self.__name__ % self.integration_id
        return super(_TendrlContextEtcd, self).render()
