import logging

from tendrl.ceph_bridge.config import TendrlConfig
config = TendrlConfig()


FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
root = logging.getLogger()
handler = logging.FileHandler(config.get('ceph_bridge', 'log_path'))
handler.setFormatter(logging.Formatter(FORMAT))
root.addHandler(handler)
root.setLevel(logging.getLevelName(config.get('ceph_bridge', 'log_level')))
