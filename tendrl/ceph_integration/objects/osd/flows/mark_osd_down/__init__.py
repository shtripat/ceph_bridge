from tendrl.commons.event import Event
from tendrl.commons import flows
from tendrl.commons.message import Message


class MarkOsdDown(flows.BaseFlow):

    def __init__(self, *args, **kwargs):
        super(MarkOsdDown, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Marking the OSD.%s DOWN" %
                    (self.parameters['Osd.id'])
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(MarkOsdDown, self).run()
