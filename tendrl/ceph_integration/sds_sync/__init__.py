import gevent.event
import logging

from tendrl.commons import sds_sync
from tendrl.ceph_integration import ceph
from tendrl.ceph_integration.manager.cluster_monitor import ClusterMonitor
from tendrl.ceph_integration.manager import utils

LOG = logging.getLogger(__name__)


class CephIntegrationSdsSyncStateThread(sds_sync.SdsSyncThread):
    def __init__(self):
                super(CephIntegrationSdsSyncStateThread, self).__init__()
                # FSID to ClusterMonitor
                self.clusters = {}

    def _run(self):
        LOG.info("%s running" % self.__class__.__name__)

        while not self._complete.is_set():
            data = ceph.heartbeat(heartbeat_type="cluster", discover=True)
            if data is not None:
                for tag, cluster_data in data.iteritems():
                    try:
                        if tag.startswith("ceph/cluster/"):
                            if not cluster_data[
                                    'fsid'
                            ] in self._manager.clusters:
                                self._manager.on_pull(
                                    cluster_data
                                )
                            else:
                                LOG.debug(
                                    "%s: heartbeat from existing"
                                    " cluster %s" % (
                                        self.__class__.__name__,
                                        cluster_data['fsid']
                                    )
                                )
                        else:
                            # This does not concern us, ignore it
                            LOG.debug("TopLevelEvents: ignoring %s" % tag)
                            pass
                    except Exception:
                        LOG.exception(
                            "Exception handling message tag=%s" % tag)
            gevent.sleep(3)

        LOG.info("%s complete" % self.__class__.__name__)

    def on_pull(self, heartbeat_data):
        LOG.info("on_discovery: {0}".format(heartbeat_data['fsid']))
        cluster_monitor = ClusterMonitor(
            heartbeat_data['fsid'],
            heartbeat_data['name']
        )
        self.clusters[heartbeat_data['fsid']] = cluster_monitor
        utils.set_fsid(heartbeat_data['fsid'])
        # Run before passing on the heartbeat, because otherwise the
        # syncs resulting from the heartbeat might not be received
        # by the monitor.
        cluster_monitor.start()
        # Wait for ClusterMonitor to start accepting events before asking it
        # to do anything
        cluster_monitor.ready()
        cluster_monitor.on_heartbeat(heartbeat_data['id'], heartbeat_data)

    def delete_cluster(self, fs_id):
        """Note that the cluster will pop right back again if it's

        still sending heartbeats.

        """
        victim = self.clusters[fs_id]
        victim.stop()
        victim.done.wait()
        del self.clusters[fs_id]

        self._expunge(fs_id)

    def join(self):
        super(self).join()
        for monitor in self.clusters.values():
            monitor.join()
