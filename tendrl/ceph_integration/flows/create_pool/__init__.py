from tendrl.ceph_integration import flows


class CreatePool(flows.CephIntegrationBaseFlow):
    def run(self):
        super(CreatePool, self).run()
