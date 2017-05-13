from tendrl.commons import objects


class SyncObject(objects.BaseObject):
    def __init__(self, sync_type=None, version=None, when=None,
                 data=None, updated=None, *args, **kwargs):
        super(SyncObject, self).__init__(*args, **kwargs)

        self.sync_type = sync_type
        self.version = version
        self.when = when
        self.data = data
        self.updated = updated
        self.value = 'clusters/{0}/maps/{1}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.sync_type)
        return super(SyncObject, self).render()
