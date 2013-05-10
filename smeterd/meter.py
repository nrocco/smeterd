import re
import logging
import serial
from datetime import datetime



log = logging.getLogger(__name__)


RE_UID = re.compile(r'^0-0:96\.1\.1\(([^)]+)\)$', re.MULTILINE)
RE_KWH1 = re.compile(r'^1-0:1\.8\.1\(([0-9]{5}\.[0-9]{3})\*kWh\)$', re.MULTILINE)
RE_KWH2 = re.compile(r'^1-0:1\.8\.2\(([0-9]{5}\.[0-9]{3})\*kWh\)$', re.MULTILINE)
RE_GAS = re.compile(r'^\(([0-9]{5}\.[0-9]{3})\)$', re.MULTILINE)
RE_TARIFF = re.compile(r'^0-0:96\.14\.0\(([0-9]+)\)$', re.MULTILINE)
RE_CURRENT_USAGE = re.compile(r'^1-0:1\.7\.0\(([0-9]{4}\.[0-9]{2})\*kW\)$', re.MULTILINE)



class SmartMeter(object):

    def __init__(self, port, *args, **kwargs):
        self.serial = serial.Serial(port, 9600, timeout=2,
                                    bytesize=serial.SEVENBITS,
                                    parity=serial.PARITY_EVEN,
                                    stopbits=serial.STOPBITS_ONE)
        self.serial.setRTS(False)
        self.port = self.serial.portstr
        log.debug('New serial connection opened to %s', self.port)


    def connect(self):
        if not self.serial.isOpen():
            log.debug('Opening connection to `%s`', self.serial.portstr)
            self.serial.open()
            self.serial.setRTS(False)
        else:
            log.debug('`%s` was already open.', self.serial.portstr)


    def disconnect(self):
        if self.serial.isOpen():
            log.debug('Closing connection to `%s`.', self.serial.portstr)
            self.serial.close()
        else:
            log.debug('`%s` was already closed.', self.serial.portstr)


    def connected(self):
        return self.serial.isOpen()


    def read_one_packet(self):
        raw = []
        i = 20
        log.debug('Start reading %d lines', i)
        while i > 0:
            raw.append(str(self.serial.readline()).strip())
            i = i - 1
        log.debug('Done reading lines. Constructing P1Packet')
        return P1Packet('\n'.join(raw))



class P1Packet(object):
    def __init__(self, data):
        self._data = data
        self.date = datetime.now()
        self.uid = RE_UID.search(data).group(1)
        self.kwh1 = float(RE_KWH1.search(data).group(1))
        self.kwh2 = float(RE_KWH2.search(data).group(1))
        self.gas = float(RE_GAS.search(data).group(1))
        self.tariff = int(RE_TARIFF.search(data).group(1))
        self.current_usage = float(RE_CURRENT_USAGE.search(data).group(1))

    def kwh1_asint(self):
        return int(self.kwh1 * 1000)

    def kwh2_asint(self):
        return int(self.kwh2 * 1000)

    def gas_asint(self):
        return int(self.gas * 1000)

    def __str__(self):
        return self._data


def read_one_packet(serial_port='/dev/ttyUSB0'):
    meter = SmartMeter(serial_port)
    packet = meter.read_one_packet()
    meter.disconnect()
    return packet
