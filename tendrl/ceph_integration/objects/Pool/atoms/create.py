from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.manager import utils as manager_utils
from tendrl.commons.atoms.base_atom import BaseAtom


class Create(BaseAtom):
    def run(self):
        fsid = manager_utils.get_fsid()
        attrs = dict(name=self.parameters['Pool.poolname'],
                     pg_num=self.parameters['Pool.pg_num'],
                     min_size=self.parameters['Pool.min_size'])
        crud = Crud(self.parameters['manager'])
        crud.create(fsid, "pool", attrs)
        return True
