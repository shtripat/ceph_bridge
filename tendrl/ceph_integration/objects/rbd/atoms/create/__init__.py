from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.rbd import Rbd
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Create(objects.CephIntegrationBaseAtom):
    obj = Rbd
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        attrs = dict(name=self.parameters['Rbd.name'],
                     size=str(self.parameters['Rbd.size']),
                     pool_id=self.parameters.get('Rbd.pool_id')
                     )
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Creating rbd %s on pool %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        crud.create("rbd", attrs)

        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Successfully created rbd %s on pool %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        pool_name = tendrl_ns.etcd_orm.client.read(
            "clusters/%s/Pools/%s/pool_name" %
            (tendrl_ns.tendrl_context.integration_id,
             self.parameters['Rbd.pool_id'])
        ).value
        rbd_details = tendrl_ns.state_sync_thread._get_rbds(pool_name)
        for k, v in rbd_details.iteritems():
            tendrl_ns.ceph_integration.objects.Rbd(
                name=k,
                size=v['size'],
                pool_id=self.parameters['Rbd.pool_id'],
                flags=v['flags'],
                provisioned=tendrl_ns.state_sync_thread._to_bytes(
                    v['provisioned']),
                used=tendrl_ns.state_sync_thread._to_bytes(v['used'])
            ).save()

        return True
