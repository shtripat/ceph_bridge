from tendrl.ceph_integration.manager.crud import Crud
from tendrl.commons import objects
from tendrl.ceph_integration.objects.ecprofile import ECProfile
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Delete(objects.BaseAtom):
    obj = ECProfile
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Deleting ec-profile %s" %
                    self.parameters['ECProfile.name'],
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        resp = crud.delete("ec_profile", self.parameters['ECProfile.name'])
        ret_val, err = crud.sync_request_status(resp['request'])
        if ret_val != 0:
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to delete ec-profile %s."
                        " Error: %s" % (self.parameters['ECProfile.name'],
                                        err)
                    },
                    job_id=self.parameters['job_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        NS.etcd_orm.client.delete(
            "clusters/%s/ECProfiles/%s" % (
                NS.tendrl_context.integration_id,
                self.parameters['ECProfile.name']
            ),
            recursive=True
        )
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Deleted ec-profile %s" %
                    self.parameters['ECProfile.name'],
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        return True
