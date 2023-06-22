"""
InfluxDBClient
"""
import logging
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.influxdb_client import InfluxDBClient


class InfluxDatabase:
    def __init__(self, url=None, token=None, org=None, bucket=None):
        """
        Initialize Collector class and set parameters for InfluxDBClient.
        :param url: InfluxDB url
        :param token: InfluxDB token
        :param org: InfluxDB organization
        :param bucket: InfluxDB bucket
        """
        self.__name__ = 'InfluxDB ' + str(url) + '-' + str(org) + '-' + str(bucket)
        self._url = url
        self._token = token
        self._org = org
        self._bucket = bucket
        self.logger = logging.getLogger(__name__)

    def flush(self, queue):
        """
        Method for flushing data into InfluxDB. This method needs to be called at defined intervals.
        This method takes all data from Collectors points_queue, till it reach empty queue.
        """
        with InfluxDBClient(url=self._url, token=self._token, org=self._org) as influx_client:
            write_api = influx_client.write_api(write_options=ASYNCHRONOUS)
            record = []

            while len(queue) != 0:
                record.append(queue.pop(0))

            try:
                write_api.write(bucket=self._bucket, record=record)
            except InfluxDBError:
                self.logger.critical("Collector can not flush data into database - measuring is useless")
                raise Exception("Can not flush data!")
