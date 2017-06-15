import etcd

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects


class OsdExists(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(OsdExists, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Checking if OSD.%s exists" %
                    self.parameters['Osd.id'],
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )
        try:
            NS.ceph.objects.Osd(
                id=self.parameters['Osd.id']
            ).load()
            return True
        except etcd.EtcdKeyNotFound:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "OSD.%s doesnt exist" %
                        self.parameters['Osd.id'],
                    },
                    job_id=self.parameters['job_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
