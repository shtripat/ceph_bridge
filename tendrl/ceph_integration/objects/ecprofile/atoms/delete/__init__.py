from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.ecprofile import ECProfile
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Delete(objects.CephIntegrationBaseAtom):
    obj = ECProfile
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleting ec-profile %s" %
                    self.parameters['ECProfile.name'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters["flow_id"],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        crud.delete("ec_profile", self.parameters['ECProfile.name'])
        tendrl_ns.etcd_orm.client.delete(
            "clusters/%s/ECProfiles/%s" % (
                tendrl_ns.tendrl_context.integration_id,
                self.parameters['ECProfile.name']
            ),
            recursive=True
        )
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleted ec-profile %s" %
                    self.parameters['ECProfile.name'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters["flow_id"],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
