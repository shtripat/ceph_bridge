from tendrl.common.persistence.etcd_persister import EtcdPersister
from tendrl.common.persistence.file_persister import FilePersister

from tendrl.ceph_integration.persistence.sync_objects import SyncObject


class CephIntegrationEtcdPersister(EtcdPersister):
    def __init__(self, config):
        super(CephIntegrationEtcdPersister, self).__init__(config)
        self._store = self.get_store()

    def update_sync_object(
        self,
        updated,
        fsid,
        name,
        sync_type,
        version,
        when,
        data,
        cluster_id
    ):
        self._store.save(
            SyncObject(
                updated=updated,
                fsid=fsid,
                cluster_name=name,
                sync_type=sync_type,
                version=version,
                when=when,
                data=data,
                cluster_id=cluster_id
            )
        )

    def create_server(self, server):
        self._store.save(server)

    def create_service(self, service):
        self._store.save(service)

    def save_events(self, events):
        for event in events:
            self._store.save(event)

    def update_tendrl_context(self, context):
        self._store.save(context)

    def update_tendrl_definitions(self, definition):
        self._store.save(definition)

    def update_pool(self, pool):
        self._store.save(pool)


class CephIntegrationFilePersister(FilePersister):
    def __init__(self, config):
        super(CephIntegrationEtcdPersister, self).__init__(config)
        self._doc_location = "%s/ceph_integration" % \
            config.get("ceph_integration", "doc_persist_location")

    def _update_sync_object(self,
                            updated,
                            fsid,
                            name,
                            sync_type,
                            version,
                            when,
                            data,
                            cluster_id):
        obj = SyncObject(
            updated=updated,
            fsid=fsid,
            cluster_name=name,
            sync_type=sync_type,
            version=version,
            when=when,
            data=data,
            cluster_id=cluster_id
        )

        f = open(
            "%s/%s" % (self._doc_location, cluster_id),
            "w"
        )
        f.write(obj.json())
        f.close()

    def _create_server(self, server):
        f = open(
            "%s/%s" % (self._doc_location, server.__name__),
            "w"
        )
        f.write(server.json())
        f.close()

    def _create_service(self, service):
        f = open(
            "%s/%s" % (self._doc_location, service.__name__),
            "w"
        )
        f.write(service.json())
        f.close()

    def _save_events(self, events):
        for event in events:
            f = open(
                "%s/%s" % (set._doc_location, event.__name__),
                "w"
            )
            f.write(event.json())
            f.close()

    def update_tendrl_context(self, context):
        f = open(
            "%s/%s" % (self._doc_location, context.__name__),
            "w"
        )
        f.write(context.json())
        f.close()

    def update_tendrl_definitions(self, definition):
        f = open(
            "%s/%s" % (self._doc_location, definition.__name__),
            "w"
        )
        f.write(definition.__name__)
        f.close()

    def update_pool(self, pool):
        f = open(
            "%s/%s" % (self._doc_location, pool.__name__),
            "w"
        )
        f.write(pool.__name__)
        f.close()
