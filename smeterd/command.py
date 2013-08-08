import logging

from pycli_tools.parsers import get_argparser

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
    packet = read_one_packet(args.serial_port)

    if args.store and args.database:
        db = get_absolute_path(args.database)
        log.info('Storing data in database %s', db)
        store_single_packet(db, packet)

    if args.raw:
        print str(packet)
    else:
        print 'Date:      ', packet.date
        print 'kWh 1:     ', packet.kwh1
        print 'kWh 2:     ', packet.kwh2
        print 'Gas:       ', packet.gas



from argparse import Action
from os.path import isfile, isabs, abspath


class ExistingFile(Action):
    def __call__(self, parser, args, values, option_string=None):
        if not isfile(values):
            parser.error('File `%s` does not exist' % values)

        path = values if isabs(values) else abspath(values)
        setattr(args, self.dest, path)



def parse_and_run():
    # create the top-level parser
    parser = get_argparser(prog='smeterd',
                           version=__version__,
                           default_config='~/.smeterdrc',
                           description=__description__)
    subparsers = parser.add_subparsers()

    logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s')

    # create the parser for the "read-meter" command
    parser_a = subparsers.add_parser('read-meter', help='Read a single P1 packet')
    parser_a.add_argument('--serial-port', default=DEFAULT_SERIAL,
                          metavar=DEFAULT_SERIAL,
                          help='serial port to read packets from (defaults to %s)' % DEFAULT_SERIAL)
    parser_a.add_argument('--store', action='store_true',
                          help='write the results to the database')
    parser_a.add_argument('--raw', action='store_true',
                          help='display packet in raw form')
    parser_a.add_argument('--database', action=ExistingFile,
                          help='sqlite database containig smeter data')
    parser_a.set_defaults(func=read_meter)

    # parse command line arguments
    args = parser.parse_args()

    # call the subcommand handler function
    parser.exit(args.func(args, parser=parser))
