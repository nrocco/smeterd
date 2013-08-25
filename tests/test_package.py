from os.path import join, dirname, realpath
import sys

from nose.tools import raises

from smeterd.meter import P1Packet
from smeterd.meter import SmartMeterError

from tests import NORMAL_PACKET
from tests import BROKEN_PACKET




def test_default_packet_as_string():
    p = P1Packet(NORMAL_PACKET)
    assert p['header'] == '/ISk5\2ME382-1004'
    assert p['kwh']['eid'] == '4B414C37303035313135383130323132'
    assert p['kwh']['high']['consumed'] == 608.400
    assert p['kwh']['low']['consumed'] == 490.342
    assert p['kwh']['high']['produced'] == 0.001
    assert p['kwh']['low']['produced'] == 0
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


def test_default_packet_as_array():
    p = P1Packet(NORMAL_PACKET.split('\n'))
    assert p['header'] == '/ISk5\2ME382-1004'
    assert p['kwh']['eid'] == '4B414C37303035313135383130323132'
    assert p['kwh']['high']['consumed'] == 608.400
    assert p['kwh']['low']['consumed'] == 490.342
    assert p['kwh']['high']['produced'] == 0.001
    assert p['kwh']['low']['produced'] == 0
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


def test_BROKEN_PACKET():
    p = P1Packet(BROKEN_PACKET)
    assert p['header'] == ''
    assert p['kwh']['eid'] == None
    assert p['kwh']['high']['consumed'] == None
    assert p['kwh']['low']['consumed'] == None
    assert p['kwh']['high']['produced'] == None
    assert p['kwh']['low']['produced'] == None
    assert p['kwh']['tariff'] == None
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
