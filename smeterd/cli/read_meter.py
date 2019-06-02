import logging
from datetime import datetime

import serial
from serial.serialutil import SerialException
from pycli_tools.commands import Command, arg

from smeterd import __default_serial__
from smeterd.meter import SmartMeter

log = logging.getLogger(__name__)


class ReadMeterCommand(Command):
    '''read a single P1 packet to stdout

    Read a single packet from the smart meter.
    Packets will be printed to stdout.

    All the options starting with --serial-* are passed directly to the
    underlying serial object. For more information on the possible values and
    their behavior please refer to the documentation here
    http://pyserial.readthedocs.io/en/latest/pyserial_api.html
    '''

    show_output_choices = ['time', 'kwh_eid', 'gas_eid', 'consumed', 'tariff', 'gas_measured_at', 'produced', 'current']

    args = [
        # options controlling input
        arg('--serial-port',     help='device name to read packets from (defaults to %s)' % __default_serial__,
                                 metavar=__default_serial__, default=__default_serial__),
        arg('--baudrate',        help='baud rate such as 9600 or 115200 etc. This option is deprecated in favor of --serial-baudrate and will be removed in future versions.',
                                 type=int, dest='serial_baudrate', default=9600, metavar=9600),
        arg('--serial-baudrate', help='baud rate such as 9600 or 115200 etc (defaults to 9600).',
                                 type=int, default=9600, metavar=9600),
        arg('--serial-xonxoff',  help='enable software flow control. By default software flow control is disabled.',
                                 action='store_true'),
        arg('--serial-bytesize', help='number of data bits (defaults to 7).',
                                 default=serial.SEVENBITS, type=int, choices=[5, 6, 7, 8]),
        arg('--serial-parity',   help='enable parity checking (defaults to E)',
                                 default=serial.PARITY_EVEN, choices=['N', 'E', 'O', 'M', 'S']),
        arg('--serial-stopbits', help='number of stop bits (defaults to 1).',
                                 default=serial.STOPBITS_ONE, type=float, choices=[1, 1.5, 2]),
        arg('--serial-timeout',  help='set a read timeout value in seconds (defaults to 10).',
                                 default=10, type=int, metavar=10),

        # options controlling output
        arg('--show-output',     help='choose output to display. (one of: ' + ", ".join(show_output_choices) + ')',
                                 default=('time', 'consumed', 'tariff', 'gas_measured_at'), type=str, nargs='+', metavar='param',
                                 choices=show_output_choices),
        arg('--tsv', help='display packet in tab separated value form',
                     action='store_true'),
        arg('--raw', help='display packet in raw form',
                     action='store_true'),
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

        # Construct output depending on user request
        data = []
        if ('time' in args.show_output):
            data.append(('Time', datetime.now()))
        if ('kwh_eid' in args.show_output):
            data.append(('Electricity serial', packet['kwh']['eid']))
        if ('gas_eid' in args.show_output):
            data.append(('Gas serial', packet['gas']['eid']))
        if ('consumed' in args.show_output):
            data.extend([
                ('Total electricity consumed (high, Wh)', int(packet['kwh']['high']['consumed']*1000)),
                ('Total electricity consumed (low, Wh)', int(packet['kwh']['low']['consumed']*1000)),
                ('Total gas consumed (m^3)', int(packet['gas']['total']*1000))])
        if ('produced' in args.show_output):
            data.extend([
                ('Total electricity produced (high, Wh)', int(packet['kwh']['high']['produced']*1000)),
                ('Total electricity produced (low, Wh)', int(packet['kwh']['low']['produced']*1000))])
        if ('current' in args.show_output):
            data.extend([
                ('Current electricity consumption (W)', int(packet['kwh']['current_consumed']*1000)),
                ('Current electricity production (W)', int(packet['kwh']['current_produced']*1000))])
        if ('tariff' in args.show_output):
            data.append(('Current electricity tariff', packet['kwh']['tariff']))
        if ('gas_measured_at' in args.show_output):
            data.append(('Gas measured at', packet['gas']['measured_at']))

        if args.tsv:
            print('\t'.join(map(str, [d for k,d in data])))
        else:
            print('\n'.join(['%-40s %s' % (k,d) for k,d in data]))

        return 0
