from tendrl.commons.event import Event
from tendrl.commons import flows
from tendrl.commons.message import Message


class RepairOsd(flows.BaseFlow):

    def __init__(self, *args, **kwargs):
        super(RepairOsd, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Starting repair of OSD.%s" %
                    (self.parameters['Osd.id'])
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(RepairOsd, self).run()
