import click
import datetime
import serial
import smeterd
from smeterd.meter import SmartMeter


@click.command(context_settings=dict(auto_envvar_prefix='SMETERD', show_default=True))
@click.option('--elec-unit', help='electricity unit to use', default='Wh', type=click.Choice(['Wh', 'kWh', 'J', 'MJ']))
@click.option('--gas-unit', help='gas unit to use. Caloric units (J, MJ) based on Dutch gas @ 43.94 MJ/m^3', default='m3', type=click.Choice(['m3', 'l', 'J', 'MJ']))
@click.option('--raw', help='display packet in raw form', is_flag=True)
@click.option('--serial-baudrate', help='baud rate such as 9600 or 115200 etc', type=int, default=9600)
@click.option('--serial-bytesize', help='number of data bits', default=str(serial.SEVENBITS), type=click.Choice(['5', '6', '7', '8']))
@click.option('--serial-parity', help='enable parity checking', default=serial.PARITY_EVEN, type=click.Choice(['N', 'E', 'O', 'M', 'S']))
@click.option('--serial-port', help='device name to read packets from', default=smeterd.__default_serial__)
@click.option('--serial-stopbits', help='number of stop bits', default=str(serial.STOPBITS_ONE), type=click.Choice(['1', '1.5', '2']))
@click.option('--serial-timeout', help='set a read timeout value in seconds', default=10, type=int)
@click.option('--serial-xonxoff', help='enable software flow control. By default software flow control is disabled', is_flag=True)
@click.option('--show-output', help='choose output to display', default=('time', 'consumed', 'tariff', 'gas_measured_at'), multiple=True, type=click.Choice(['time', 'kwh_eid', 'gas_eid', 'consumed', 'tariff', 'gas_measured_at', 'produced', 'current']))
@click.option('--tsv', help='display packet in tab separated value form', is_flag=True)
def read_meter(elec_unit, gas_unit, raw, serial_baudrate, serial_bytesize, serial_parity, serial_port, serial_stopbits, serial_timeout, serial_xonxoff, show_output, tsv):
    '''
    read a single P1 packet to stdout.

    Read a single packet from the smart meter. Packets will be printed to
    stdout.

    All the options starting with --serial-* are passed directly to the
    underlying serial object. For more information on the possible values and
    their behavior please refer to the documentation here
    http://pyserial.readthedocs.io/en/latest/pyserial_api.html
    '''
    meter = SmartMeter(
        serial_port,
        baudrate=serial_baudrate,
        bytesize=int(serial_bytesize),
        parity=serial_parity,
        stopbits=float(serial_stopbits),
        xonxoff=serial_xonxoff,
        timeout=serial_timeout,
    )

    with meter:
        packet = meter.read_one_packet()

    if raw:
        print(str(packet))
        return 0

    # Set multiplication factor based on requested unit
    elec_unit_factor = {
        'Wh': 1000,
        'kWh': 1,
        'J': 1000 * 3600,
        'MJ': 1000 * 3600 / 1000 / 1000
    }
    gas_unit_factor = {
        'm3': 1000,
        'l': 1,
        'J': 43.935,
        'MJ': 1000 * 43.935  # 43.46 - 44.41 MJ/m^3(n) legal Wobbe-index ('Bovenwaarde') for Dutch Groningen gas, also widely used in north-west Europe: https://wetten.overheid.nl/BWBR0035367/2019-01-01#Bijlage2
    }

    # Construct output depending on user request
    data = []
    if ('time' in show_output):
        data.append(('Time', datetime.datetime.now()))
    if ('kwh_eid' in show_output):
        data.append(('Electricity serial', packet['kwh']['eid']))
    if ('gas_eid' in show_output):
        data.append(('Gas serial', packet['gas']['eid']))
    if ('consumed' in show_output):
        data.extend([
            ('Total electricity consumed (high, {})'.format(elec_unit), int(packet['kwh']['high']['consumed'] * elec_unit_factor[elec_unit])),
            ('Total electricity consumed (low, {})'.format(elec_unit), int(packet['kwh']['low']['consumed'] * elec_unit_factor[elec_unit])),
            ('Total gas consumed ({})'.format(gas_unit), int(packet['gas']['total'] * gas_unit_factor[gas_unit]))])
    if ('produced' in show_output):
        data.extend([
            ('Total electricity produced (high, {})'.format(elec_unit), int(packet['kwh']['high']['produced'] * elec_unit_factor[elec_unit])),
            ('Total electricity produced (low, {})'.format(elec_unit), int(packet['kwh']['low']['produced'] * elec_unit_factor[elec_unit]))])
    if ('current' in show_output):
        data.extend([
            ('Current electricity consumption (W)', int(packet['kwh']['current_consumed'] * 1000)),
            ('Current electricity production (W)', int(packet['kwh']['current_produced'] * 1000))])
    if ('tariff' in show_output):
        data.append(('Current electricity tariff', packet['kwh']['tariff']))
    if ('gas_measured_at' in show_output):
        data.append(('Gas measured at', packet['gas']['measured_at']))

    if tsv:
        print('\t'.join(map(str, [d for k, d in data])))
    else:
        print('\n'.join(['%-40s %s' % (k, d) for k, d in data]))

    return 0
