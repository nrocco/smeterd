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


def dictionary_list_to_plaintext_table(data):
    if len(data) == 0:
        return ''
    result = []
    result.append('\t'.join(format(h, '8s') for h in data[0].keys()))
    result.append('')
    for row in data:
        result.append('\t'.join(format(str(e), '8s') for e in row))
    return '\n'.join(result)
