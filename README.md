# SolarLog Exporter to InfluxDB
This repository contains an exporter for SolarLog Monitoring Systems. The Script does the following operations:
1. Get data from SFTP / LOCAL
2. Parse Config file
3. Parse min/daily files 
4. Add datapoints to influxDB

After that you can create fancy dashboards for grafana and monitor your PV-System. (my simple dashboard is in this repository under `docs/grafana.json`)

## Instructions:
1. Set Environment variables (more options under `solarlog_exporter/settings.py`:
    ```bash
    # SOLAR-LOG
    CLIENT=SFTP
    SOLAR_LOG_DIR=example
    SOLAR_LOG_SYSTEM="PV-System"
   
    # INFLUXDB
    INFLUXDB_HOST=influxdb
    INFLUXDB_PORT=8086
    INFLUXDB_ADMIN_USER=root
    INFLUXDB_ADMIN_PASSWORD=root
    INFLUXDB_DB=solarlog
   
    # SFTP (only if you want to connect to SFTP)
    SFTP_HOST=
    SFTP_USERNAME=
    SFTP_PASSWORD=
    ```
2. Create file `known_hosts` and enter your `~/.ssh/known_hosts` line, that includes your connection to the SFTP-Server (only necessary if you choose SFTP as the client)
3. Start Docker containers: `docker-compose up -d`
4. Run Grafana, add influxdb as a new datasource and import the dashboard under `docs/grafana.json`

## Important:
Use with caution! If you find any issues or improvements feel free to add pull requests or an issue!