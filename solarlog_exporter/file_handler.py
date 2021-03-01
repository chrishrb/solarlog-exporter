import os
import re
from datetime import datetime, timedelta

import pysftp
import pytz

from solarlog_exporter import settings
from solarlog_exporter.utils import MinDatapoint


class SFTPConnection:
    _files = ["days.js", "base_vars.js", "min_day.js"]

    def __init__(self, host, username, password):
        self._sftp = pysftp.Connection(host=host, username=username, password=password)

    def _list_solarlog_files_since(self, influx_client, last_record_time):
        last_record_time = get_last_record_time_influxdb(influx_client)

        since_filename = last_record_time.strftime("min%y%m%d.js")
        today_filename = datetime.now().strftime("min%y%m%d.js")
        prog = re.compile(r'^min\d{6}\.js$')

        for filename in self._sftp.listdir(settings.SOLAR_LOG_DIR):
            if prog.match(filename) and filename >= since_filename \
                    and filename != today_filename:
                self._files.append(filename)
            elif filename == "days_hist.js" and datetime.now().date() != last_record_time.date():
                self._files.append("days_hist.js")

    def get_solarlog_files(self, influx_client, last_record_time):
        self._list_solarlog_files_since(influx_client, last_record_time)
        clear_tmp_dir()

        for file in self._files:
            self._sftp.get(settings.SOLAR_LOG_DIR + "/" + file, settings.TMP_DIR + "/" + file)

    def __del__(self):
        self._sftp.close()


def clear_tmp_dir():
    for file in os.listdir(path=settings.TMP_DIR):
        if not file.endswith(".js"):
            continue
        os.remove(os.path.join(settings.TMP_DIR, file))


def get_last_record_time_influxdb(influx_client):
    query = "SELECT * FROM {} WHERE SYSTEM = '{}' ORDER BY time DESC LIMIT 1;" \
        .format(MinDatapoint.influx_measurment_name, settings.SOLAR_LOG_SYSTEM)

    result_last_point_query = list(influx_client.query(query))

    if result_last_point_query:
        time = result_last_point_query[0][0]['time']
        return datetime.fromisoformat(time[:-1]).astimezone(pytz.utc)
    else:
        # no last record found
        return datetime.now(pytz.utc) - timedelta(days=1 * 365)


def chunks(input_list, n):
    n = max(1, n)
    return (input_list[i:i + n] for i in range(0, len(input_list), n))
