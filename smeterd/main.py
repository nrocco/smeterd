import logging
from subprocess import check_output
from os.path import isfile

from smeterd import VERSION
from smeterd import DESC
from smeterd import utils



log = logging.getLogger(__name__)


DEFAULT_CONFIG='/etc/defaults/smeterd.conf'
DEFAULT_DB='smeter.sqlite'
DEFAULT_PORT=8000
DEFAULT_SOCKET='0.0.0.0:%s' % DEFAULT_PORT
DEFAULT_SERIAL='/dev/ttyUSB0'



def read_meter(args, parser):
    '''
    Read a single packet from the smart meter.
    Packets can either be printed to stdout or stored
    in a sqlite database.
    '''
    from smeterd import meter
    packet = meter.read_one_packet(args.serial_port)

    if args.database:
        from smeterd import storage
        db = utils.get_absolute_path(args.database)
        if not isfile(db):
            parser.error('No database found at path %s' % db)
        log.debug('Storing data in database %s', db)
        storage.store_single_packet(db, packet)

    else:
        if args.raw:
            print str(packet)

        else:
            print 'Date:      ', packet.date
            print 'kWh 1:     ', packet.kwh1
            print 'kWh 2:     ', packet.kwh2
            print 'Gas:       ', packet.gas


def report(args, parser):
    from smeterd.storage import SQL_DAILY_RESULTS

    db = utils.get_absolute_path(args.database)

    if not isfile(db):
        parser.error('No database found at path %s' % db)

    log.debug('Working with database %s', db)
    print check_output(['sqlite3', '-header', '-column',
                        db, SQL_DAILY_RESULTS]),


def webserver(args, parser):
    from smeterd import webserver
    db = utils.get_absolute_path(args.database)

    if not isfile(db):
        parser.error('No database found at path %s' % db)

    parts = args.bind.split(':')
    host = parts[0]
    port = parts[1] if len(parts) > 1 else DEFAULT_PORT
    webserver.start_webserver(host, port, db, auto_reload=args.auto_reload)


def rrd(args, parser):
    from smeterd import rrd

    rrdfile = utils.get_absolute_path(args.rrdfile)
    db = utils.get_absolute_path(args.database)

    if 'create' == args.action:
        rrd.create_rrd_database(rrdfile)
        log.info('RRD Database created: %s', rrdfile)

    elif 'import' == args.action:
        if not isfile(rrdfile):
            parser.error('No rrd database found at %s' % rrdfile)
        if not isfile(db):
            parser.error('No database found at path %s' % db)

        log.info('Import sqlite data from %s into rrd', args.database)
        rrd.import_data_into_rrd(args.database, rrdfile)

    elif 'graph' == args.action:
        rrd.graph(rrdfile)

    else:
        log.error('Unsupported action %s', args.action)


def add_db_arg(parser):
    parser.add_argument('-d', '--database',
                        default=DEFAULT_DB, metavar=DEFAULT_DB,
                        help='sqlite database containig smeter data. '
                             'defaults to %s' % DEFAULT_DB)


def parse_and_run():
    from pycli_tools import get_argparser
    # create the top-level parser
    parser = get_argparser(prog='smeterd', version=VERSION,
                           default_config=DEFAULT_CONFIG, description=DESC)
    subparsers = parser.add_subparsers()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s')

    # create the parser for the "read-meter" command
    parser_a = subparsers.add_parser('read-meter', help='Read a single P1 packet')
    parser_a.add_argument('-p', '--serial-port', default=DEFAULT_SERIAL,
                          metavar='/dev/ttyXXXX',
                          help='serial port to read packets from. Defaults to %s' % DEFAULT_SERIAL)
    parser_a.add_argument('-r', '--raw', action='store_true',
                          help='display packet in raw form')
    add_db_arg(parser_a)
    parser_a.set_defaults(func=read_meter)


    # create the parser for the "webserver" command
    parser_b = subparsers.add_parser('webserver', help='Start a webserver')
    parser_b.add_argument('-b', '--bind', metavar='address:port',
                          default=DEFAULT_SOCKET,
                          help='Inet socket to bind to. Defaults to %s' % DEFAULT_SOCKET)
    add_db_arg(parser_b)
    parser_b.add_argument('-r', '--auto-reload',
                          action='store_true', help='auto respawn server')
    parser_b.set_defaults(func=webserver)


    # create the parser for the "report" command
    parser_c = subparsers.add_parser('report', help='Generate reports')
    add_db_arg(parser_c)
    parser_c.set_defaults(func=report)

    # create the parser for the "rrd" command
    parser_d = subparsers.add_parser('rrd', help='Generate rrd graphs')
    parser_d.add_argument('action', choices=['create','import', 'graph'])
    parser_d.add_argument('rrdfile', help='path to the rrd file')
    add_db_arg(parser_d)
    parser_d.set_defaults(func=rrd)

    # parse command line arguments
    args = parser.parse_args()

    # call the subcommand handler function
    args.func(args, parser=parser)
