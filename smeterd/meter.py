import re
import logging
import serial
import crcmod.predefined

from time import mktime
from datetime import datetime


log = logging.getLogger(__name__)
crc16 = crcmod.predefined.mkPredefinedCrcFun('crc16')


class SmartMeter(object):
    serial_defaults = {
        'baudrate': 9600,
        'bytesize': serial.SEVENBITS,
        'parity': serial.PARITY_EVEN,
        'stopbits': serial.STOPBITS_ONE,
        'xonxoff': False,
        'timeout': 10,
    }
    serial_rts = False

    def __init__(self, port, **kwargs):
        config = {}
        config.update(self.serial_defaults)

        # This is quite uggly. The config part should probably be rewritten.
        if 'rts' in kwargs:
            self.serial_rts = kwargs['rts']
            del kwargs['rts']
        config.update(kwargs)

        log.debug('Open serial connect to {} with: {}'.format(port, ', '.join('{}={}'.format(key, value) for key, value in config.items())))

        try:
            self.serial = serial.Serial(port, **config)
        except (serial.SerialException, OSError) as e:
            raise SmartMeterError(e)
        else:
            self.serial.rts = self.serial_rts
            self.port = self.serial.name

        log.info('New serial connection opened to %s', self.port)

    def connect(self):
        if not self.serial.isOpen():
            log.info('Opening connection to `%s`', self.serial.name)
            self.serial.open()
            self.serial.rts = self.serial_rts
        else:
            log.debug('`%s` was already open.', self.serial.name)

    def disconnect(self):
        if self.serial.isOpen():
            log.info('Closing connection to `%s`.', self.serial.name)
            self.serial.close()
        else:
            log.debug('`%s` was already closed.', self.serial.name)

    def connected(self):
        return self.serial.isOpen()

    def read_one_packet(self):
        datagram = b''
        lines_read = 0
        startFound = False
        endFound = False

        log.info('Start reading lines')

        while not startFound or not endFound:
            try:
                line = self.serial.readline()
                log.debug('>> %s', line.decode('ascii').rstrip())
            except Exception as e:
                log.error(e)
                log.error('Read a total of %d lines', lines_read)
                raise SmartMeterError(e)

            lines_read += 1

            if re.match(rb'.*(?=/)', line):
                startFound = True
                endFound = False
                datagram = line.lstrip()
            elif re.match(rb'(?=!)', line):
                endFound = True
                datagram = datagram + line
            else:
                datagram = datagram + line

            # TODO: build in some protection for infinite loops

        log.info('Done reading one packet (containing %d lines)' % len(datagram.splitlines()))
        log.debug('Total lines read from serial port: %d', lines_read)
        log.debug('Constructing P1Packet from raw data')

        return P1Packet(datagram)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()


class SmartMeterError(Exception):
    pass


class P1PacketError(Exception):
    pass


