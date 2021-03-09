from datetime import datetime
from unittest import TestCase
from solarlog_exporter.file_handler import is_import_file


class TestFileHandler(TestCase):
    def setUp(self):
        self._last_record_time = datetime.strptime("01.03.2021", "%d.%m.%Y")

    def test_is_import_file(self):
        self.assertTrue(is_import_file("days.js", self._last_record_time))
        self.assertTrue(is_import_file("days_hist.js", self._last_record_time))
        self.assertTrue(is_import_file("min_day.js", self._last_record_time))

        self.assertFalse(is_import_file("min_cur.js", self._last_record_time))
        self.assertFalse(is_import_file("min_210301.js", self._last_record_time))
        self.assertFalse(is_import_file("min_210228.js", self._last_record_time))
        self.assertFalse(is_import_file("min_200101.js", self._last_record_time))
        self.assertFalse(is_import_file("months.js", self._last_record_time))

    # todo: add test
    def test_get_last_record_time_influxdb(self):
        pass
