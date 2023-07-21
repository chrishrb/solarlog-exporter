import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

TIMEZONE = os.getenv("TIMEZONE", "Europe/Berlin")
PROJECT_DIR = str(Path(__file__).parent.parent)

# General
SOLAR_LOG_NAME = os.getenv("SOLAR_LOG_NAME", "PV-Anlage")
DIRECTORY = os.getenv("DIRECTORY")
VERBOSE =os.getenv("VERBOSE", 'False').lower() in ('true', '1')

# FTP
FTP_MONITOR_FOR_CHANGES =os.getenv("FTP_MONITOR_FOR_CHANGES", 'False').lower() in ('true', '1')
FTP_HOST = os.getenv("FTP_HOST")
FTP_USERNAME = os.getenv("FTP_USERNAME")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_DIRECTORY = os.getenv("FTP_DIRECTORY")

# INFLUX
INFLUXDB_HOST = os.getenv("INFLUXDB_HOST")
INFLUXDB_PORT = os.getenv("INFLUXDB_PORT", '8086')
INFLUXDB_USERNAME = os.getenv("INFLUXDB_ADMIN_USER", "root")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_ADMIN_PASSWORD", "root")
INFLUXDB_DB = os.getenv("INFLUXDB_DB")
