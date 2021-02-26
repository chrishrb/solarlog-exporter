import logging
import os

from influxdb import InfluxDBClient

from solarlog_exporter import settings, file_handler
from solarlog_exporter.file_handler import SFTPConnection, get_last_record_time_influxdb
from solarlog_exporter.parser import ConfigParser, DataParser

if __name__ == "__main__":
    influx_client = InfluxDBClient(settings.INFLUX_HOST, settings.INFLUX_PORT, settings.INFLUX_USERNAME,
                                   settings.SFTP_PASSWORD, settings.INFLUX_DB)

    influx_client.drop_database("example")
    influx_client.create_database("example")

    inverters = None
    last_record_time = get_last_record_time_influxdb(influx_client)
    logging.debug("Starting..")

    if settings.CLIENT == "SFTP":
        sftp_client = SFTPConnection(settings.SFTP_HOST, settings.SFTP_USERNAME, settings.SFTP_PASSWORD)
        sftp_client.get_solarlog_files(influx_client, last_record_time)
        logging.info("Getting data from SFTP Server")
        del sftp_client

    # Read Configs at start
    if os.path.exists(settings.CLIENT_DIR + "/base_vars.js"):
        config_parser = ConfigParser(settings.CLIENT_DIR + "/base_vars.js")
        inverters = config_parser.get_inverters()
        logging.debug("Inverters read from config..")
    else:
        logging.error("No inverters in config found!")
        exit(1)

    # Read Daily and Monthly Data
    data_parser = DataParser(inverters, last_record_time)
    for file in os.listdir(settings.CLIENT_DIR):
        if file.startswith("min") or file.startswith("days"):
            logging.debug("Read file %s", file)
            data_parser.parse_file(settings.CLIENT_DIR + "/" + file)

    logging.debug("Daily Data read..")
    # Store it in Influx DB
    datapoints = file_handler.chunks(inverters.get_inverter_datapoints_to_influx(), 8000)
    for chunk in datapoints:
        influx_client.write_points(chunk)
        logging.debug("Datapoints in influxdb saved")
