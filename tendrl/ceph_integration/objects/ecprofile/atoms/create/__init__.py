from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.ecprofile import ECProfile


class Create(objects.CephIntegrationBaseAtom):
    obj = ECProfile
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        if 'ECProfile.plugin' in self.parameters:
            plugin = self.parameters['ECProfile.plugin']
        else:
            plugin = 'jerasure'

        if 'ECProfile.directory' in self.parameters:
            directory = self.parameters.get('ECProfile.directory')
        else:
            directory = "/usr/lib/ceph/erasure-code"

        attrs = dict(name=self.parameters['ECProfile.name'],
                     k=self.parameters['ECProfile.k'],
                     m=self.parameters['ECProfile.m'],
                     plugin=plugin,
                     directory=directory
                     )
        crud = Crud()
        crud.create("ec_profile", attrs)
        return True
