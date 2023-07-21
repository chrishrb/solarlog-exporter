# SolarLog Exporter to InfluxDB
[![Version](https://img.shields.io/github/v/tag/chrishrb/solarlog-exporter?include_prereleases&style=plastic)](https://github.com/chrishrb/solarlog-exporter/releases)

[![Main Branch CI](https://github.com/chrishrb/solarlog-exporter/actions/workflows/pipeline.yml/badge.svg)](https://github.com/chrishrb/solarlog-exporter/actions/workflows/pipeline.yml)
[![Nightly Test](https://github.com/chrishrb/solarlog-exporter/actions/workflows/nightly.yml/badge.svg)](https://github.com/chrishrb/solarlog-exporter/actions/workflows/nightly.yml)
[![Release](https://github.com/chrishrb/solarlog-exporter/actions/workflows/release.yml/badge.svg)](https://github.com/chrishrb/solarlog-exporter/actions/workflows/release.yml)

This repository contains an exporter for SolarLog Monitoring Systems. The Script does the following operations:
1. Get data from LOCAL or FTP
2. Parse Config file
3. Parse min/daily files 
4. Add datapoints to influxDB

After that you can create fancy dashboards for grafana and monitor your PV-System. (my simple dashboard is in this repository under `docs/grafana.json`)

![grafana](docs/screenshot.png)

## Getting started:
1. Set Environment variables (e.g. create a .env file):
    ```bash
    # SOLAR-LOG
    SOLAR_LOG_NAME="PV-System"
    DIRECTORY= # if you want to use local files
    VERBOSE=true # verbose helps to debug the application
   
    # INFLUXDB
    INFLUXDB_HOST=influxdb
    INFLUXDB_DB=solarlog
    INFLUXDB_USERNAME=
    INFLUXDB_PASSWORD=
    INFLUXDB_DB=

    # FTP
    FTP_HOST=
    FTP_USERNAME=
    FTP_PASSWORD=
    FTP_DIRECTORY=
    FTP_MONITOR_FOR_CHANGES= # if you want to monitor the dir for changes

    ```
2. Start Docker containers: `docker-compose up -d`
3. Run Grafana, add influxdb as a new datasource and import the dashboard under `docs/grafana.json`

## Development

```bash
# Run tests
./bin/entrypoint test

# Start application
./bin/entrypoint
```

## Todo
- add target value
- add actual value in percent

## Important:
Use with caution! If you find any issues or improvements feel free to add pull requests or an issue!
