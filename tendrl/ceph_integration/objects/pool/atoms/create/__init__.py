from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Create(objects.CephIntegrationBaseAtom):
    obj = Pool
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        attrs = dict(name=self.parameters['Pool.poolname'],
                     pg_num=self.parameters['Pool.pg_num'],
                     min_size=self.parameters['Pool.min_size'],
                     size=self.parameters['Pool.size'],
                     type=self.parameters.get('Pool.type'),
                     erasure_code_profile=self.parameters.get(
                         'Pool.erasure_code_profile'))
        if 'Pool.quota_enabled' in self.parameters and \
            self.parameters['Pool.quota_enabled'] is True:
            attrs['quota_max_objects'] = \
                self.parameters.get('Pool.quota_max_objects')
            attrs['quota_max_bytes'] = \
                self.parameters.get('Pool.quota_max_bytes')
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Creating pool %s" %
                    self.parameters['Pool.poolname'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        crud.create("pool", attrs)
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Successfully created pool %s" %
                    self.parameters['Pool.poolname'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
