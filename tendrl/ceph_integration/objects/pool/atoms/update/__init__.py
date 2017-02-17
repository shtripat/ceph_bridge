from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons.objects.atoms import AtomExecutionFailedError


class Update(objects.CephIntegrationBaseAtom):
    obj = Pool
    def __init__(self, *args, **kwargs):
        super(Update, self).__init__(*args, **kwargs)

    def run(self):
        pool_id = self.parameters['Pool.pool_id']
        attrs = {}
        if 'Pool.poolname' in self.parameters:
            attrs['name'] = self.parameters.get('Pool.poolname')
            Event(
                Message(
                    priority="info",
                    publisher=tendrl_ns.publisher_id,
                    payload={
                        "message": "Renaming pool-id %s to %s" %
                        (self.parameters['Pool.pool_id'],
                         self.parameters['Pool.poolname'])
                        },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
        if 'Pool.pg_num' in self.parameters:
            obj = Pool(
                pool_id=pool_id
            )
            fetched_pool = tendrl_ns.etcd_orm.read(obj)
            if fetched_pool.pg_num > self.parameters.get('Pool.pg_num'):
                raise AtomExecutionFailedError(
                    "New pg-num cannot be less than existing value"
                )
            attrs['pg_num'] = self.parameters.get('Pool.pg_num')
            Event(
                Message(
                    priority="info",
                    publisher=tendrl_ns.publisher_id,
                    payload={
                        "message": "Growing pg-num for pool-id %s to %s" %
                        (self.parameters['Pool.pool_id'],
                         self.parameters['Pool.pg_num'])
                        },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
        if 'Pool.size' in self.parameters:
            attrs['size'] = self.parameters.get('Pool.size')
            Event(
                Message(
                    priority="info",
                    publisher=tendrl_ns.publisher_id,
                    payload={
                        "message": "Updating size for pool-id %s to %s" %
                        (self.parameters['Pool.pool_id'],
                         self.parameters['Pool.size'])
                        },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
        if 'Pool.min_size' in self.parameters:
            attrs['min_size'] = self.parameters.get('Pool.min_size')
            Event(
                Message(
                    priority="info",
                    publisher=tendrl_ns.publisher_id,
                    payload={
                        "message": "Updating min_size for pool-id %s to %s" %
                        (self.parameters['Pool.pool_id'],
                         self.parameters['Pool.min_size'])
                        },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
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
                        "message": "Updating quota parameters for pool-id %s "
                        "to quota_max_objects=%s, quota_max_bytes=%s" %
                        (self.parameters['Pool.pool_id'],
                         self.parameters['Pool.quota_max_objects'],
                         self.parameters['Pool.quota_max_bytes'])
                        },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
        crud = Crud()
        crud.update("pool", pool_id, attrs)
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Pool %s successfully updated" %
                    (self.parameters['Pool.pool_id'])
                    },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
