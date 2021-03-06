import unittest
from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import MagicMock, patch, create_autospec

import pytz

from solarlog_exporter import settings
from solarlog_exporter.utils import InverterList, FileType, Inverter, DayDatapoint, MinDatapoint, Datapoint


class FileTypeTest(unittest.TestCase):
    def test_min(self):
        # given
        line = 'm[mi++]="29.04.16 23:55:00|0;0;5"'
        # when
        file_type = FileType.get_filetype(line)
        # then
        self.assertEqual(file_type, FileType.MIN)

    def test_day(self):
        # given
        line = 'da[dx++]="29.04.16 23:55:00|0;0;5"'
        # when
        file_type = FileType.get_filetype(line)
        # then
        self.assertEqual(file_type, FileType.DAY)


class TestInverterList(TestCase):
    def setUp(self):
        self._inverter_config = [
            [["PAC7", "  10002579", 7800, 1, "WR 1", 1, None, None, 0, None, 14, 0, 1, 1000, None]]
        ]
        self._system = "system"

    def test_constructor_is_ok(self):
        inverter_list = InverterList(self._inverter_config, self._system)
        self.assertNotEqual(inverter_list.inverters, [])

    def test_no_inverter(self):
        with self.assertRaises(ValueError) as context:
            InverterList([], "system")

        self.assertEqual("No inverter in config found", str(context.exception))

    def test_no_system(self):
        with self.assertRaises(ValueError) as context:
            InverterList([0], None)

        self.assertEqual("No name of system provided", str(context.exception))

    def test_get_inverter(self):
        inverter_list = InverterList(self._inverter_config, self._system)
        self.assertIsInstance(inverter_list.get_inverter(0), Inverter)
        self.assertIsNone(inverter_list.get_inverter(1))
        self.assertIsNone(inverter_list.get_inverter(-1))

    def test_get_number_of_inverters(self):
        inverter_list = InverterList(self._inverter_config, self._system)
        self.assertEqual(inverter_list.get_number_of_inverters(), 1)


class TestInverter(TestCase):
    def setUp(self):
        self._inverter_config = [
            [["PAC7", "  10002579", 7800, 1, "WR 1", 1, None, None, 0, None, 14, 0, 1, 1000, None]]
        ]
        self._system = "testsystem"
        self._last_record_time = datetime.now() - timedelta(hours=0, minutes=10)
        self._date_today = datetime.now().date().strftime("%d.%m.%y")
        self._time_now = datetime.now().strftime("%d.%m.%y %H:%M:%S")

    def test_inverter_constructor(self):
        inverter = Inverter(self._inverter_config[0], self._system)
        self.assertEqual(inverter.name, "WR 01")
        self.assertEqual(inverter.system, "testsystem")
        self.assertEqual(inverter.type, "PAC7")
        self.assertEqual(inverter.power, 7800)
        self.assertEqual(inverter.group, None)

    def test_inverter_group(self):
        inverter_config = [
            [["PAC7", "  10002579", 7800, 1, "WR 1", 1, None, None, 0, None, 14, 0, 1, 1000, None],
             "testgroup"]
        ]
        inverter = Inverter(inverter_config[0], self._system)
        self.assertEqual(inverter.group, "testgroup")

    def test_add_min_datapoint(self):
        inverter = Inverter(self._inverter_config[0], self._system)
        datapoint = MinDatapoint(
            min_time=self._time_now,
            pac=1200,
            pdc=1100,
            eday=4000,
            udc=1500,
            temperature=60
        )

        datapoint_2 = MinDatapoint(
            min_time="12.02.20 23:55:00",
            pac=1200,
            pdc=1100,
            eday=4000,
            udc=1500,
            temperature=60
        )

        inverter.add_datapoint(datapoint, self._last_record_time)
        inverter.add_datapoint(datapoint_2, self._last_record_time)

        self.assertNotEqual(inverter.datapoints_min, {})
        self.assertEqual(len(inverter.datapoints_min), 1)

    def test_add_day_datapoint(self):
        inverter = Inverter(self._inverter_config[0], self._system)
        datapoint = DayDatapoint(self._date_today, "1200")
        datapoint_2 = DayDatapoint("12.02.20", "1200")

        inverter.add_datapoint(datapoint, self._last_record_time)
        inverter.add_datapoint(datapoint_2, self._last_record_time)

        self.assertNotEqual(inverter.datapoints_day, {})
        self.assertEqual(len(inverter.datapoints_day), 1)

    def test_get_datapoints_to_influx(self):
        inverter = Inverter(self._inverter_config[0], self._system)
        datapoint_min_1 = MinDatapoint(
            min_time=self._time_now,
            pac=1200,
            pdc=1100,
            eday=4000,
            udc=1500,
            temperature=60
        )
        datapoint_min_2 = MinDatapoint(
            min_time=(datetime.now() - timedelta(minutes=5)).strftime("%d.%m.%y %H:%M:%S"),
            pac=1200,
            pdc=1100,
            eday=4000,
            udc=1500,
            temperature=60
        )
        datapoint_day = DayDatapoint(self._date_today, "1200")

        inverter.add_datapoint(datapoint_day, self._last_record_time)
        inverter.add_datapoint(datapoint_min_1, self._last_record_time)
        inverter.add_datapoint(datapoint_min_2, self._last_record_time)

        influx_points = inverter.get_datapoints_to_influx()
        self.assertNotEqual(influx_points, {})
        self.assertNotEqual(inverter.datapoints_day[self._date_today].pac, 0.0)
        self.assertNotEqual(inverter.datapoints_day[self._date_today].pdc, 0.0)
        self.assertNotEqual(inverter.datapoints_day[self._date_today].efficiency, 0.0)


