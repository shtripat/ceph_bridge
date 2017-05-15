from tendrl.commons import objects


class ECProfile(objects.BaseObject):
    def __init__(self, name=None, k=None,
                 m=None, plugin=None,
                 directory=None,
                 ruleset_failure_domain=None,
                 *args, **kwargs):
        super(ECProfile, self).__init__(*args, **kwargs)

        self.name = name
        # The no of data chunks
        self.k = k
        # The no of coding chunks
        # It means that `m` OSDs could be out without losing any data out of
        # total k+m
        self.m = m
        self.plugin = plugin
        self.directory = directory
        self.ruleset_failure_domain = ruleset_failure_domain
        self.value = 'clusters/{0}/ECProfiles/{1}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.name)
        return super(ECProfile, self).render()
