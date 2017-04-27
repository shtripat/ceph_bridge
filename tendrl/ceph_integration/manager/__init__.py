import etcd
import gevent
import gevent.event
import signal

from tendrl import ceph_integration
from tendrl.ceph_integration import central_store
from tendrl.ceph_integration import sds_sync

from tendrl.commons.event import Event
from tendrl.commons import manager
from tendrl.commons.message import Message
from tendrl.commons import TendrlNS


class CephIntegrationManager(manager.Manager):
    def __init__(self):
        self._complete = gevent.event.Event()
        super(
            CephIntegrationManager,
            self
        ).__init__(
            NS.state_sync_thread,
            NS.central_store_thread
        )


def main():
    ceph_integration.CephIntegrationNS()
    TendrlNS()

    NS.type = "sds"
    NS.publisher_id = "ceph_integration"

    NS.central_store_thread =\
        central_store.CephIntegrationEtcdCentralStore()
    NS.state_sync_thread = sds_sync.CephIntegrationSdsSyncStateThread()

    NS.node_context.save()

    # Check if Integration is part of any Tendrl imported/created sds cluster
    try:
        NS.tendrl_context = NS.tendrl_context.load()
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={"message": "Integration %s is part of sds cluster"
                                    % NS.tendrl_context.integration_id
                         }
            )
        )

    except etcd.EtcdKeyNotFound:
        Event(
            Message(
                priority="error",
                publisher=NS.publisher_id,
                payload={"message": "Node %s is not part of any sds cluster" %
                                    NS.node_context.node_id
                         }
            )
        )
        raise Exception(
            "Integration cannot be started, "
            "please Import or Create sds cluster in Tendrl "
            "and include Node %s" % NS.node_context.node_id
        )
    if NS.tendrl_context.integration_id is None:
        Event(
            Message(
                priority="error",
                publisher=NS.publisher_id,
                payload={"message": "Node %s is not part of any sds cluster" %
                                    NS.node_context.node_id
                         }
            )
        )
        raise Exception(
            "Integration cannot be started, "
            "please Import or Create sds cluster in Tendrl "
            "and include Node %s" % NS.node_context.node_id
        )

    NS.tendrl_context.save()
    NS.ceph.definitions.save()
    NS.ceph.config.save()

    m = CephIntegrationManager()
    m.start()

    # Persist the monitor secret to central store
    # This is required while expand cluster with more mon nodes
    # We need to wait for few seconds to let the first round of
    # cluster sync happen
    gevent.sleep(5)
    try:
        with open(
            "/etc/ceph/%s.client.admin.keyring" %\
            NS.tendrl_context.cluster_name
        ) as f:
            content = f.read()
            mon_sec = content.split('\n')[1].strip().split(' = ')[1].strip()
            NS.etcd_orm.client.write(
                "clusters/%s/_mon_key" % NS.tendrl_context.integration_id,
                mon_sec
            )
    except:
        Event(
            Message(
                priority="warning",
                publisher=NS.publisher_id,
                payload={"message": "Couldn't save monitor key"}
            )
        )
    finally:
        f.close()

    complete = gevent.event.Event()

    def shutdown():
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={"message": "Signal handler: stopping"}
            )
        )
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)
