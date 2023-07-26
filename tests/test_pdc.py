from datetime import datetime
from unittest import TestCase
from solarlog_exporter.parser import ConfigParser, DataParser
from tests.test_parser import TEST_DIR


class TestDataParser(TestCase):
    def setUp(self):
        self._assets = TEST_DIR + "/pdc_test/"

        config_parser = ConfigParser()
        config_parser.parse_file(self._assets + "base_vars.js")
        self._inverter_list = config_parser.get_inverters()
        self._last_record_time = datetime.strptime("01.03.2021", "%d.%m.%Y")

    def test_parse_file_for_pdc(self):
        data_parser = DataParser(self._inverter_list, self._last_record_time)
        data_parser.parse_file(self._assets + "days_hist.js")
        data_parser.parse_file(self._assets + "min230721.js")

        inv_list = self._inverter_list.get_inverter_datapoints_to_influx()
        day_data = list(filter(lambda o: o['measurement'] == 'solarlog_day', inv_list))

        self.assertEqual(34168.0, get_pdc_data_of_wr(day_data, 'WR 01'))
        self.assertEqual(32964.0, get_pdc_data_of_wr(day_data, 'WR 02'))
        self.assertEqual(35096.0, get_pdc_data_of_wr(day_data, 'WR 03'))
        self.assertEqual(37215.0, get_pdc_data_of_wr(day_data, 'WR 04'))
        self.assertEqual(22922.0, get_pdc_data_of_wr(day_data, 'WR 05'))
        self.assertEqual(37465.0, get_pdc_data_of_wr(day_data, 'WR 06'))
        self.assertEqual(36358.0, get_pdc_data_of_wr(day_data, 'WR 08'))
        self.assertEqual(23914.0, get_pdc_data_of_wr(day_data, 'WR 09'))
        self.assertEqual(23905.0, get_pdc_data_of_wr(day_data, 'WR 10'))
        self.assertEqual(23864.0, get_pdc_data_of_wr(day_data, 'WR 11'))

def get_pdc_data_of_wr(day_data, wr):
    return list(filter(lambda o: o['tags']['inverter'] == wr, day_data))[0]['fields']['Pdc']
