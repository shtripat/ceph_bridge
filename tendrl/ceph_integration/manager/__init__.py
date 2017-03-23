import logging

import etcd
import gevent.event
import signal

from tendrl.commons import TendrlNS
from tendrl.commons import manager
from tendrl import ceph_integration
from tendrl.ceph_integration import sds_sync
from tendrl.ceph_integration import central_store

LOG = logging.getLogger(__name__)


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

    NS.central_store_thread =\
        central_store.CephIntegrationEtcdCentralStore()
    NS.state_sync_thread = sds_sync.CephIntegrationSdsSyncStateThread()

    NS.node_context.save()
    
    # Check if Integration is part of any Tendrl imported/created sds cluster
    try:
        NS.tendrl_context = NS.tendrl_context.load()
        LOG.info(
            "Integration %s is part of sds cluster" %
            NS.tendrl_context.integration_id
        )
    except etcd.EtcdKeyNotFound:
        LOG.error(
            "Node %s is not part of any sds cluster" %
            NS.node_context.node_id
        )
        raise Exception(
            "Integration cannot be started, "
            "please Import or Create sds cluster in Tendrl "
            "and include Node %s" % NS.node_context.node_id
        )
    NS.ceph.definitions.save()
    NS.ceph.config.save()
    NS.publisher_id = "ceph_integration"

    m = CephIntegrationManager()
    m.start()

    complete = gevent.event.Event()

    def shutdown():
        LOG.info("Signal handler: stopping")
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)
