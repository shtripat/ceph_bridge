from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.rbd import Rbd
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Resize(objects.CephIntegrationBaseAtom):
    obj = Rbd
    def __init__(self, *args, **kwargs):
        super(Resize, self).__init__(*args, **kwargs)

    def run(self):
        attrs = dict(pool_id=self.parameters['Rbd.pool_id'],
                     size=str(self.parameters['Rbd.size']))
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Re-sizing rbd %s on pool %s to %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'],
                     self.parameters['Rbd.size'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        crud.update("rbd", self.parameters['Rbd.name'], attrs)
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Successfully re-sized rbd %s on pool-id %s to "
                    "%s" % (self.parameters['Rbd.name'],
                            self.parameters['Rbd.pool_id'],
                            self.parameters['Rbd.size'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
