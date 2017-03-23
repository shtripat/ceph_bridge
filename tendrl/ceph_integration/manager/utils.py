import logging
import os
import os.path
import subprocess

LOG = logging.getLogger(__name__)


def get_sds_version():
    res = subprocess.check_output(['ceph', '--version'])
    return res.split()[2].split("-")[0]
