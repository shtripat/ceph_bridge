from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.manager import utils as manager_utils
from tendrl.commons.atoms.base_atom import BaseAtom


class Delete(BaseAtom):
    def run(self):
        cluster_id = self.parameters['Tendrl_context.cluster_id']
        pool_id = self.parameters['Pool.pool_id']
        fsid = manager_utils.get_fsid()
        crud = Crud(self.parameters['manager'])
        crud.delete(
            fsid,
            "pool",
            pool_id
        )

        etcd_client = self.parameters['etcd_orm'].client
        pool_key = "clusters/%s/Pools/%s/deleted" % (cluster_id, pool_id)
        etcd_client.write(pool_key, "True")

        return True
