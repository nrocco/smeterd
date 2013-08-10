import logging

from datetime import datetime

from serial.serialutil import SerialException

from pycli_tools.parsers import get_argparser
from pycli_tools.actions import ExistingFileAction

from smeterd import __version__
from smeterd import __description__
from smeterd.meter import read_one_packet
from smeterd.storage import store_single_packet



log = logging.getLogger(__name__)


DEFAULT_SERIAL='/dev/ttyUSB0'



def read_meter(args, parser):
    '''
    Read a single packet from the smart meter.
    Packets can either be printed to stdout or stored
    in a sqlite database.
    '''
    try:
        packet = read_one_packet(args.serial_port)
    except SerialException as e:
        parser.error(e)

    if args.store and args.database:
        log.info('Storing data in database %s', args.database)
        store_single_packet(args.database, packet)

    if args.raw:
        print str(packet)
    else:
        print('Date:      %s' % datetime.now())
        print('kWh1:      %s kwh' % packet['kwh1_in'])
        print('kWh2:      %s kwh' % packet['kwh2_in'])
        print('Gas:       %s m3' % packet['gas'])



def parse_and_run():
    # create the top-level parser
    parser = get_argparser(prog='smeterd',
                           version=__version__,
                           default_config='~/.smeterdrc',
                           logging_format='[%(asctime)-15s] %(levelname)s %(message)s',
                           description=__description__)
    subparsers = parser.add_subparsers()

    # create the parser for the "read-meter" command
    parser_a = subparsers.add_parser('read-meter', help='Read a single P1 packet')
    parser_a.add_argument('--serial-port', default=DEFAULT_SERIAL,
                          metavar=DEFAULT_SERIAL,
                          help='serial port to read packets from (defaults to %s)' % DEFAULT_SERIAL)
    parser_a.add_argument('--store', action='store_true',
                          help='write the results to the database')
    parser_a.add_argument('--raw', action='store_true',
                          help='display packet in raw form')
    parser_a.add_argument('--database', action=ExistingFileAction,
                          help='sqlite database containig smeter data')
    parser_a.set_defaults(func=read_meter)

    # parse command line arguments
    args = parser.parse_args()

    # call the subcommand handler function
    parser.exit(args.func(args, parser=parser))
