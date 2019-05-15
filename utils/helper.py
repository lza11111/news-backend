from datetime import datetime, timedelta

import pytz

def int_to_utc(it):
    return datetime(1900, 1, 1, tzinfo=pytz.UTC) + timedelta(seconds=it)