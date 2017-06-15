from tendrl.ceph_integration import ceph
from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError


class MarkIn(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(MarkIn, self).__init__(*args, **kwargs)

    def run(self):
        commands = ['osd', 'in', str(self.parameters['Osd.id'])]
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
                        "message": "Failed to mark OSD.%s as IN" %
                        self.parameters['Osd.id'],
                    },
                    job_id=self.parameters['job_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            raise AtomExecutionFaledError(
                "Failed to mark OSD.%s as IN" %
                self.parameters['Osd.id']
            )

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Successfully marked OSD.%s IN" %
                    self.parameters['Osd.id'],
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        return True
