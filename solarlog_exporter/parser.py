import logging
import os

import pyjsparser

from solarlog_exporter.utils import MinDatapoint, DayDatapoint, InverterList, Client
from solarlog_exporter.utils import FileType


class Parser:
    """
    Main Parser for all file types
    """
    def parse_file(self, file_path):
        if not os.path.isfile(file_path):
            logging.error("File is not under path %s", self)

        file = open(file_path, "r")
        for line in file:
            self._parse_line(line)

    def _parse_line(self, line):
        pass


class ConfigParser(Parser):
    """
    Parser for config file (base_vars.js)
    """
    _config = {}

    def __init__(self, config_path):
        self._config_path = config_path
        self.parse_file(config_path)

    def _parse_line(self, line):
        _parsed_config = pyjsparser.parse(line)

        for i in _parsed_config["body"]:
            if i["type"] == "VariableDeclaration":
                if i["declarations"][0]["init"]["type"] == "Literal":
                    self._config[i["declarations"][0]["id"]["name"]] = i["declarations"][0]["init"]["raw"]
                elif i["declarations"][0]["init"]["type"] == "NewExpression":
                    temp = []
                    for j in i["declarations"][0]["init"]["arguments"]:
                        if j["type"] == "Literal":
                            temp.append(j["raw"])
                    self._config[i["declarations"][0]["id"]["name"]] = temp
            elif i["type"] == "ExpressionStatement":
                if i["expression"]["type"] == "AssignmentExpression" \
                        and i["expression"]["left"]["type"] == "MemberExpression":
                    if i["expression"]["left"]["object"]["type"] == "Identifier":
                        if not self._config.get(i["expression"]["left"]["object"]["name"]):
                            self._config[i["expression"]["left"]["object"]["name"]] = []

                        if i["expression"]["right"]["type"] == "Literal":
                            values = i["expression"]["right"]["value"]
                        elif i["expression"]["right"]["type"] == "NewExpression":
                            values = []
                            for k in i["expression"]["right"]["arguments"]:
                                if k["type"] == "Literal":
                                    values.append(k["value"])
                        else:
                            values = 0

                        self._config[i["expression"]["left"]["object"]["name"]].append(values)
                    if i["expression"]["left"]["object"]["type"] == "MemberExpression":
                        pass

    def get_power(self):
        return self._config["HPLeistung"]

    def get_title(self):
        return self._config["HPTitel"]

    def get_inverters(self):
        return InverterList(self._config["WRInfo"])


class DataParser(Parser):
    """
    Simple parser for minute and day-data
    """

    def __init__(self, inverters):
        self._inverters = inverters

    def _parse_line(self, line):
        file_type = FileType.get_filetype(line)
        if file_type is None:
            return

        record = line.split("=")[1].strip("\n").strip('\"')
        parts = record.split("|")
        date_time = parts[0]

        for i in range(1, len(parts)):
            values = parts[i].split(";")

            if file_type == FileType.MIN:
                datapoint = MinDatapoint(date_time, values[0], values[1], values[2], values[3],
                                         values[4] if (len(values) > 4) else 0)
                self._inverters.get_inverter(i - 1).add_datapoint(datapoint)
            elif file_type == FileType.DAY:
                datapoint = DayDatapoint(date_time, values[0])
                self._inverters.get_inverter(i - 1).add_datapoint(datapoint)
            elif file_type == FileType.MONTH:
                pass
            elif file_type == FileType.YEAR:
                pass
            else:
                logging.error("This filetype is not supported!")
