from influxdb import InfluxDBClient

from solarlog_exporter.parser import ConfigParser, DataParser

if __name__ == "__main__":
    # Read Configs
    config_parser = ConfigParser("testfiles/base_vars.js")

    # Parse Data of Solar Log
    min_parser = DataParser(config_parser)
    min_parser.parse_file("testfiles/min_day.js")
    influx_data = min_parser.get_inverter_datapoints_to_influx()

    day_parser = DataParser(config_parser)
    day_parser.parse_file("testfiles/days.js")
    influx_data_mon = day_parser.get_inverter_datapoints_to_influx()

    # Store it in Influx DB
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

    client.drop_database('example')
    client.create_database('example')
    client.write_points(influx_data)
    client.write_points(influx_data_mon)

    #print(influx_data)
