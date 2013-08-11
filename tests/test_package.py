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
    assert unicode(p) == NORMAL_PACKET


def test_default_packet_as_array():
    p = P1Packet(NORMAL_PACKET.split('\n'))
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
    assert unicode(p) == NORMAL_PACKET


def test_BROKEN_PACKET():
    p = P1Packet(BROKEN_PACKET)
    assert p['header'] == ''
    assert p['eid'] == None
    assert p['kwh1_in'] == None
    assert p['kwh2_in'] == None
    assert p['kwh1_out'] == None
    assert p['kwh2_out'] == None
    assert p['tariff'] == None
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
