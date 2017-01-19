from tendrl.ceph_integration.persistence.sync_objects import SyncObject
from tendrl.commons.persistence.etcd_persister import EtcdPersister


class CephIntegrationEtcdPersister(EtcdPersister):
    def __init__(self, etcd_orm):
        super(CephIntegrationEtcdPersister, self).__init__(etcd_orm)

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
        self.etcd_orm.save(
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
        self.etcd_orm.save(server)

    def create_service(self, service):
        self.etcd_orm.save(service)

    def save_events(self, events):
        for event in events:
            self.etcd_orm.save(event)

    def update_tendrl_context(self, context):
        self.etcd_orm.save(context)

    def update_tendrl_definitions(self, definition):
        self.etcd_orm.save(definition)

    def update_pool(self, pool):
        self.etcd_orm.save(pool)
