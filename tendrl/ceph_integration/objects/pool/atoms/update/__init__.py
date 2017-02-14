from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.pool import Pool
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
        if 'Pool.size' in self.parameters:
            attrs['size'] = self.parameters.get('Pool.size')
        if 'Pool.quota_enabled' in self.parameters and \
            self.parameters['Pool.quota_enabled'] is True:
            attrs['quota_max_objects'] = \
                self.parameters.get('Pool.quota_max_objects')
            attrs['quota_max_bytes'] = \
                self.parameters.get('Pool.quota_max_bytes')
        crud = Crud()
        crud.update("pool", pool_id, attrs)
        return True
