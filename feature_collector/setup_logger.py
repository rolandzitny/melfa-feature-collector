import sys
import logging
from config import get_config


_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def log_level(level) -> int:
    """
        Method convert text representation of log level to int log level.
    """
    if isinstance(level, str):
        _level = level.upper()
        if _level not in _nameToLevel:
            raise AttributeError('Unknown log level "{}"'.format(level))
        return _nameToLevel[_level]
    return level


class LogFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level


LOG_LEVEL = get_config('LOG_LEVEL', wrapper=log_level)

DEBUGGING_LOG_LEVEL = {
    'slmpclient.client': logging.INFO,
    'slmpclient.slmp_controller': logging.INFO,
}

root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
FORMATTER = logging.Formatter('%(asctime)s  [%(levelname)s] %(name)s: %(message)s')

handler_stdout = logging.StreamHandler(sys.stdout)
handler_stdout.addFilter(LogFilter(logging.WARNING))
handler_stdout.setFormatter(FORMATTER)
handler_stdout.setLevel(LOG_LEVEL)

handler_stderr = logging.StreamHandler(sys.stderr)
handler_stderr.setFormatter(FORMATTER)
handler_stderr.setLevel(max(LOG_LEVEL, logging.WARNING))

root_logger.addHandler(handler_stdout)
root_logger.addHandler(handler_stderr)


for log_name, level in DEBUGGING_LOG_LEVEL.items():
    logging.getLogger(log_name).setLevel(level)

logger = logging.getLogger('collector')
