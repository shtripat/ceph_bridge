import logging

from tendrl.commons import flows
from tendrl.ceph_integration import objects


class CephIntegrationBaseFlow(flows.BaseFlow):
    obj = objects.CephIntegrationBaseObject

    def __init__(self, *args, **kwargs):
        super(CephIntegrationBaseFlow, self).__init__(*args, **kwargs)
