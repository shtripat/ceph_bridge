import uuid

from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration.manager.exceptions import \
    RequestStateError
from tendrl.commons import objects
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.ceph_integration.objects.rbd import Rbd
from tendrl.commons.event import Event
from tendrl.commons.objects.job import Job
from tendrl.commons.message import Message


class Create(objects.BaseAtom):
    obj = Rbd
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        # Checking if a new  pool has to be created or not rbd creation.
        if self.parameters['Rbd.create_pool'] is True and \
                        self.parameters['Rbd.pool_id'] is None:
            # Creating job for pool creation.
            if ['Rbd.pool_parameters'] in self.parameters:
                payload = {
                    "integration_id": NS.tendrl_context.integration_id,
                    "run": "ceph.flows.CreatePool",
                    "status": "new",
                    "parameters": self.parameters['Rbd.pool_parameters'],
                    "type": "sds",
                    "tags": ["ceph/mon"],
                    "parent": self.parameters['job_id']
                }
                _job_id = str(uuid.uuid4())
                Job(job_id=_job_id,
                    status="new",
                    payload=json.dumps(payload)).save()
                #Checking for successful pool creation
                pool_created=False
                job_status = "new"
                while not pool_created:
                    try:
                        job_status=NS.etcd_orm.client.read("/queue/%s/status" %
                                                       _job_id).value
                    except etcd.EtcdKeyNotFound:
                        #Failed to fetch pool creation status for rbd creation
                        break
                    if job_status == "finished":
                        pool_created = True
                    elif job_status == "failed":
                        break
                if not pool_created:
                    return False
            else:
                # Failed to create pool due to unavailability of attributes for
                # pool creation.
                return False

        # Setting pool_id for rbd creation
        pool_id = self._get_pool_id(self.parameters['Rbd.pool_parameters']
                                    ['Pool.poolname'])
        if pool_id:
            self.parameters['Rbd.pool_id'] = pool_id
        else:
            # Failed to fetch pool_id. Cannot create rbd without pool_id
            # TO delete created pool ?
            return False
        attrs = dict(name=self.parameters['Rbd.name'],
                     size=str(self.parameters['Rbd.size']),
                     pool_id=self.parameters.get('Rbd.pool_id')
                     )
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Creating rbd %s on pool %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        resp = crud.create("rbd", attrs)
        try:
            crud.sync_request_status(resp['request'])
        except RequestStateError as ex:
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to create rbd %s."
                        " Error: %s" % (self.parameters['Rbd.name'],
                                        ex)
                    },
                    job_id=self.parameters['job_id'],
                    flow_id=self.parameters['flow_id'],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Successfully created rbd %s on pool %s" %
                    (self.parameters['Rbd.name'],
                     self.parameters['Rbd.pool_id'])
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        pool_name = NS.etcd_orm.client.read(
            "clusters/%s/Pools/%s/pool_name" %
            (NS.tendrl_context.integration_id,
             self.parameters['Rbd.pool_id'])
        ).value
        rbd_details = NS.state_sync_thread._get_rbds(pool_name)
        for k, v in rbd_details.iteritems():
            NS.ceph.objects.Rbd(
                name=k,
                size=v['size'],
                pool_id=self.parameters['Rbd.pool_id'],
                flags=v['flags'],
                provisioned=NS.state_sync_thread._to_bytes(
                    v['provisioned']),
                used=NS.state_sync_thread._to_bytes(v['used'])
            ).save()

        return True


    def _get_pool_id(self, pool_name):
        try:
            pools = NS.etcd_orm.client.read(
                "clusters/%s/Pools" % NS.tendrl_context.integration_id
            )
        except etcd.EtcdKeyNotFound:
            # No pools available in cluster, return True
            return False

        for pool in pools._children:
            fetched_pool = Pool(
                pool_id=pool['key'].split('/')[-1]
            ).load()
            if fetched_pool.pool_name == pool_name:
                Event(
                    Message(
                        priority="info",
                        publisher=NS.publisher_id,
                        payload={
                            "message": "Found pool_id with pool_name %s" %s
                            pool_name
                        },
                        job_id=self.parameters['job_id'],
                        flow_id=self.parameters['flow_id'],
                        cluster_id=NS.tendrl_context.integration_id,
                    )
                )
                return fetched_pool.pool_id