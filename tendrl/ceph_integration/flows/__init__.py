from tendrl.commons import flows


class CephIntegrationBaseFlow(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(CephIntegrationBaseFlow, self).__init__(*args, **kwargs)
