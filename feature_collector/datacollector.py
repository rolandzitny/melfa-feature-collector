"""
DataCollector is a wrapper over the method of collecting data from the requested device.
The DataCollector must be initialized with the DataDispenser in order to insert
the obtained data into its internal queue, which is periodically flushed to the database.
"""
import logging


class DataCollector:
    def __init__(self, collector=None, datadispenser=None):
        """
        Initialization of Datacollector.
        :param collector: method for collecting data - dir feature_collector/collectors
        :param datadispenser: wrapper over required database
        """
        self._collector = collector
        self._datadispenser = datadispenser
        self.logger = logging.getLogger(__name__)
        self.logger.info("DataCollector was initialized with collector : {}".format(self._collector.__name__))

    def begin_collecting(self):
        """
        Start communication between collector and device.
        For TCP communication performs handshake and connects socket. -> slmp.py
        For UDP communication sends initial message e.g. LLC message  -> monitor.py (real-time).
        """
        self._collector.begin()
        self.logger.info("Collecting began: {}".format(self._collector.__name__))

    def collect(self):
        """
        Receive data from collector and save it into internal queue of datadispenser.
        """
        self._datadispenser.save_feature(self._collector.get_feature())


