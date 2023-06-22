"""
Mitsubishi monitor.
Its realtime monitoring of current feedback. Features are received as UDP packet approximately every 3.5ms.
PyPi package: https://pypi.org/project/mitsubishi-monitor/
"""
from mitsubishi_monitor import Monitor
from mitsubishi_monitor import DataType
from mitsubishi_monitor import parse_current_feedback
from datetime import datetime
from influxdb_client import Point


class MitsubishiMonitor:
    def __init__(self, ipaddr=None, port=None):
        """
        Initialize monitor.
        :param ipaddr: IP ADDR of robotic arm
        :param port: PORT or robotic arm
        """
        self.__name__ = 'Mitsubishi Monitor '+str(ipaddr)+'-'+str(port)
        self._ipaddr = ipaddr
        self._port = port
        self._monitor = None

    def begin(self):
        """
        Begin communication with LLC (logical link control) packet.
        After this message will robotic arm answer approximately every 3.6 ms.
        """
        self._monitor = Monitor(ip_addr=self._ipaddr,
                                port=self._port,
                                datatype=DataType.CURRENT_FEEDBACK.value)

        self._monitor.start_monitor()

    def get_feature(self):
        """
        Read response and return it.
        TODO: rename registers to J-
        """
        data = parse_current_feedback(self._monitor.receive_data())
        point = (Point("energy-consumption")
                 .tag('robotic-arm', self._ipaddr)
                 .field("M32", float(data[0]))
                 .field("M33", float(data[1]))
                 .field("M34", float(data[2]))
                 .field("M35", float(data[3]))
                 .field("M36", float(data[4]))
                 .field("M37", float(data[5]))
                 .time(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]))
        return point
