from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.manager import utils as manager_utils
from tendrl.common.flows.base_flow import BaseFlow


class CreatePool(BaseFlow):
    def run(self):
        self.parameters.update(
            {
                "crud": Crud(self.parameters['manager']),
                "fsid": manager_utils.get_fsid()
            }
        )
        super(CreatePool, self).run()
        del self.parameters['fsid']
        del self.parameters['crud']
