import sys
import logging
from argparse import ArgumentParser



log = logging.getLogger(__name__)


VERSION = 'v1.5'
DESC='''Read smart meter P1 packets'''

DEFAULT_DB='smeter.sqlite'
DEFAULT_PORT=8000
DEFAULT_SOCKET='0.0.0.0:%s' % DEFAULT_PORT
DEFAULT_SERIAL='/dev/ttyUSB0'



def read_meter(args):
    '''
    Read a single packet from the smart meter.
    Packets can either be printed to stdout or stored
    in a sqlite database.
    '''
    from smeterd import meter
    packet = meter.read_one_packet(args.serial_port)

    if args.database:
        from smeterd import storage
        db = storage._get_db_abspath(args.database)
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


def report(args):
    from smeterd import storage
    from smeterd import utils
    db = utils.get_absolute_path(args.database)
    log.debug('Working with database %s', db)
    data = storage.generate_report(db)
    print utils.dictionary_list_to_plaintext_table(data)


def webserver(args):
    from smeterd import webserver
    parts = args.bind.split(':')
    host = parts[0]
    port = parts[1] if len(parts) > 1 else DEFAULT_PORT
    webserver.start_webserver(host, port, DEFAULT_DB,
                              auto_reload=args.auto_reload)







if '__main__' == __name__:
    # create the top-level parser
    parser = ArgumentParser(prog='smeterd', description=DESC)
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='output more verbose')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='surpress all output')
    subparsers = parser.add_subparsers()


    # create the parser for the "read-meter" command
    parser_a = subparsers.add_parser('read-meter', help='Read a single P1 packet')
    parser_a.add_argument('-p', '--serial-port', default=DEFAULT_SERIAL,
                          metavar='/dev/ttyXXXX',
                          help='serial port to read packets from. Defaults to %s' % DEFAULT_SERIAL)
    parser_a.add_argument('-r', '--raw', action='store_true',
                          help='display packet in raw form')
    parser_a.add_argument('-d', '--database', metavar=DEFAULT_DB,
                          help='path to a sqlite database.')
    parser_a.set_defaults(func=read_meter)


    # create the parser for the "webserver" command
    parser_b = subparsers.add_parser('webserver', help='Start a webserver')
    parser_b.add_argument('-b', '--bind', metavar='address:port',
                          default=DEFAULT_SOCKET,
                          help='Inet socket to bind to. Defaults to %s' % DEFAULT_SOCKET)
    parser_b.add_argument('-r', '--auto-reload',
                          action='store_true', help='auto respawn server')
    parser_b.set_defaults(func=webserver)


    # create the parser for the "report" command
    parser_c = subparsers.add_parser('report', help='Generate reports')
    parser_c.add_argument('-d', '--database',
                          default=DEFAULT_DB, metavar=DEFAULT_DB,
                          help='sqlite database containig smeter data. defaults to %s' % DEFAULT_DB)
    parser_c.set_defaults(func=report)


    # parse command line arguments
    args = parser.parse_args()

    # set log level
    loglevel = 100 if args.quiet else max(30 - args.verbose * 10, 10)
    logging.basicConfig(level=loglevel, format='%(asctime)-15s %(levelname)s %(message)s')

    # call the subcommand
    args.func(args)
