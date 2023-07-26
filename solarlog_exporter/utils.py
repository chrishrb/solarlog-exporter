from operator import itemgetter
import re
from abc import abstractmethod
from datetime import datetime
from typing import Optional

import pytz as pytz

from solarlog_exporter import settings


class FileType:
    """
    File Types for SolarLog datas
    """

    MIN = 1
    DAY = 2
    MONTH = 3
    YEAR = 4

    @staticmethod
    def get_filetype(line):
        if line.startswith("m[mi++]="):
            return FileType.MIN
        elif line.startswith("da[dx++]="):
            return FileType.DAY
        else:
            return None


class Inverter:
    """
    Inverter Object
    """

    def __init__(self, inverter_config, system):
        self.datapoints_min = {}
        self.datapoints_day = {}

        self.name = inverter_config[0][4]
        self.system = system
        if re.match(r"WR \d*", self.name):
            self.name = self.name[:3] + self.name[3:].zfill(2)
        self.type = inverter_config[0][0]
        self.power = inverter_config[0][2]
        if len(inverter_config) > 1:
            self.group = inverter_config[1]
        else:
            self.group = None

    def add_datapoint(self, datapoint, last_record_time):
        if datapoint.date_time.date() < last_record_time.date():
            return

        if datapoint.type == FileType.MIN:
            self.datapoints_min[datapoint.get_date_time_as_timestring()] = datapoint
        elif datapoint.type == FileType.DAY:
            self.datapoints_day[datapoint.get_date_time_as_datestring()] = datapoint

    def get_datapoints_to_influx(self):
        self._add_values_to_datapoint()
        influx_datapoints = []

        for _, value in self.datapoints_min.items():
            influx_datapoints.append(value.get_datapoint_to_influx(self))

        for _, value in self.datapoints_day.items():
            influx_datapoints.append(value.get_datapoint_to_influx(self))

        return influx_datapoints

    def _add_values_to_datapoint(self):
        for datapoint_min in self.datapoints_min.values():
            if datapoint_min.get_date_time_as_datestring() in self.datapoints_day:
                self.datapoints_day[
                    datapoint_min.get_date_time_as_datestring()
                ].add_min_datapoint(datapoint_min.date_time, datapoint_min.pac, datapoint_min.pdc, datapoint_min.eday)

        for _, value in self.datapoints_day.items():
            value.calculate_values()


class InverterList:
    """
    List of all inverters found in the config
    """

    def __init__(self, inverter_config, system):
        self.inverters = []

        if len(inverter_config) == 0:
            raise ValueError("No inverter in config found")

        if not system:
            raise ValueError("No name of system provided")

        for inverter in inverter_config:
            self.inverters.append(Inverter(inverter, system))

    def get_inverter(self, key) -> Optional[Inverter]:
        if key < 0 or key >= self.get_number_of_inverters():
            return None
        return self.inverters[key]

    def get_number_of_inverters(self):
        return len(self.inverters)

    def get_inverter_datapoints_to_influx(self):
        datapoints = []

        for inverter in self.inverters:
            datapoints += inverter.get_datapoints_to_influx()

        return datapoints


class Datapoint:
    """
    Basic Datapoint
    """

    _timezone = pytz.timezone(settings.TIMEZONE)
    date_time = datetime.now()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.date_time == other.date_time

    @abstractmethod
    def get_datapoint_to_influx(self, inverter):
        pass

    def get_date_time_as_timestring(self):
        return self.date_time.strftime("%d.%m.%y %H:%M:%S")

    def get_date_time_as_datestring(self):
        return self.date_time.date().strftime("%d.%m.%y")

    def get_date_time_for_influxdb(self):
        return self.date_time.astimezone(pytz.utc).isoformat().replace("+00:00", "Z")


class MinDatapoint(Datapoint):
    """
    Minute Datapoint (min_xxxx.js)
    """

    influx_measurment_name = "solarlog_min"
    type = FileType.MIN

    def __init__(self, min_time, pac, pdc, eday, udc, temperature):
        self.date_time = self._timezone.localize(
            datetime.strptime(min_time, "%d.%m.%y %H:%M:%S")
        )
        self.pac = float(pac)
        self.pdc = float(pdc)
        self.eday = float(eday)
        self.udc = float(udc)
        self.temperature = int(temperature)

    def get_datapoint_to_influx(self, inverter):
        return {
            "measurement": self.influx_measurment_name,
            "tags": {
                "inverter": inverter.name,
                "system": inverter.system,
                "group": inverter.group,
            },
            "time": self.get_date_time_for_influxdb(),
            "fields": {
                "Pac": self.pac,
                "Pdc": self.pdc,
                "Eday": self.eday,
                "Udc": self.udc,
                "temperature": self.temperature,
            },
        }


class DayDatapoint(Datapoint):
    """
    Day Datapoint (days.js, days_hist.js)
    """

    influx_measurment_name = "solarlog_day"
    type = FileType.DAY

    def __init__(self, day_time, pac):
        self.date_time = self._timezone.localize(
            datetime.strptime(day_time, "%d.%m.%y")
        )
        self.pac = float(pac)
        self._pdc_min_data = []
        self.efficiency = float(0)
        self.pdc = float(0)

    def get_datapoint_to_influx(self, inverter):
        return {
            "measurement": self.influx_measurment_name,
            "tags": {
                "inverter": inverter.name,
                "system": inverter.system,
                "group": inverter.group,
            },
            "time": self.get_date_time_for_influxdb(),
            "fields": {"Pac": self.pac, "Pdc": self.pdc, "efficiency": self.efficiency},
        }

    def add_min_datapoint(self, time, pac, pdc, eday):
        self._pdc_min_data.append({"time": time, "pac": pac, "pdc": pdc, "eday": eday})

    def calculate_values(self):
        ist_ertrag_ac_yield = self._pdc_min_data[0]['eday']
        ist_ertrag_ac = 0.0
        pdc = 0.0

        for i in range(1, len(self._pdc_min_data)):
            dt = (self._pdc_min_data[i]['time'] - self._pdc_min_data[i - 1]['time'])
            hour_diff = abs(dt.total_seconds()) / (60.0 * 60.0)
            pdc += self._pdc_min_data[i]['pdc'] * hour_diff
            ist_ertrag_ac += self._pdc_min_data[i]['pac'] * hour_diff

        if ist_ertrag_ac == 0:
            factor = 1.0
        else:
            factor = ist_ertrag_ac_yield / ist_ertrag_ac

        self.pdc = round(pdc * factor, 0)
        if self.pdc != 0 and self.pac != 0:
            self.efficiency = round((self.pac / self.pdc), 3)
