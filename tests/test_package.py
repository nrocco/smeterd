import os
import sys

from nose.tools import raises

from smeterd.meter import P1Packet
from smeterd.meter import SmartMeterError



normal_packet = '''/ISk5\2ME382-1004

0-0:96.1.1(4B414C37303035313135383130323132)
1-0:1.8.1(00608.400*kWh)
1-0:1.8.2(00490.342*kWh)
1-0:2.8.1(00000.001*kWh)
1-0:2.8.2(00000.000*kWh)
0-0:96.14.0(0001)
1-0:1.7.0(0001.51*kW)
1-0:2.7.0(0000.00*kW)
0-0:17.0.0(0999.00*kW)
0-0:96.3.10(1)
0-0:96.13.1()
0-0:96.13.0()
0-1:24.1.0(3)
0-1:96.1.0(3238303131303031323332313337343132)
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)
(00947.680)
0-1:24.4.0(1)
!'''


def test_default_packet():
    p = P1Packet(normal_packet)
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
    assert str(p) == normal_packet


def test_default_packet():
    p = P1Packet(normal_packet.split('\n'))
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
    assert str(p) == normal_packet


def test_broken_packet():
    p = P1Packet('''
1-0:1.7.0(0001.51*kW)
1-0:2.7.0(0000.00*kW)
0-0:17.0.0(0999.00*kW)
0-0:96.3.10(1)
0-0:96.13.1()
0-0:96.13.0()
0-1:24.1.0(3)
0-1:96.1.0(3238303131303031323332313337343132)
0-1:24.3.0(130810180000)(00)(60)(1)(0-1:24.2.1)(m3)
(00947.680)
0-1:24.4.0(1)
!''')
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
