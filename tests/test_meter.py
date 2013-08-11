import serial

from nose.tools import raises

from smeterd.meter import SmartMeter
from smeterd.meter import SmartMeterError
from smeterd.meter import read_one_packet

from tests import SerialMock
from tests import NORMAL_PACKET
from tests import BROKEN_PACKET



Serial = serial.Serial

@raises(TypeError)
def test_meter_typeerror():
    meter = SmartMeter()


@raises(SmartMeterError)
def test_meter_tty_not_available():
    meter = SmartMeter('/dev/ttyUSB0')


@raises(SmartMeterError)
def test_meter_tty_not_available_again():
    p = read_one_packet()


def test_meter_connect_twice():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    assert meter.connected() == True
    meter.connect()
    assert meter.connected() == True
    meter.connect()
    assert meter.connected() == True


def test_meter_disconnect_twice():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    assert meter.connected() == True
    meter.disconnect()
    assert meter.connected() == False
    meter.disconnect()
    assert meter.connected() == False


def test_meter_disconnect_and_connect():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    assert meter.connected() == True
    meter.disconnect()
    assert meter.connected() == False
    meter.connect()
    assert meter.connected() == True



def test_meter_ok():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    assert meter.port == '/dev/ttyUSB0'
    assert meter.connected() == True


def test_meter_read_one_packet():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.lines_in_buffer = NORMAL_PACKET.split('\n')

    p = meter.read_one_packet()
    assert p['header'] == '/ISk5\2ME382-1004'
    assert p['eid'] == '4B414C37303035313135383130323132'
    assert p['kwh1_in'] == 608.400
    assert p['kwh2_in'] == 490.342
    assert p['kwh1_out'] == 0.001
    assert p['kwh2_out'] == 0
    assert p['tariff'] == 1
    assert p['current_kwh_in'] == 1.51
    assert p['current_kwh_out'] == 0
    assert p['kwh_treshold'] == 999
    assert p['switch'] == 1
    assert p['txtmsg_code'] == None
    assert p['txtmsg'] == None
    assert p['device_type'] == 3
    assert p['eid_gas'] == '3238303131303031323332313337343132'
    assert p['gas'] == 947.680
    assert p['valve'] == 1
    assert str(p) == NORMAL_PACKET


@raises(SmartMeterError)
def test_meter_read_broken_packet():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.lines_in_buffer = BROKEN_PACKET.split('\n')
    meter.read_one_packet()
