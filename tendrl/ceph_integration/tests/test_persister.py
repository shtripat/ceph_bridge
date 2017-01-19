from mock import MagicMock
import sys
sys.modules['tendrl.commons.config'] = MagicMock()
from tendrl.ceph_integration.persistence import persister
del sys.modules['tendrl.commons.config']


class Test_Persister(object):
    def setup_method(self, method):
        self.Persister = persister.CephIntegrationEtcdPersister(MagicMock())

    def test_Persister_Creation(self):
        assert self.Persister is not None

    def test_update_sync_object(self):
        """Sending dummy parameters"""
        data = "data"
        updated = "updated"
        fsid = "fsid"
        name = "name"
        sync_type = "sync_type"
        version = "version"
        when = "when"
        cluster_id = "cluster_id"
        self.Persister.update_sync_object(
            updated, fsid, name, sync_type, version, when, data, cluster_id)
        self.Persister.etcd_orm.save.assert_called()

    def test_create_server(self):
        self.Persister.create_server("servers")
        self.Persister.etcd_orm.save.assert_called_with(
            "servers"
            )

    def test_create_service(self):
        self.Persister.create_service("service")
        self.Persister.etcd_orm.save.assert_called_with(
            "service"
            )

    def test_save_events(self):
        self.Persister.save_events(["Event1", "Event2"])
        self.Persister.etcd_orm.save.assert_called_with(
            "Event2"
            )
