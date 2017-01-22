from tendrl.ceph_integration import objects
from tendrl.ceph_integration.flows import CephIntegrationBaseFlow


class DeletePool(CephIntegrationBaseFlow):
    def __init__(self, *args, **kwargs):
        super(DeletePool, self).__init__(*args, **kwargs)
        self.obj = objects.pool.Pool

    def run(self):
        super(DeletePool, self).run()
