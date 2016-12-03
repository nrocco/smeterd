import logging
from datetime import datetime

import serial
from serial.serialutil import SerialException
from pycli_tools.commands import Command, arg

from smeterd import __default_serial__
from smeterd.meter import SmartMeter

log = logging.getLogger(__name__)


class ReadMeterCommand(Command):
    '''Read a single P1 packet

    Read a single packet from the smart meter.
    Packets will be printed to stdout.
    '''

    args = [
        # options controlling input
        arg('--serial-port',     default=__default_serial__, metavar=__default_serial__, help='Device name to read packets from (defaults to %s)' % __default_serial__),
        arg('--serial-baudrate', default=9600, help='Baud rate such as 9600 or 115200 etc.'),
        arg('--serial-xonxoff',  action='store_true', help='Enable software flow control'),
        arg('--serial-bytesize', type=int, default=serial.SEVENBITS, help='Number of data bits. Possible values: 5, 6, 7, 8'),
        arg('--serial-parity',   default=serial.PARITY_EVEN, help='Enable parity checking. Possible values: N, E, O, M, S'),
        arg('--serial-stopbits', type=float, default=serial.STOPBITS_ONE, help='Number of stop bits. Possible values: 1, 1.5, 2'),
        arg('--serial-timeout',  type=int, default=10, help='Set a read timeout value'),

        # options controlling output
        arg('--tsv', action='store_true', help='display packet in tab separated value form'),
        arg('--raw', action='store_true', help='display packet in raw form'),
    ]

    def run(self, args, parser):
        meter = SmartMeter(
            args.serial_port,
            baudrate=args.serial_baudrate,
            bytesize=args.serial_bytesize,
            parity=args.serial_parity,
            stopbits=args.serial_stopbits,
            xonxoff=args.serial_xonxoff,
            timeout=args.serial_timeout,
        )

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

        return 0
