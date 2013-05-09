import rrdtool
import logging
import os

from smeterd import storage
from smeterd import utils



log = logging.getLogger(__name__)


def create_rrd_database(file, force=False):
    file = utils.get_absolute_path(file)

    if os.path.isfile(file) and not force:
        if force:
            log.debug('%s already exists. '
                      'overwriting existing file', file)
        else:
            log.debug('%s already exists. '
                      'not creating rrd file', file)
            return

    log.info('Creating RRD file in %s', file)

    rrdtool.create(file,
                   '--start', '1366750607',
                   '--step', '300',
                   'DS:kwh1:COUNTER:600:0:U',
                   'DS:kwh2:COUNTER:600:0:U',
                   'DS:gas:COUNTER:600:0:U',
                   'RRA:MAX:0.5:1:8640',
                   'RRA:MAX:0.5:12:8760',
                   'RRA:MAX:0.5:228:3650')


def import_data_into_rrd(database, rrd_file):
    database = utils.get_absolute_path(database)
    rrd_file = utils.get_absolute_path(rrd_file)

    log.info('Importing data from %s to %s',
             database, rrd_file)

    data = storage.get_all_data(database)

    for row in data:
        ts = utils.convert_to_timestamp(row['date'])
        rrdtool.update(rrd_file, '%s:%s:%s:%s' %
                       (ts, row['kwh1'], row['kwh2'], row['gas']))

    log.info('A total of %d rows imported', len(data))


def graph(rrd_file):
    rrdtool.graph('kwh.png',
                  '--step', '3600',
                  '--start', 'end-14d', '--end', 'now',
                  '--width', '800', '--height', '300',
                  '--title', 'Energy consumption in kWh per hour',
                  '--vertical-label', 'kWh per hour',
                  '--lower-limit', '0',
                  '--no-legend',
                  'DEF:kwh1=%s:kwh1:MAX' % rrd_file,
                  'DEF:kwh2=%s:kwh2:MAX' % rrd_file,
                  # 'CDEF:kwh1k=kwh1,1000,/',
                  # 'CDEF:kwh2k=kwh2,1000,/',
                  'AREA:kwh1#0000FF:"Average kwh1"',
                  'AREA:kwh2#00FF00:"Average kwh2"')




#rrdtool graph gas.png \
#  --step $STEP $PERIOD $DIMENSIONS \
#  --vertical-label 'Cubic meters' \
#  --lower-limit 0 \
#  --no-legend \
#  DEF:gas=$RRD_FILE:gas:AVERAGE \
#  AREA:gas#FF0000:"Average"
