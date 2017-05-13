from tendrl.commons import objects


class Rbd(objects.BaseObject):
    def __init__(self, name=None, size=None,
                 pool_id=None, flags=None, provisioned=None,
                 used=None, *args, **kwargs):
        super(Rbd, self).__init__(*args, **kwargs)

        self.name = name
        self.size = size
        self.pool_id = pool_id
        self.flags = flags
        self.provisioned = provisioned
        self.used = used
        self.value = 'clusters/{0}/Pools/{1}/Rbds/{2}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.pool_id, self.name)
        return super(Rbd, self).render()
