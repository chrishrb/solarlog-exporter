import logging
import os
from datetime import timezone, datetime

import pyjsparser
import pytz

import settings
from solarlog_exporter.line import Inverter, DayDatapoint


class FileType:
    DAY = 1
    MONTH = 2
    YEAR = 3


class ConfigParser:
    _config = {}

    def __init__(self, config_path):
        self._config_path = config_path

    def parse_config(self):
        f = open(self._config_path, "r")
        _parsed_config = pyjsparser.parse(f.read())

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

    def get_inverter(self, key):
        if key < 0 or key >= self.get_number_of_inverters():
            return None
        return self._config["WRInfo"][key]

    def get_number_of_inverters(self):
        return len(self._config["WRInfo"])

    def get_power(self):
        return self._config["HPLeistung"]

    def get_title(self):
        return self._config["HPTitel"]


class DataParser:
    _inverters = []

    def __init__(self, config_parser):
        if config_parser.get_number_of_inverters == 0:
            raise Exception("No inverter in config found!")

        for i in range(0, config_parser.get_number_of_inverters()):
            self._inverters.append(Inverter(config_parser.get_inverter(i)))

    def parse_file(self, file_path):
        if not os.path.isfile(file_path):
            logging.error("File is not under path %s", self)

        file = open(file_path, "r")
        for line in file:
            self._parse_line(line)

    def _parse_line(self, line):
        record = line.split("=")[1].strip("\n").strip('\"')
        parts = record.split("|")
        file_type = get_filetype(line)
        date_time = parts[0]

        for i in range(1, len(parts)):
            values = parts[i].split(";")

            if file_type == FileType.DAY:
                datapoint = DayDatapoint(date_time, values[0], values[1], values[2], values[3])
                self._inverters[i - 1].add_datapoint(datapoint)
            elif file_type == FileType.MONTH:
                pass
            elif file_type == FileType.YEAR:
                pass
            else:
                logging.error("This filetype is not supported!")

    def get_influx_datapoints(self):
        datapoints = []

        for inverter in self._inverters:
            datapoints += inverter.get_influx_datapoints()

        return datapoints


def get_filetype(line):
    if line.startswith("m[mi++]="):
        return FileType.DAY
    elif line.startswith("mo[mx++]="):
        return FileType.MONTH
    elif line.startswith("ye[yx++]="):
        return FileType.YEAR
    else:
        return None
