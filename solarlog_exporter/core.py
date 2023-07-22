from datetime import datetime
import logging
import os
from ftplib import FTP
from time import sleep
from typing import Set

from influxdb import InfluxDBClient

from solarlog_exporter import file_handler, settings
from solarlog_exporter.file_handler import (get_last_record_time_influxdb,
                                            is_import_file)
from solarlog_exporter.parser import ConfigParser, DataParser

CHUNK_SIZE = 10000


def start_import(
    path, influx_host, influx_port, influx_username, influx_password, influx_db
):
    """Start import with directory path"""
    influx_client = InfluxDBClient(
        influx_host, influx_port, influx_username, influx_password, influx_db
    )

    inverters = None
    last_record_time = get_last_record_time_influxdb(influx_client)
    logging.debug("Starting..")
    logging.debug("Used directory: %s", path)
    logging.debug("Last Record %s", last_record_time)

    # Read Configs at start
    if os.path.exists(path + "/base_vars.js"):
        config_parser = ConfigParser()
        config_parser.parse_file(path + "/base_vars.js")
        inverters = config_parser.get_inverters()
        logging.debug("Inverters read from config..")
    else:
        raise Exception("No inverters in config found!")

    # Read Daily and Monthly Data
    data_parser = DataParser(inverters, last_record_time)
    for file in os.listdir(path):
        if is_import_file(file, last_record_time):
            logging.debug("Read file %s", file)
            data_parser.parse_file(path + "/" + file)

    logging.debug("Daily and monthly data read..")

    # Store it in Influx DB
    datapoints = file_handler.chunks(
        inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
    )
    for chunk in datapoints:
        influx_client.write_points(chunk)
        logging.debug("Datapoints in influxdb saved")


def start_ftp_import(
    path,
    influx_host,
    influx_port,
    influx_username,
    influx_password,
    influx_db,
    mon_for_changes=False
):
    """Start import with directory path"""
    influx_client = InfluxDBClient(
        influx_host, influx_port, influx_username, influx_password, influx_db
    )

    inverters = None
    last_record_time = get_last_record_time_influxdb(influx_client)
    logging.debug("Starting..")
    logging.debug("Used directory: %s", path)
    logging.debug("Last Record %s", last_record_time)

    if not settings.FTP_HOST:
        raise Exception("FTP_HOST not defined!")

    with FTP(settings.FTP_HOST) as ftp:
        ftp.login(user=settings.FTP_USERNAME or "", passwd=settings.FTP_PASSWORD or "")

        # Read Configs at start
        config_parser = ConfigParser()
        config_parser.parse_ftp_file(ftp, path + "/base_vars.js")

        # Read Daily and Monthly Data
        if mon_for_changes:
            for add in changemon_ftp_directory(ftp, path):
                inverters = config_parser.get_inverters()
                if not inverters:
                    raise Exception("No inverters in config found!")
                logging.debug("Inverters read from config..")
                data_parser = DataParser(inverters, last_record_time)

                for file in add:
                    if is_import_file(file, last_record_time):
                        logging.debug("Read file %s", file)
                        data_parser.parse_ftp_file(ftp, path + "/" + file)

                logging.debug("Daily and monthly data read..")

                # Store it in Influx DB
                datapoints = file_handler.chunks(
                    inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
                )
                for chunk in datapoints:
                    influx_client.write_points(chunk)
                    logging.debug("Datapoints in influxdb saved")
        else:
            inverters = config_parser.get_inverters()
            if not inverters:
                raise Exception("No inverters in config found!")
            logging.debug("Inverters read from config..")
            data_parser = DataParser(inverters, last_record_time)

            for file in ftp.nlst(path):
                if is_import_file(file, last_record_time):
                    logging.debug("Read file %s", file)
                    data_parser.parse_ftp_file(ftp, path + "/" + file)

            logging.debug("Daily and monthly data read..")

            # Store it in Influx DB
            datapoints = file_handler.chunks(
                inverters.get_inverter_datapoints_to_influx(), CHUNK_SIZE
            )
            for chunk in datapoints:
                influx_client.write_points(chunk)
                logging.debug("Datapoints in influxdb saved")


def changemon_ftp_directory(ftp: FTP, directory="./"):
    """Check ftp directory for file changes"""
    ls_prev: Set[str] = set()

    while True:
        ls = set(ftp.nlst(directory))

        # listen for new files
        add = ls - ls_prev

        # read current date again
        add.add('min_day.js')
        add.add('days.js')

        if add:
            yield add

        ls_prev = ls
        sleep(20)
