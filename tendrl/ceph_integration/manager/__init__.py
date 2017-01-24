import gevent.event
import logging
import signal

from tendrl.commons.manager import Manager
from tendrl.ceph_integration import sds_sync
from tendrl.ceph_integration import central_store


LOG = logging.getLogger(__name__)


class CephIntegrationManager(Manager):
    def __init__(self):
        self._complete = gevent.event.Event()
        super(
            CephIntegrationManager,
            self
        ).__init__(
            tendrl_ns.state_sync_thread,
            tendrl_ns.central_store_thread
        )
        self.register_to_cluster()

    def register_to_cluster(self):
        # save tendrl context
        tendrl_ns.tendrl_context.save()


def main():
    tendrl_ns.register_subclasses_to_ns()
    tendrl_ns.setup_initial_objects()

    tendrl_ns.central_store_thread =\
        central_store.CephIntegrationEtcdCentralStore()
    tendrl_ns.state_sync_thread = sds_sync.CephIntegrationSdsSyncStateThread()

    tendrl_ns.definitions.save()
    tendrl_ns.config.save()

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
