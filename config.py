"""
Configuration file for Docker.
This file consists from SLMPClient parameters and InfluxDB parameters.
"""
import os
from typing import Callable

DEFAULT_CONFIG = {
    # INFLUX
    'INFLUX_URL': 'http://localhost:4050',
    'INFLUX_TOKEN': 'token',
    'INFLUX_ORG': 'org',
    'INFLUX_BUCKET': 'slmp',
    # DEVICE
    'DEVICE_IP': '192.168.10.201',
    'DEVICE_PORT': 4050,
    # SLMP
    'SLMP_TCP': 1,
    # TIMING
    'FEATURE_SLEEP': 0,
    'FEATURE_FLUSH': 3,
    # LOGGING
    'LOG_LEVEL': 'DEBUG'
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))
