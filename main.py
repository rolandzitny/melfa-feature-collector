"""
Main program of asynchronous communication between Mitsubishi robotic arm and InfluxDB for collecting time series data.
"""
from config import get_config
from asyncio import sleep, get_event_loop
from feature_collector.datacollector import DataCollector
from feature_collector.datadispenser import DataDispenser
from feature_collector.collectors.monitor import MitsubishiMonitor
from feature_collector.dbs.influxdb import InfluxDatabase
from feature_collector.setup_logger import logger


async def obtain_feature(datacollector, sleep_time):
    """
    Asynchronous function for reading energy consumption from 6 register of robotic arm.
    :param datacollector: DataCollector class
    :param sleep_time: read interval in seconds
    """
    datacollector.begin_collecting()
    while True:
        await sleep(sleep_time)
        datacollector.collect()


async def save_features(datadispenser, sleep_time):
    """
    Asynchronous function for flushing obtained data from robotic arm into DB.
    :param datadispenser: DataDispenser class
    :param sleep_time: flush interval in seconds
    """
    while True:
        await sleep(sleep_time)
        datadispenser.flush_features()


def main():
    """
    Start two asynchronous parallel cycles.
    One cycle is for obtaining data points from robotic arm.
    Second cycle is for flushing obtained data into DB.
    """
    logger.info('Start main program')
    influx = InfluxDatabase(url=get_config('INFLUX_URL'),
                            token=get_config('INFLUX_TOKEN'),
                            org=get_config("INFLUX_ORG"),
                            bucket=get_config('INFLUX_BUCKET'))

    datadispenser = DataDispenser(db=influx)
    monitor = MitsubishiMonitor(ipaddr=get_config('DEVICE_IP'), port=get_config('DEVICE_PORT', wrapper=int))
    datacollector = DataCollector(collector=monitor, datadispenser=datadispenser)

    loop = get_event_loop()
    loop.create_task(obtain_feature(datacollector, get_config('FEATURE_SLEEP', wrapper=float)))
    loop.create_task(save_features(datadispenser, get_config('FEATURE_FLUSH', wrapper=float)))

    loop.run_forever()


if __name__ == "__main__":
    main()
