from tendrl.commons import objects


class Utilization(objects.BaseObject):
    def __init__(self, total=None, used=None,
                 available=None, pcnt_used=None,
                 *args, **kwargs):
        super(Utilization, self).__init__(*args, **kwargs)

        self.total = total
        self.used = used
        self.available = available
        self.pcnt_used = pcnt_used
        self.value = 'clusters/{0}/Utilization'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id)
        return super(Utilization, self).render()
