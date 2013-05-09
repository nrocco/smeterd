import time
import datetime
from os import path



def convert_to_timestamp(dstring, dformat='%Y-%m-%d %H:%M:%S.%f'):
    date = datetime.datetime.strptime(dstring, dformat)
    timestamp = time.mktime(date.timetuple())

    return int(timestamp)


def get_absolute_path(filename):
    if path.isabs(filename):
        return filename
    else:
        return path.abspath(filename)
