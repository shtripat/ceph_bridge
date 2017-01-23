import datetime
from tendrl.ceph_integration.manager import event_utils


def test_severity_str_critical():
    assert event_utils.severity_str(1) == 'CRITICAL'


def test_severity_str_error():
    assert event_utils.severity_str(2) == 'ERROR'


def test_severity_str_warning():
    assert event_utils.severity_str(3) == 'WARNING'


def test_severity_str_recovery():
    assert event_utils.severity_str(4) == 'RECOVERY'


def test_severity_str_info():
    assert event_utils.severity_str(5) == 'INFO'


def test_severity_from_str_critical():
    assert event_utils.severity_from_str("CRITICAL") == 1


def test_severity_from_str_error():
    assert event_utils.severity_from_str("ERROR") == 2


def test_severity_from_str_warning():
    assert event_utils.severity_from_str("WARNING") == 3


def test_severity_from_str_recovery():
    assert event_utils.severity_from_str("RECOVERY") == 4


def test_severity_from_str_info():
    assert event_utils.severity_from_str("INFO") == 5


class Test_Event(object):
    def test_Event(self):
        self.event = tendrl_ns.ceph_integration.objects.Event()
        self.event.when = datetime.datetime(2008, 9, 3)
        assert self.event._etcd_cls.render() == [
            {
                'value': None,
                'name': 'fqdn',
                'key': '/clusters/None/events/None/fqdn',
                'dir': False
            },
            {
                'value': None,
                'name': 'fsid',
                'key': '/clusters/None/events/None/fsid',
                'dir': False
            },
            {
                'value': None,
                'name': 'uuid',
                'key': '/clusters/None/events/None/uuid',
                'dir': False
            },
            {
                'value': None,
                'name': 'message',
                'key': '/clusters/None/events/None/message',
                'dir': False
            },
            {
                'value': None,
                'name': 'service_id',
                'key': '/clusters/None/events/None/service_id',
                'dir': False
            },
            {
                'value': None,
                'name': 'service_type',
                'key': '/clusters/None/events/None/service_type',
                'dir': False
            },
            {
                'value': None,
                'name': 'severity',
                'key': '/clusters/None/events/None/severity',
                'dir': False
            },
            {
                'value': '2008-09-03T00:00:00',
                'name': 'when',
                'key': '/clusters/None/events/None/when',
                'dir': False
            }]
