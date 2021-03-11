from datetime import datetime
from unittest import TestCase

from solarlog_exporter import settings
from solarlog_exporter.parser import ConfigParser, DataParser
from solarlog_exporter.utils import InverterList


class TestConfigParser(TestCase):
    def setUp(self):
        self._assets = "./assets/"
        self._config_parser = ConfigParser(self._assets + "base_vars.js")

    def test_get_power(self):
        self.assertEqual(self._config_parser.get_power(), "100 kwp")

    def test_get_title(self):
        self.assertEqual(self._config_parser.get_title(), settings.SOLAR_LOG_SYSTEM)

    def test_get_group(self):
        # todo: add groups
        self.assertIsNone(self._config_parser.get_group(0))

    def test_get_operator(self):
        self.assertEqual(self._config_parser.get_operator(), "example-operator")

    def test_get_place(self):
        self.assertEqual(self._config_parser.get_place(), "example-place")

    def test_get_installation_date(self):
        self.assertEqual(self._config_parser.get_installation_date(), "01.01.2010")

    def test_get_orientation(self):
        self.assertEqual(self._config_parser.get_orientation(), "35 Grad;  18 Grad von süd nach west")

    def test_get_banner_1(self):
        self.assertEqual(self._config_parser.get_banner_1(), "banner row 1")

    def test_get_banner_2(self):
        self.assertEqual(self._config_parser.get_banner_2(), "banner row 2")

    def test_get_banner_3(self):
        self.assertEqual(self._config_parser.get_banner_3(), "banner row 3")

    def test_get_inverter_config(self):
        inverter_config = [[['PAC7', '100001', 7800.0, 1.0, 'WR 1', 1.0, None, None, 0.0, None,
                             14.0, 0.0, 1.0, 1000.0, None], None],
                           [['PAC7', '100002', 7800.0, 1.0, 'WR 2', 1.0, None, None, 0.0, None,
                             14.0, 0.0, 1.0, 1000.0, None], None]]

        self.assertEqual(self._config_parser.get_inverter_config(), inverter_config)

    def test_get_inverters(self):
        self.assertIsInstance(self._config_parser.get_inverters(), InverterList)


class TestDataParser(TestCase):
    def setUp(self):
        self._assets = "./assets/"

        config_parser = ConfigParser(self._assets + "base_vars.js")
        self._inverter_list = config_parser.get_inverters()
        self._last_record_time = datetime.strptime("01.03.2021", "%d.%m.%Y")

    def test_parse_file_in_timezone(self):
        data_parser = DataParser(self._inverter_list, self._last_record_time)
        data_parser.parse_file(self._assets + "minTEST.js")

        self.assertEqual(self._inverter_list.get_inverter(0).datapoints_min.get('01.03.21 23:55:00').pac, 10)
        self.assertEqual(self._inverter_list.get_inverter(0).datapoints_min.get('01.03.21 23:55:00').pdc, 20)
        self.assertEqual(self._inverter_list.get_inverter(0).datapoints_min.get('01.03.21 23:55:00').eday, 50214)
        self.assertEqual(self._inverter_list.get_inverter(0).datapoints_min.get('01.03.21 23:55:00').udc, 30)
        self.assertEqual(self._inverter_list.get_inverter(0).datapoints_min.get('01.03.21 23:55:00').temperature, 21)

        self.assertEqual(self._inverter_list.get_inverter(1).datapoints_min.get('01.03.21 23:55:00').pac, 13)
        self.assertEqual(self._inverter_list.get_inverter(1).datapoints_min.get('01.03.21 23:55:00').pdc, 21)
        self.assertEqual(self._inverter_list.get_inverter(1).datapoints_min.get('01.03.21 23:55:00').eday, 50858)
        self.assertEqual(self._inverter_list.get_inverter(1).datapoints_min.get('01.03.21 23:55:00').udc, 32)
        self.assertEqual(self._inverter_list.get_inverter(1).datapoints_min.get('01.03.21 23:55:00').temperature, 22)

    def test_parse_file_not_in_timezone(self):
        data_parser = DataParser(self._inverter_list, self._last_record_time)
        data_parser.parse_file(self._assets + "minTEST.js")

        self.assertIsNone(self._inverter_list.get_inverter(0).datapoints_min.get('28.02.21 23:55:00'))
