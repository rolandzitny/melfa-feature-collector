"""
Communicator communicate with Mitsubishi robotic arm, using SLMP protocol and slmpclient
library from https://pypi.org/project/slmpclient/. Check documentation there to understand creation of messages.
This communicator serves to obtain values of energy consumption registers, which are 6 of them and 1 register is
synchronization flag.
Response is parsed and from data are created InfluxDB points, which are saved into internal queue of Collector.
"""
import struct
from datetime import datetime
from influxdb_client import Point
from slmpclient import UnwantedResponse
from slmpclient import SLMPClient, SLMPPacket, FrameType, ProcessorNumber, TimerValue, SLMPCommand, SLMPSubCommand


class SLMPCollector:
    def __init__(self, ipaddr=None, port=None, tcp=True):
        """
        Initialize Communicator.
        :param ipaddr: IP ADDR of robotic arm
        :param port: PORT or robotic arm
        :param tcp: Flag -> True = TCP, False = UDP
        """
        self.__name__ = 'SLMP '+ str(ipaddr)+'-'+str(port)+'-'+str(tcp)
        self._ipaddr = ipaddr
        self._port = port
        self._tcp = tcp
        self._client = SLMPClient(ip_addr=self._ipaddr, port=self._port, tcp=self._tcp)
        self._request = None
        self._response = None

    def begin(self):
        """
        Begin communication by connecting socket (Handshake).
        There in SLMP is also created message, for more intel check https://pypi.org/project/slmpclient
        and DOC about SLMP protocol.
        """
        self._client.open()
        pucData = b'\xAC\x12\x00\xA8\x1C\x00'  # Reading will start from register D4780, and takes 28 words
        slmp_controller = SLMPPacket(ulFrameType=FrameType.SLMP_FTYPE_BIN_REQ_ST.value,
                                     usNetNumber=0,
                                     usNodeNumber=0xFF,
                                     usProcNumber=ProcessorNumber.SLMP_CPU_DEFAULT.value,
                                     usTimer=TimerValue.SLMP_TIMER_WAIT_FOREVER.value,
                                     usCommand=SLMPCommand.SLMP_COMMAND_DEVICE_READ.value,
                                     usSubCommand=SLMPSubCommand.SUB_word0.value, pucData=pucData)

        self._request = slmp_controller.create_stream()

    def send_request(self):
        """
        Send request to robotic arm and save response into self._response.
        """
        self._client.send(self._request)
        self._response = self._client.receive()

    def parse_response(self):
        """
        Parsing of SLMP response.
        :returns True/False, [data], True -> write, False -> skip
        """
        # Check whether answer is ok, if not exception
        # May occur when SLMP server does not understand request
        if self._response[8:10] != b'\x00\x00' or len(self._response) < 67:     # length of 7 registers
            raise UnwantedResponse

        data = struct.unpack('<ddddddd', self._response[11:67])     # transfer 7 register values into readable form

        # Synchronization, if synchronization register (M38) == 1 write data
        if data[0] == 1:
            return True, [data[6], data[5], data[4], data[3], data[2], data[1]]  # M32, M33, M34, M35, M36, M37
        return False, []

    def get_feature(self):
        """
        Creates Influx point from response and save into internal queue of Collector.
        TODO: rename registers to J-
        """
        self.send_request()
        ready_flag, data = self.parse_response()
        if ready_flag:
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
