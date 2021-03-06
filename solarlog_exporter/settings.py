import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

TIMEZONE = os.getenv("TIMEZONE", "Europe/Berlin")
PROJECT_DIR = Path(__file__).parent.parent

DIR = os.getenv("DIR", str(PROJECT_DIR) + "/tmp")
SOLAR_LOG_SYSTEM = os.getenv("SOLAR_LOG_SYSTEM", "PV-Anlage")

# INFLUX
INFLUX_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUX_PORT = os.getenv("INFLUXDB_PORT", 8086)
INFLUX_USERNAME = os.getenv("INFLUXDB_ADMIN_USER", "root")
INFLUX_PASSWORD = os.getenv("INFLUXDB_ADMIN_PASSWORD", "root")
INFLUX_DB = os.getenv("INFLUXDB_DB")
