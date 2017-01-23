from tendrl.ceph_integration.flows import CephIntegrationBaseFlow


class CreatePool(CephIntegrationBaseFlow):
    def run(self):
        super(CreatePool, self).run()
