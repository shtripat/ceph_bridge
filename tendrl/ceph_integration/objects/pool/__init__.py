from tendrl.commons import objects


class Pool(objects.BaseObject):
    def __init__(self, pool_id=None,
                 pool_name=None, pg_num=None, min_size=None, size=None,
                 used=None, percent_used=None,
                 deleted=None, type=None,
                 erasure_code_profile=None,
                 quota_enabled=None, quota_max_objects=None,
                 quota_max_bytes=None, *args, **kwargs):
        super(Pool, self).__init__(*args, **kwargs)

        self.pool_id = pool_id
        self.pool_name = pool_name
        self.pg_num = pg_num
        self.min_size = min_size
        self.size = size
        self.used = used
        self.percent_used = percent_used
        self.deleted = deleted
        self.type = type
        self.erasure_code_profile = erasure_code_profile
        self.quota_enabled = quota_enabled
        self.quota_max_objects = quota_max_objects
        self.quota_max_bytes = quota_max_bytes
        self.value = 'clusters/{0}/Pools/{1}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.pool_id)
        return super(Pool, self).render()
