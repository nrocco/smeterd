import re
import logging
import serial



log = logging.getLogger(__name__)


class SmartMeter(object):

    def __init__(self, port, *args, **kwargs):
        try:
            self.serial = serial.Serial(
                port,
                9600,
                timeout=2,
                bytesize=serial.SEVENBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE
            )
        except serial.SerialException as e:
            raise SmartMeterError(e)
        else:
            self.serial.setRTS(False)
            self.port = self.serial.name

        log.info('New serial connection opened to %s', self.port)


    def connect(self):
        if not self.serial.isOpen():
            log.info('Opening connection to `%s`', self.serial.name)
            self.serial.open()
            self.serial.setRTS(False)
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
        lines = []
        lines_read = 0
        complete_packet = False

        log.info('Start reading lines')

        while not complete_packet:
            line = ''
            try:
                line = self.serial.readline().strip()
            except Exception as e:
                log.error(e)
                log.error('Read a total of %d lines', lines_read)
                raise SmartMeterError(e)
            else:
                lines_read += 1
                if line.startswith('/ISk5'):
                    lines = [line]
                else:
                    lines.append(line)
                if line == '!' and len(lines) > 19:
                    complete_packet = True
            finally:
                log.debug('>> %s', line)

        log.info('Done reading one packet (containing %d lines)' % len(lines))
        log.debug('Total lines read from serial port: %d', lines_read)
        log.debug('Constructing P1Packet from raw data')

        return P1Packet('\n'.join(lines))



class SmartMeterError(Exception):
    pass



class P1Packet(object):
    _raw = ''

    def __init__(self, data):
        if type(data) == list:
            self._raw = '\n'.join(data)
        else:
            self._raw = data

        keys = {}
        keys['header'] = self.get(r'^(/ISk5.*)$', '')

        keys['kwh'] = {}
        keys['kwh']['eid'] = self.get(r'^0-0:96\.1\.1\(([^)]+)\)$')
        keys['kwh']['tariff'] = self.get_int(r'^0-0:96\.14\.0\(([0-9]+)\)$')
        keys['kwh']['switch'] = self.get_int(r'^0-0:96\.3\.10\((\d)\)$')
        keys['kwh']['treshold'] = self.get_float(r'^0-0:17\.0\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$')

        keys['kwh']['high'] = {}
        keys['kwh']['high']['consumed'] = self.get_float(r'^1-0:1\.8\.1\(([0-9]{5}\.[0-9]{3})\*kWh\)$')
        keys['kwh']['high']['produced'] = self.get_float(r'^1-0:2\.8\.1\(([0-9]{5}\.[0-9]{3})\*kWh\)$')

        keys['kwh']['low'] = {}
        keys['kwh']['low']['consumed'] = self.get_float(r'^1-0:1\.8\.2\(([0-9]{5}\.[0-9]{3})\*kWh\)$')
        keys['kwh']['low']['produced'] = self.get_float(r'^1-0:2\.8\.2\(([0-9]{5}\.[0-9]{3})\*kWh\)$')

        keys['kwh']['current_consumed'] = self.get_float(r'^1-0:1\.7\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$')
        keys['kwh']['current_produced'] = self.get_float(r'^1-0:2\.7\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$')

        keys['gas'] = {}
        keys['gas']['eid'] = self.get(r'^0-1:96\.1\.0\(([^)]+)\)$')
        keys['gas']['device_type'] = self.get_int(r'^0-1:24\.1\.0\((\d)\)$')
        keys['gas']['total'] = self.get_float(r'^\(([0-9]{5}\.[0-9]{3})\)$')
        keys['gas']['valve'] = self.get_int(r'^0-1:24\.4\.0\((\d)\)$')

        keys['msg'] = {}
        keys['msg']['code'] = self.get(r'^0-0:96\.13\.1\((\d+)\)$')
        keys['msg']['text'] = self.get(r'^0-0:96\.13\.0\((.+)\)$')

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
        results = re.search(regex, self._raw, re.MULTILINE)
        if not results:
            return default
        return results.group(1)

    def __str__(self):
        return self._raw
