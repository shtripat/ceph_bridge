from tendrl.ceph_integration import flows


class CreateECProfile(flows.CephIntegrationBaseFlow):
    def run(self):
        super(CreateECProfile, self).run()
