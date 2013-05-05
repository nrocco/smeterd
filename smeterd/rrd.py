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




#STEP=3600
#PERIOD='--start end-7d --end now'
#DIMENSIONS='--width 800 --height 300'
#
#RRD_FILE="test.rrd"
#
#[ -f $RRD_FILE ] || exit 1
#
#rrdtool graph kwh.png \
#  --step $STEP $PERIOD $DIMENSIONS \
#  --title 'Energy consumption in kWh' --vertical-label 'kWh' \
#  --lower-limit 0 \
#  --no-legend \
#  DEF:kwh1=$RRD_FILE:kwh1:AVERAGE \
#  DEF:kwh2=$RRD_FILE:kwh2:AVERAGE \
#  CDEF:kwh1k=kwh1,1000,/ \
#  CDEF:kwh2k=kwh2,1000,/ \
#  AREA:kwh1k#0000FF:"Average kwh1" \
#  AREA:kwh2k#00FF00:"Average kwh2"
#
#
#rrdtool graph gas.png \
#  --step $STEP $PERIOD $DIMENSIONS \
#  --vertical-label 'Cubic meters' \
#  --lower-limit 0 \
#  --no-legend \
#  DEF:gas=$RRD_FILE:gas:AVERAGE \
#  AREA:gas#FF0000:"Average"
