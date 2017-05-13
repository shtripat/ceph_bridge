from tendrl.commons import objects


class GlobalDetails(objects.BaseObject):
    def __init__(self, status=None, *args, **kwargs):
        super(GlobalDetails, self).__init__(*args, **kwargs)

        self.status = status
        self.value = 'clusters/{0}/GlobalDetails'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id)
        return super(GlobalDetails, self).render()
