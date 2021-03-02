import os
import re
from datetime import datetime, timedelta

import pytz

from solarlog_exporter import settings
from solarlog_exporter.utils import MinDatapoint


def is_import_file(filename, last_record_time):
    since_filename = last_record_time.strftime("min%y%m%d.js")
    today_filename = datetime.now().strftime("min%y%m%d.js")
    prog = re.compile(r'^(min|days)\d{6}\.js$')

    if prog.match(filename) and filename >= since_filename \
            and filename != today_filename:
        return True

    return False


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
