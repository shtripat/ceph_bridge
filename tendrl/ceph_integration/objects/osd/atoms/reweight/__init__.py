from tendrl.ceph_integration import ceph
from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError


class Reweight(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(Reweight, self).__init__(*args, **kwargs)

    def run(self):
        commands = [
            'osd',
            'reweight',
            str(self.parameters['Osd.id']),
            str(self.parameters['Osd.weight'])
        ]
        cmd_out = ceph.ceph_command(
            NS.tendrl_context.cluster_name,
            commands
        )
        if cmd_out['status'] != 0:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to start reweight for OSD.%s" %
                        self.parameters['Osd.id'],
                    },
                    job_id=self.parameters['job_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            raise AtomExecutionFaledError(
                "Failed to start reweight for OSD.%s" %
                self.parameters['Osd.id']
            )

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Successfully started reweight for OSD.%s" %
                    self.parameters['Osd.id'],
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        return True
