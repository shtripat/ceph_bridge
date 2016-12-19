from tendrl.common.atoms.base_atom import BaseAtom


class Delete(BaseAtom):
    def run(self, parameters):
        cluster_id = parameters['Tendrl_context.cluster_id']
        pool_id = parameters['Pool.pool_id']
        parameters['crud'].delete(
            parameters['fsid'],
            "pool",
            pool_id
        )

        etcd_client = parameters['etcd_client']
        pool_key = "clusters/%s/Pools/%s/deleted" % (cluster_id, pool_id)
        etcd_client.write(pool_key, "True")

        return True
