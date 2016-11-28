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
    Packets can either be printed to stdout or stored
    in a sqlite database.
    '''

    args = [
        arg('--serial-port', default=__default_serial__, metavar=__default_serial__, help='serial port to read packets from (defaults to %s)' % __default_serial__),
        arg('--baudrate', default=9600, help='baudrate for the serial connection'),
        arg('--xonxoff', action='store_true', help='wether to enable software flow control'),
        arg('--bytesize', type=int, default=serial.SEVENBITS, help='byte size for the serial connection, choose from 5, 6, 7, 8'),
        arg('--parity', default=serial.PARITY_EVEN, help='parity for the serial connection, choose from N, E, O, M, S'),
        arg('--stopbits', type=float, default=serial.STOPBITS_ONE, help='stop bits for the serial connection, choose from 1, 1.5, 2'),
        arg('--tsv', action='store_true', help='display packet in tab separated value form'),
        arg('--raw', action='store_true', help='display packet in raw form'),
    ]

    def run(self, args, parser):
        meter = SmartMeter(args.serial_port,
                           baudrate=args.baudrate,
                           bytesize=args.bytesize,
                           parity=args.parity,
                           stopbits=args.stopbits,
                           xonxoff=args.xonxoff)

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
