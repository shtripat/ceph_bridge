import gevent.event
import logging
import signal

from tendrl.commons.manager import Manager
from tendrl.node_agent import node_sync
from tendrl.node_agent import central_store


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
    tendrl_ns.state_sync_thread = node_sync.CephIntegrationSdsSyncStateThread()
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
