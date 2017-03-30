import json
import uuid

import etcd

job_id1 = str(uuid.uuid4())

job = {
    "integration_id": "ab3b125e-4769-4071-a349-e82b380c11f4",
    "run": "ceph.objects.Pool.flows.UpdatePool",
    "status": "new",
    "parameters": {
        "Pool.pool_id": 2,
        "Pool.pg_num": 240,
        "Pool.min_size": 2,
        "Pool.size": 2
    },
    "type": "sds",
    "node_ids": ["434d39ba-fff7-4b22-9ea0-c0fba75c27da"]
}

print("/queue/%s/" % job_id1)
client = etcd.Client(host="host", port=2379)
client.write("/queue/%s" % job_id1, None, dir=True)
client.write("/queue/%s/payload" % job_id1, json.dumps(job))
client.write("/queue/%s/status" % job_id1, "new")

