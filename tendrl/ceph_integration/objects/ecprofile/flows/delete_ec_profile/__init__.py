from tendrl.ceph_integration import objects
from tendrl.ceph_integration.flows import CephIntegrationBaseFlow
from tendrl.ceph_integration.objects.ecprofile import ECProfile


class DeleteECProfile(CephIntegrationBaseFlow):
    obj = ECProfile
    def __init__(self, *args, **kwargs):
        super(DeleteECProfile, self).__init__(*args, **kwargs)

    def run(self):
        super(DeleteECProfile, self).run()
