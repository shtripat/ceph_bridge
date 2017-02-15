from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.rbd import Rbd
from tendrl.ceph_integration.manager.rbd_crud import RbdCrud


class Delete(objects.CephIntegrationBaseAtom):
    obj = Rbd
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        pool_id = self.parameters['Rbd.pool_id']
        rbd_name = self.parameters['Rbd.name']
        crud = RbdCrud()
        crud.delete_rbd(
            pool_id,
            rbd_name
        )

        tendrl_ns.etcd_orm.client.delete(
            "clusters/%s/Pools/%s/Rbds/%s" % (
                tendrl_ns.tendrl_context.integration_id,
                self.parameters['Rbd.pool_id'],
                self.parameters['Rbd.name']
            ),
            recursive=True
        )

        return True
