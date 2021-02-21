from datetime import datetime

import pytz as pytz

from solarlog_exporter import settings


class Inverter:
    def __init__(self, inverter_config):
        self._datapoints = []
        self.name = inverter_config[4]
        self.type = inverter_config[0]
        self.power = inverter_config[2]

    def add_datapoint(self, datapoint):
        self._datapoints.append(datapoint)

    def get_datapoints_to_influx(self):
        influx_datapoints = []

        for datapoint in self._datapoints:
            influx_datapoints.append(datapoint.get_datapoint_to_influx(self.name))

        return influx_datapoints


class Datapoint:
    _timezone = pytz.timezone(settings.TIMEZONE)

    pass


class MinDatapoint(Datapoint):
    _influx_measurment_name = "solarlog_min"

    def __init__(self, min_time, pac, pdc, eday, udc, temperature):
        self._time = self._timezone.localize(datetime.strptime(min_time, "%d.%m.%y %H:%M:%S"))
        self._pac = int(pac)
        self._pdc = int(pdc)
        self._eday = int(eday)
        self._udc = int(udc)
        self._temperature = int(temperature)

    def get_datapoint_to_influx(self, inverter):
        return (
            {
                "measurement": self._influx_measurment_name,
                "tags": {
                    "inverter": inverter
                },
                "time": self._time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": self._pac,
                    "Pdc": self._pdc,
                    "Eday": self._eday,
                    "Udc": self._udc,
                    "temperature": self._temperature
                }
            }
        )


class DayDatapoint(Datapoint):
    _influx_measurment_name = "solarlog_day"

    def __init__(self, day_time, pac):
        self._time = self._timezone.localize(datetime.strptime(day_time, "%d.%m.%y"))
        self._pac = int(pac)

        # todo: Calculate these two
        self._pdc = 0
        self._efficiency = 0

    def get_datapoint_to_influx(self, inverter):
        return (
            {
                "measurement": self._influx_measurment_name,
                "tags": {
                    "inverter": inverter
                },
                "time": self._time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": self._pac,
                    "Pdc": self._pdc,
                    "efficiency": self._efficiency
                }
            }
        )


class MonthLine(Datapoint):
    _influx_measurment_name = "solarlog_month"

    def __init__(self, month_date, pac):
        self._time = self._timezone.localize(datetime.strptime(month_date, "%d.%m.%y %H:%M:%S"))
        self._pac = pac


class YearLine:
    _influx_measurment_name = "solarlog_year"

    pass
