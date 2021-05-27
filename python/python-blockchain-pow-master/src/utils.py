from datetime import datetime
from dateutil.tz import *


def get_local_timestamp():
    # This contains the local timezone
    local = tzlocal()
    now = datetime.now()
    now = now.replace(tzinfo=local)
    timestamp = datetime.timestamp(now) * 1000
    return timestamp


def get_utc_timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now) * 1000
    return timestamp
