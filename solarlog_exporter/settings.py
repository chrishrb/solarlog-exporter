import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

TIMEZONE = os.getenv("TIMEZONE", "Europe/Berlin")
PROJECT_DIR = Path(__file__).parent.parent

# Local/SFTP
CLIENT = os.getenv("CLIENT", "LOCAL")
TMP_DIR = str(PROJECT_DIR) + "/tmp"
SOLAR_LOG_DIR = os.getenv("SOLAR_LOG_DIR", "")
SOLAR_LOG_SYSTEM = os.getenv("SOLAR_LOG_SYSTEM", "PV-Anlage")

# INFLUX
INFLUX_HOST = os.getenv("INFLUX_HOST", "localhost")
INFLUX_PORT = os.getenv("INFLUX_PORT", 8086)
INFLUX_USERNAME = os.getenv("INFLUX_USERNAME", "root")
INFLUX_PASSWORD = os.getenv("INFLUX_PASSWORD", "root")
INFLUX_DB = os.getenv("INFLUX_DB")

# SFTP
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = os.getenv("SFTP_PORT", 22)
SFTP_USERNAME = os.getenv("SFTP_USERNAME")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")
