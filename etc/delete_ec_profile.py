import json
import uuid

import etcd

job_id = str(uuid.uuid4())

job = {
    "integration_id": "89604c6b-2eff-4221-96b4-e41319240240",
    "run": "ceph.objects.ECProfile.flows.DeleteECProfile",
    "status": "new",
    "parameters": {
        "ECProfile.name": "ecprofile1",
    },
    "type": "sds",
    "node_ids": ["aee2f7d3-7e1a-4d5f-b83b-0f4b057ca627"]
}

print("/queue/%s/" % job_id)
client = etcd.Client(host="host", port=2379)
client.write("/queue/%s" % job_id, None, dir=True)
client.write("/queue/%s/payload" % job_id, json.dumps(job))
client.write("/queue/%s/status" % job_id, "new")
