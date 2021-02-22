from datetime import datetime

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
        elif line.startswith("mo[mx++]="):
            return FileType.MONTH
        elif line.startswith("ye[yx++]="):
            return FileType.YEAR
        else:
            return None


class InverterList:
    """
    List of all inverters found in the config
    """
    _inverters = []

    def __init__(self, inverter_config):
        if len(inverter_config) == 0:
            raise Exception("No inverter in config found")

        for inverter in inverter_config:
            self._inverters.append(Inverter(inverter))

    def get_inverter(self, key):
        if key < 0 or key >= self.get_number_of_inverters():
            return None
        return self._inverters[key]

    def get_number_of_inverters(self):
        return len(self._inverters)

    def get_inverter_datapoints_to_influx(self):
        datapoints = []

        for inverter in self._inverters:
            datapoints += inverter.get_datapoints_to_influx()

        return datapoints


class Inverter:
    """
    Inverter Object
    """
    def __init__(self, inverter_config):
        self._datapoints_min = []
        self._datapoints_day = []

        self.name = inverter_config[4]
        self.type = inverter_config[0]
        self.power = inverter_config[2]

        self.sum_pdc = 0
        self.efficiency = 0

    def add_datapoint(self, datapoint):
        if datapoint.type == FileType.MIN:
            self._datapoints_min.append(datapoint)
        elif datapoint.type == FileType.DAY:
            self._datapoints_day.append(datapoint)

    def get_datapoints_to_influx(self):
        self._add_values_to_datapoint()
        influx_datapoints = []

        for datapoint in self._datapoints_min:
            influx_datapoints.append(datapoint.get_datapoint_to_influx(self.name))

        for datapoint in self._datapoints_day:
            influx_datapoints.append(datapoint.get_datapoint_to_influx(self.name))

        return influx_datapoints

    def _add_values_to_datapoint(self):
        for datapoint_day in self._datapoints_day:
            for datapoint_min in self._datapoints_min:
                if datapoint_min.date_time.date() == datapoint_day.date_time.date():
                    datapoint_day.add_pdc(datapoint_min.date_time, datapoint_min.pdc)
            datapoint_day.calculate_values()


class Datapoint:
    """
    Basic Datapoint
    """
    _timezone = pytz.timezone(settings.TIMEZONE)
    date_time = datetime.now()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.date_time == other.date_time


class MinDatapoint(Datapoint):
    """
    Minute Datapoint (min_xxxx.js)
    """
    _influx_measurment_name = "solarlog_min"
    type = FileType.MIN

    def __init__(self, min_time, pac, pdc, eday, udc, temperature):
        self.date_time = self._timezone.localize(datetime.strptime(min_time, "%d.%m.%y %H:%M:%S"))
        self.pac = int(pac)
        self.pdc = int(pdc)
        self.eday = int(eday)
        self.udc = int(udc)
        self.temperature = int(temperature)

    def get_datapoint_to_influx(self, inverter):
        return (
            {
                "measurement": self._influx_measurment_name,
                "tags": {
                    "inverter": inverter
                },
                "time": self.date_time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": self.pac,
                    "Pdc": self.pdc,
                    "Eday": self.eday,
                    "Udc": self.udc,
                    "temperature": self.temperature
                }
            }
        )


class DayDatapoint(Datapoint):
    """
    Day Datapoint (days.js, days_hist.js)
    """
    _influx_measurment_name = "solarlog_day"
    type = FileType.DAY

    def __init__(self, day_time, pac):
        self.date_time = self._timezone.localize(datetime.strptime(day_time, "%d.%m.%y"))
        self.pac = int(pac)
        self._pdc_min_data = []
        self.efficiency = 0
        self.pdc = 0

    def get_datapoint_to_influx(self, inverter):
        return (
            {
                "measurement": self._influx_measurment_name,
                "tags": {
                    "inverter": inverter
                },
                "time": self.date_time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": self.pac,
                    "Pdc": self.pdc,
                    "efficiency": self.efficiency
                }
            }
        )

    def add_pdc(self, time, pdc):
        self._pdc_min_data.append([time, pdc])

    def calculate_values(self):
        total_ws = 0.0
        total_t = 0

        for i in range(1, len(self._pdc_min_data)):
            dt = self._pdc_min_data[i][0] - self._pdc_min_data[i-1][0]
            dt = abs(dt.total_seconds())
            average = (self._pdc_min_data[i][1] + self._pdc_min_data[i - 1][1]) / 2
            total_ws += average * dt
            total_t += dt

        self.pdc = int(total_ws/3600)
        if self.pdc != 0 and self.pac != 0:
            self.efficiency = round((self.pac/self.pdc), 3)

