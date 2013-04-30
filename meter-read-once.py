#!/usr/bin/env python

import re
import logging
import serial



log = logging.getLogger(__name__)
VERSION = '1.0'


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
        self.port = self.serial.portstr


    def connect(self):
        if not self.serial.isOpen():
            log.debug('Opening connection to `%s`', self.serial.portstr)
            self.serial.open()
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
        while i > 0:
            raw.append(str(self.serial.readline()).strip())
            i = i - 1

        return P1Packet('\n'.join(raw))



class P1Packet(object):
    def __init__(self, data):
        self._data = data
        self.uid = RE_UID.search(data).group(1)
        self.kwh1 = float(RE_KWH1.search(data).group(1))
        self.kwh2 = float(RE_KWH2.search(data).group(1))
        self.gas = float(RE_GAS.search(data).group(1))
        self.tariff = int(RE_TARIFF.search(data).group(1))
        self.current_usage = float(RE_CURRENT_USAGE.search(data).group(1))

    def __str__(self):
        return self._data



def store_in_sqlite(dbfile, packet):
    import sqlite3
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data (date TEXT UNIQUE, kwh1 INTEGER, kwh2 INTEGER, gas INTEGER)''')
    c.execute('INSERT INTO data VALUES(?,?,?,?)', (datetime.datetime.now(),
                                                   int(packet.kwh1 * 1000),
                                                   int(packet.kwh2 * 1000),
                                                   int(packet.gas * 1000)))
    conn.commit()
    conn.close()


if '__main__' == __name__:
    import sys
    import datetime

    logging.basicConfig(level=logging.WARN, format='%(asctime)-15s %(message)s')
    log.info('Reading smart meter (version %s)', VERSION)

    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.setRTS(False)

    try:
        packet = meter.read_one_packet()
    except Exception as e:
        log.error(e)
        sys.exit(1)

    meter.disconnect()

    if packet:
        if len(sys.argv) > 1:
            store_in_sqlite(sys.argv[1], packet)
        else:
            print '%s\t%s\t%s\t%s' % (datetime.datetime.now(),
                                      int(packet.kwh1 * 1000),
                                      int(packet.kwh2 * 1000),
                                      int(packet.gas * 1000)
            )
