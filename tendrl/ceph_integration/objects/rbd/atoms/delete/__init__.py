from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.rbd import Rbd
from tendrl.ceph_integration.manager.rbd_crud import RbdCrud
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Delete(objects.CephIntegrationBaseAtom):
    obj = Rbd
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        pool_id = self.parameters['Rbd.pool_id']
        rbd_name = self.parameters['Rbd.name']

        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleting rbd %s on pool %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

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
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleted rbd %s on pool-id %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
