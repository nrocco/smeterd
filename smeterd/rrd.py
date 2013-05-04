import rrdtool
import logging

from smeterd import storage
from smeterd import utils



log = logging.getLogger(__name__)


def create_rrd_database(file):
    file = utils.get_absolute_path(file)
    log.info('Creating RRD file in %s', file)

    rrdtool.create(file,
                   '--start', '1366750607',
                   '--step', '300',
                   'DS:kwh1:COUNTER:600:0:U',
                   'DS:kwh2:COUNTER:600:0:U',
                   'DS:gas:COUNTER:600:0:U',
                   'RRA:AVERAGE:0.5:1:8640',
                   'RRA:AVERAGE:0.5:12:8760',
                   'RRA:AVERAGE:0.5:228:3650')


def import_data_into_rrd(database, rrd_file):
    database = utils.get_absolute_path(database)
    rrd_File = utils.get_absolute_path(rrd_file)

    log.info('Importing data from %s to %s',
             database, rrd_file)

    data = storage.get_all_data(database)

    for row in data:
        ts = utils.convert_to_timestamp(row['date'])
        rrdtool.update(rrd_file, '%s:%s:%s:%s' % 
                       (ts, row['kwh1'], row['kwh2'], row['gas']))

