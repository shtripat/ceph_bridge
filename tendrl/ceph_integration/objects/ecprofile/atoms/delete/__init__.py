from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.ecprofile import ECProfile


class Delete(objects.CephIntegrationBaseAtom):
    obj = ECProfile
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        crud = Crud()
        crud.delete("ec_profile", self.parameters['ECProfile.name'])
        tendrl_ns.etcd_orm.client.delete(
            "clusters/%s/ec_profiles/%s" % (
                tendrl_ns.tendrl_context.integration_id,
                self.parameters['ECProfile.name']
            ),
            recursive=True
        )
        return True
