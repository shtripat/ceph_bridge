import subprocess

def get_sds_version():
    res = subprocess.check_output(['ceph', '--version'])
    return res.split()[2].split("-")[0]
