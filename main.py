from influxdb import InfluxDBClient

from solarlog_exporter.parser import ConfigParser, DataParser


if __name__ == "__main__":
    # Read Configs
    config_parser = ConfigParser("testfiles/base_vars.js")
    inverters = config_parser.parse_inverter()

    # Parse Data of Solar Log
    min_parser = DataParser(inverters)
    min_parser.parse_file("testfiles/min_day.js")

    day_parser = DataParser(inverters)
    day_parser.parse_file("testfiles/days.js")

    # Store it in Influx DB
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

    client.drop_database('example')
    client.create_database('example')

    print(inverters.get_inverter_datapoints_to_influx())

    # print(influx_data)
