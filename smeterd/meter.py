import re
import logging
import serial
from datetime import datetime



log = logging.getLogger(__name__)


class SmartMeter(object):

    def __init__(self, port, *args, **kwargs):
        self.serial = serial.Serial(port, 9600, timeout=2,
                                    bytesize=serial.SEVENBITS,
                                    parity=serial.PARITY_EVEN,
                                    stopbits=serial.STOPBITS_ONE)
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
            try:
                line = self.serial.readline().decode('utf-8').strip()
            except:
                log.error('Read a total of %d lines', lines_read)
                raise
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

        self._keys = {
            'header': self.get(r'^(/ISk5.*)$', ''),
            'eid': self.get(r'^0-0:96\.1\.1\(([^)]+)\)$'),
            'kwh1_in': self.get_float(r'^1-0:1\.8\.1\(([0-9]{5}\.[0-9]{3})\*kWh\)$'),
            'kwh2_in': self.get_float(r'^1-0:1\.8\.2\(([0-9]{5}\.[0-9]{3})\*kWh\)$'),
            'kwh1_out': self.get_float(r'^1-0:2\.8\.1\(([0-9]{5}\.[0-9]{3})\*kWh\)$'),
            'kwh2_out': self.get_float(r'^1-0:2\.8\.2\(([0-9]{5}\.[0-9]{3})\*kWh\)$'),
            'tariff': self.get_int(r'^0-0:96\.14\.0\(([0-9]+)\)$'),
            'current_kwh_in': self.get_float(r'^1-0:1\.7\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$'),
            'current_kwh_out': self.get_float(r'^1-0:2\.7\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$'),
            'kwh_treshold': self.get_float(r'^0-0:17\.0\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$'),
            'switch': self.get_int(r'^0-0:96\.3\.10\((\d)\)$'),
            'txtmsg_code': self.get(r'^0-0:96\.13\.1\((\d+)\)$'),
            'txtmsg': self.get(r'^0-0:96\.13\.0\((.+)\)$'),
            'device_type': self.get_int(r'^0-1:24\.1\.0\((\d)\)$'),
            'eid_gas': self.get(r'^0-1:96\.1\.0\(([^)]+)\)$'),
            'gas': self.get_float(r'^\(([0-9]{5}\.[0-9]{3})\)$'),
            'valve': self.get_int(r'^0-1:24\.4\.0\((\d)\)$')
        }

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



def read_one_packet(serial_port='/dev/ttyUSB0'):
    meter = SmartMeter(serial_port)
    packet = meter.read_one_packet()
    meter.disconnect()

    return packet
