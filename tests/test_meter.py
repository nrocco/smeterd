import serial

from nose.tools import raises

from smeterd.meter import SmartMeter
from smeterd.meter import SmartMeterError

from tests import SerialMock
from tests import NORMAL_PACKET
from tests import BROKEN_PACKET
from tests import LONG_BROKEN_PACKET
from tests import NORMAL_PACKET_1003

Serial = serial.Serial

@raises(TypeError)
def test_meter_typeerror():
    meter = SmartMeter()


@raises(SmartMeterError)
def test_meter_tty_not_available():
    meter = SmartMeter('/dev/ttyUSB0')


@raises(SmartMeterError)
def test_meter_tty_not_available_again():
    meter = SmartMeter('/dev/ttyUSB0')
    packet = meter.read_one_packet()


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
    assert p['kwh']['eid'] == '4B414C37303035313135383130323132'
    assert p['kwh']['low']['consumed'] == 608.400
    assert p['kwh']['high']['consumed'] == 490.342
    assert p['kwh']['low']['produced'] == 0.001
    assert p['kwh']['high']['produced'] == 0
    assert p['kwh']['tariff'] == 1
    assert p['kwh']['current_consumed'] == 1.51
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == 999
    assert p['kwh']['switch'] == 1
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert p['gas']['device_type'] == 3
    assert p['gas']['eid'] == '3238303131303031323332313337343132'
    assert p['gas']['total'] == 947.680
    assert p['gas']['valve'] == 1
    assert str(p) == NORMAL_PACKET


def test_meter_read_one_packet_1003():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.lines_in_buffer = NORMAL_PACKET_1003.split('\n')

    p = meter.read_one_packet()
    assert p['header'] == '/ISk5\2ME382-1003'
    assert p['kwh']['eid'] == '5A424556303035303933313937373132'
    assert p['kwh']['low']['consumed'] == 608.400
    assert p['kwh']['high']['consumed'] == 490.342
    assert p['kwh']['low']['produced'] == 0.001
    assert p['kwh']['high']['produced'] == 0
    assert p['kwh']['tariff'] == 1
    assert p['kwh']['current_consumed'] == 1.51
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == 999
    assert p['kwh']['switch'] == 1
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert str(p) == NORMAL_PACKET_1003


@raises(SmartMeterError)
def test_meter_read_broken_packet():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.lines_in_buffer = BROKEN_PACKET.split('\n')
    meter.read_one_packet()
    

@raises(SmartMeterError)
def test_meter_read_long_broken_packet():
    serial.Serial = SerialMock
    meter = SmartMeter('/dev/ttyUSB0')
    meter.serial.lines_in_buffer = LONG_BROKEN_PACKET.split('\n')
    meter.read_one_packet()    
