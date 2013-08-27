import logging

from datetime import datetime

from serial.serialutil import SerialException

from pycli_tools.parsers import get_argparser
from pycli_tools.commands import Command, arg

from smeterd import __version__
from smeterd import __description__

from smeterd.meter import SmartMeter



log = logging.getLogger(__name__)


DEFAULT_SERIAL='/dev/ttyUSB0'


class ReadMeterCommand(Command):
    '''Read a single P1 packet

    Read a single packet from the smart meter.
    Packets can either be printed to stdout or stored
    in a sqlite database.
    '''

    args = [
        arg('--serial-port', default=DEFAULT_SERIAL, metavar=DEFAULT_SERIAL,
            help='serial port to read packets from (defaults to %s)' % DEFAULT_SERIAL),
        arg('--tsv', action='store_true',
            help='display packet in tab seperated value form'),
        arg('--raw', action='store_true',
            help='display packet in raw form'),
    ]

    def run(self, args, parser):
        meter = SmartMeter(args.serial_port)

        try:
            packet = meter.read_one_packet()
        except SerialException as e:
            parser.error(e)
        finally:
            meter.disconnect()

        if args.raw:
            print(str(packet))
            return 0

        data = [
            ('Time', datetime.now()),
            ('Total kWh High consumed', int(packet['kwh']['high']['consumed']*1000)),
            ('Total kWh Low consumed', int(packet['kwh']['low']['consumed']*1000)),
            ('Total gas consumed', int(packet['gas']['total']*1000)),
            ('Current kWh tariff', packet['kwh']['tariff'])
        ]

        if args.tsv:
            print('\t'.join(map(str, [d for k,d in data])))
        else:
            print('\n'.join(['%-25s %s' % (k,d) for k,d in data]))




def parse_and_run():
    parser = get_argparser(
        prog='smeterd',
       version=__version__,
       default_config='~/.smeterdrc',
       logging_format='[%(asctime)-15s] %(levelname)s %(message)s',
       description=__description__
    )

    parser.add_commands([
        ReadMeterCommand(),
    ])

    args = parser.parse_args()
    args.func(args, parser=parser)
