
CRITICAL = 1
ERROR = 2
WARNING = 3
RECOVERY = 4
INFO = 5

SEVERITIES = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    RECOVERY: "RECOVERY",
    INFO: "INFO"
}

STR_TO_SEVERITY = dict([(b, a) for (a, b) in SEVERITIES.items()])


def severity_str(severity):
    return SEVERITIES[severity]


def severity_from_str(severitry_str):
    return STR_TO_SEVERITY[severitry_str]
