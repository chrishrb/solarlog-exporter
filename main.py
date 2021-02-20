import pyjsparser

from solarlog_exporter.parser import ConfigParser, DataParser

if __name__ == "__main__":
    # Read Configs
    config_parser = ConfigParser("testfiles/base_vars.js")
    config_parser.parse_config()

    # Parse Data of Solar Log
    data_parser = DataParser(config_parser)
    data_parser.parse_file("testfiles/min200606.js")
    influx_data = data_parser.get_influx_datapoints()

    # Store it in Influx DB

    print(influx_data)
