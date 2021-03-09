import logging
import os

from influxdb import InfluxDBClient

from solarlog_exporter import settings, file_handler
from solarlog_exporter.file_handler import get_last_record_time_influxdb, is_import_file
from solarlog_exporter.parser import ConfigParser, DataParser

if __name__ == "__main__":
    influx_client = InfluxDBClient(settings.INFLUX_HOST, settings.INFLUX_PORT, settings.INFLUX_USERNAME,
                                   settings.INFLUX_PASSWORD, settings.INFLUX_DB)

    inverters = None
    last_record_time = get_last_record_time_influxdb(influx_client)
    logging.debug("Starting..")
    logging.debug("Used directory: " + settings.DIR)
    logging.debug("Last Record %s", last_record_time)

    # Read Configs at start
    if os.path.exists(settings.DIR + "base_vars.js"):
        config_parser = ConfigParser(settings.DIR + "base_vars.js")
        inverters = config_parser.get_inverters()
        logging.debug("Inverters read from config..")
    else:
        logging.error("No inverters in config found!")
        exit(1)

    # Read Daily and Monthly Data
    data_parser = DataParser(inverters, last_record_time)
    for file in os.listdir(settings.DIR):
        if is_import_file(file, last_record_time):
            logging.debug("Read file %s", file)
            data_parser.parse_file(settings.DIR + file)

    logging.debug("Daily Data read..")

    # Store it in Influx DB
    datapoints = file_handler.chunks(inverters.get_inverter_datapoints_to_influx(), 10000)
    for chunk in datapoints:
        influx_client.write_points(chunk)
        logging.debug("Datapoints in influxdb saved")
