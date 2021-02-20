from datetime import datetime

import pytz as pytz

import settings


class Inverter:
    _datapoints = []

    def __init__(self, inverter_config):
        self.name = inverter_config[3]
        self.type = inverter_config[0]
        self.power = inverter_config[2]

    def add_datapoint(self, datapoint):
        self._datapoints.append(datapoint)

    def get_influx_datapoints(self):
        influx_points = []

        for datapoint in self._datapoints:
            influx_points.append(
                {
                    "measurement": datapoint.influx_measurment_name,
                    "tags": {
                        "inverter": self.name
                    },
                    "time": datapoint.time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                    "fields": {
                        "Pac": datapoint.pac,
                        "Pdc": datapoint.pdc,
                        "Eday": datapoint.eday,
                        "Udc": datapoint.udc
                    }
                }
            )

        return influx_points


class Datapoint:
    pass


class DayDatapoint(Datapoint):
    influx_measurment_name = "solarlog_day"

    def __init__(self, day_time, pac, pdc, eday, udc):
        timezone = pytz.timezone(settings.TIMEZONE)
        self.time = timezone.localize(datetime.strptime(day_time, "%d.%m.%y %H:%M:%S"))
        self.pac = int(pac)
        self.pdc = int(pdc)
        self.eday = int(eday)
        self.udc = int(udc)


class MonthLine(Datapoint):
    influx_measurment_name = "solarlog_month"

    def __init__(self, month_date, pac):
        self._date = datetime.strptime(month_date, "%d.%m.%y")
        self._pac = pac


class YearLine:
    influx_measurment_name = "solarlog_year"
    pass
