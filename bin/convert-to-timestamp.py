#!/usr/bin/env python

import sys
import time
import datetime

dstring = sys.argv[1]

dformat = '%Y-%m-%d %H:%M:%S.%f'

date = datetime.datetime.strptime(dstring, dformat)
timestamp = time.mktime(date.timetuple())

print int(timestamp)