class TestMinDatapoint(TestCase):
    def test_get_datapoint_to_influx(self):
        min_time = "29.04.16 23:55:00"
        timezone = pytz.timezone(settings.TIMEZONE)
        min_time = timezone.localize(datetime.strptime(min_time, "%d.%m.%y %H:%M:%S"))

        datapoint_min = MinDatapoint(
            min_time=min_time.strftime("%d.%m.%y %H:%M:%S"),
            pac=1200,
            pdc=1100,
            eday=4000,
            udc=1500,
            temperature=60
        )

        inverter = MagicMock()
        inverter.configure_mock(name="WR 01", system="example_system", group="example_group")
        influx_point = datapoint_min.get_datapoint_to_influx(inverter)

        self.assertIsNotNone(influx_point)
        self.assertDictEqual(
            influx_point,
            {
                "measurement": "solarlog_min",
                "tags": {
                    "inverter": "WR 01",
                    "system": "example_system",
                    "group": "example_group"
                },
                "time": min_time.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": 1200,
                    "Pdc": 1100,
                    "Eday": 4000,
                    "Udc": 1500,
                    "temperature": 60
                }
            }
        )


class TestDayDatapoint(TestCase):
    def test_get_datapoint_to_influx(self):
        day_date = "02.03.21"
        timezone = pytz.timezone(settings.TIMEZONE)
        day_date_as_datetime = timezone.localize(datetime.strptime(day_date, "%d.%m.%y"))

        datapoint_day = DayDatapoint(day_date, 1200)

        inverter = MagicMock()
        inverter.configure_mock(name="WR 01", system="example_system", group="example_group")
        influx_point = datapoint_day.get_datapoint_to_influx(inverter)

        self.assertIsNotNone(influx_point)
        self.assertDictEqual(
            influx_point,
            {
                "measurement": "solarlog_day",
                "tags": {
                    "inverter": "WR 01",
                    "system": "example_system",
                    "group": "example_group"
                },
                "time": day_date_as_datetime.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z'),
                "fields": {
                    "Pac": 1200,
                    "Pdc": 0,
                    "efficiency": 0
                }
            }
        )

    # todo
    def test_add_pdc(self):
        pass

    # todo: tests are very important here
    def test_calculate_values(self):
        self.fail()
