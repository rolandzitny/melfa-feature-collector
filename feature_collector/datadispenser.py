"""
DataDispenser is a wrapper over any type of database that is used
to store collected data in its internal queue, which is then periodically flushed to the server.

It is necessary to pay attention to the fact that data parsing is performed with
attention to the type of used database. This means that when using InfluxDB,
it is necessary to have an initialized collector(e.g. slmp.py class) inside the DataCollector with a parser
converting data to Influx.DataPoint.

The points created in this way are stored in the queue as objects,
and the flush_features method periodically empties this queue and sends it to the server.
"""
import logging


class DataDispenser:
    def __init__(self, db=None):
        """
        Initialization of DataDispenser.
        :param db: specific database - dir feature_collector/dbs
        """
        self._db = db
        self._queue = []    # Queue for data
        self.logger = logging.getLogger(__name__)
        self.logger.info("DataDispenser was initialized with database  : {}".format(self._db.__name__))

    def save_feature(self, feature):
        """
        Appends feature into internal queue of DataDispenser.
        :param feature: feature from collector.get_feature()

        Feature itself needs to be in correct form, based on database type. (e.g. InfluxDBD = InfluxPoints)
        """
        self._queue.append(feature)

    def flush_features(self):
        """
        Empties internal queue and flushes data into database.
        """
        self._db.flush(self._queue)
        self.logger.info("Data were flushed: No. {} - {}".format(len(self._queue), self._db.__name__))