class P1Packet(object):
    _datagram = ''

    def __init__(self, datagram):
        self._datagram = datagram

        self.validate()

        keys = {}

        keys['header'] = self.get(rb'^\s*(/.*)\r\n')
        keys['version'] = self.get_int(rb'^1-3:0\.2\.8\((\d+)\)\r\n')

        timestamp = self.get(rb'^0-0:1\.0\.0\((\d+)[SW]\)\r\n')

        if timestamp:
            keys['timestamp'] = int(mktime(datetime.strptime(timestamp, "%y%m%d%H%M%S").timetuple()))
        else:
            keys['timestamp'] = None

        keys['kwh'] = {}
        keys['kwh']['eid'] = self.get(rb'^0-0:96\.1\.1\(([^)]+)\)\r\n')
        keys['kwh']['tariff'] = self.get_int(rb'^0-0:96\.14\.0\(([0-9]+)\)\r\n')
        keys['kwh']['switch'] = self.get_int(rb'^0-0:96\.3\.10\((\d)\)\r\n')
        keys['kwh']['treshold'] = self.get_float(rb'^0-0:17\.0\.0\(([0-9]{4}\.[0-9]{2})\*kW\)\r\n')

        keys['kwh']['low'] = {}
        keys['kwh']['low']['consumed'] = self.get_float(rb'^1-0:1\.8\.1\(([0-9]+\.[0-9]+)\*kWh\)\r\n')
        keys['kwh']['low']['produced'] = self.get_float(rb'^1-0:2\.8\.1\(([0-9]+\.[0-9]+)\*kWh\)\r\n')

        keys['kwh']['high'] = {}
        keys['kwh']['high']['consumed'] = self.get_float(rb'^1-0:1\.8\.2\(([0-9]+\.[0-9]+)\*kWh\)\r\n')
        keys['kwh']['high']['produced'] = self.get_float(rb'^1-0:2\.8\.2\(([0-9]+\.[0-9]+)\*kWh\)\r\n')

        keys['kwh']['current_consumed'] = self.get_float(rb'^1-0:1\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        keys['kwh']['current_produced'] = self.get_float(rb'^1-0:2\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')

        keys['instantaneous'] = {}
        keys['instantaneous']['l1'] = {}
        keys['instantaneous']['l1']['volts'] = self.get_float(rb'^1-0:32\.7\.0\((\d+\.\d+)\*V\)\r\n')
        keys['instantaneous']['l1']['amps'] = self.get_int(rb'^1-0:31\.7\.0\((\d+)\*A\)\r\n')
        keys['instantaneous']['l1']['watts'] = self.get_float(rb'^1-0:21\.7\.0\((\d+\.\d+)\*kW\)\r\n', 0) * 1000
        keys['instantaneous']['l2'] = {}
        keys['instantaneous']['l2']['volts'] = self.get_float(rb'^1-0:52\.7\.0\((\d+\.\d+)\*V\)\r\n')
        keys['instantaneous']['l2']['amps'] = self.get_int(rb'^1-0:51\.7\.0\((\d+)\*A\)\r\n')
        keys['instantaneous']['l2']['watts'] = self.get_float(rb'^1-0:41\.7\.0\((\d+\.\d+)\*kW\)\r\n', 0) * 1000
        keys['instantaneous']['l3'] = {}
        keys['instantaneous']['l3']['volts'] = self.get_float(rb'^1-0:72\.7\.0\((\d+\.\d+)\*V\)\r\n')
        keys['instantaneous']['l3']['amps'] = self.get_int(rb'^1-0:71\.7\.0\((\d+)\*A\)\r\n')
        keys['instantaneous']['l3']['watts'] = self.get_float(rb'^1-0:61\.7\.0\((\d+\.\d+)\*kW\)\r\n', 0) * 1000

        keys['gas'] = {}
        keys['gas']['eid'] = self.get(rb'^0-1:96\.1\.0\(([^)]+)\)\r\n')
        keys['gas']['device_type'] = self.get_int(rb'^0-1:24\.1\.0\((\d)+\)\r\n')
        keys['gas']['total'] = self.get_float(rb'^(?:0-1:24\.2\.1(?:\(\d+[SW]\))?)?\(([0-9]{5}\.[0-9]{3})(?:\*m3)?\)\r\n', 0)
        keys['gas']['valve'] = self.get_int(rb'^0-1:24\.4\.0\((\d)\)\r\n')

        measured_at = self.get(rb'^(?:0-1:24\.[23]\.[01](?:\((\d+)[SW]?\))?)')

        if measured_at:
            keys['gas']['measured_at'] = int(mktime(datetime.strptime(measured_at, "%y%m%d%H%M%S").timetuple()))
        else:
            keys['gas']['measured_at'] = None

        keys['msg'] = {}
        keys['msg']['code'] = self.get(rb'^0-0:96\.13\.1\((\d+)\)\r\n')
        keys['msg']['text'] = self.get(rb'^0-0:96\.13\.0\((.+)\)\r\n')

        self._keys = keys

    def __getitem__(self, key):
        return self._keys[key]

    def get_float(self, regex, default=None):
        result = self.get(regex, None)
        if not result:
            return default
        return float(self.get(regex, default))

    def get_int(self, regex, default=None):
        result = self.get(regex, None)
        if not result:
            return default
        return int(result)

    def get(self, regex, default=None):
        results = re.search(regex, self._datagram, re.MULTILINE)
        if not results:
            return default
        return results.group(1).decode('ascii')

    def validate(self):
        pattern = re.compile(rb'\r\n(?=!)')
        for match in pattern.finditer(self._datagram):
            packet = self._datagram[:match.end() + 1]
            checksum = self._datagram[match.end() + 1:]

        if checksum.strip():
            given_checksum = int('0x' + checksum.decode('ascii').strip(), 16)
            calculated_checksum = crc16(packet)

            if given_checksum != calculated_checksum:
                log.error('Checksum mismatch: given={}, calculated={}'.format(given_checksum, calculated_checksum))
                raise P1PacketError('P1Packet with invalid checksum found')

    def __str__(self):
        return self._datagram.decode('ascii')
