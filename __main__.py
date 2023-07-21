import logging
import sys

from solarlog_exporter import settings
from solarlog_exporter.core import start_ftp_import, start_import

def main():
    """
    Run main application with can interface
    """
    # Verbose output
    if settings.VERBOSE is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not settings.INFLUXDB_HOST or not settings.INFLUXDB_DB:
        raise Exception('INFLUX_HOST or INFLUX_DB not defined!')

    # scan directory
    if settings.DIRECTORY:
        start_import(
            settings.DIRECTORY,
            influx_host=settings.INFLUXDB_HOST,
            influx_port=settings.INFLUXDB_PORT,
            influx_username=settings.INFLUXDB_USERNAME,
            influx_password=settings.INFLUXDB_PASSWORD,
            influx_db=settings.INFLUXDB_DB,
        )

    # scan with ftp
    if settings.FTP_DIRECTORY:
        start_ftp_import(
            settings.FTP_DIRECTORY,
            influx_host=settings.INFLUXDB_HOST,
            influx_port=settings.INFLUXDB_PORT,
            influx_username=settings.INFLUXDB_USERNAME,
            influx_password=settings.INFLUXDB_PASSWORD,
            influx_db=settings.INFLUXDB_DB,
            mon_for_changes=settings.FTP_MONITOR_FOR_CHANGES
        )

    raise Exception('One env variable of DIRECTORY or FTP_DIRECTORY must be defined!')


if __name__ == "__main__":
    sys.exit(main())
