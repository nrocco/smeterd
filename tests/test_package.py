from time import mktime
from datetime import datetime
from os.path import join, dirname, realpath
import sys

from nose.tools import raises

from smeterd.meter import P1Packet
from smeterd.meter import SmartMeterError
from smeterd.meter import P1PacketError

from tests import NORMAL_PACKET
from tests import BROKEN_PACKET
from tests import NORMAL_PACKET_KAIFA1
from tests import NORMAL_PACKET_KAIFA2
from tests import NORMAL_PACKET_KAIFA3
from tests import NORMAL_PACKET_CRC_VALID
from tests import NORMAL_PACKET_CRC_INVALID


def test_default_packet_as_string():
    p = P1Packet(NORMAL_PACKET)

    assert p['header'] == '/ISk5\2ME382-1004'
    assert p['kwh']['eid'] == 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX'
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
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 947.680
    assert p['gas']['valve'] == 1
    assert p._datagram == NORMAL_PACKET


def test_default_packet_as_array():
    p = P1Packet(NORMAL_PACKET)
    assert p['header'] == '/ISk5\2ME382-1004'
    assert p['kwh']['eid'] == 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX'
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
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 947.680
    assert p['gas']['valve'] == 1
    assert p._datagram == NORMAL_PACKET


def test_BROKEN_PACKET():
    p = P1Packet(BROKEN_PACKET)
    assert p['header'] == None
    assert p['kwh']['eid'] == None
    assert p['kwh']['low']['consumed'] == None
    assert p['kwh']['high']['consumed'] == None
    assert p['kwh']['low']['produced'] == None
    assert p['kwh']['high']['produced'] == None
    assert p['kwh']['tariff'] == None
    assert p['kwh']['current_consumed'] == 1.51
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == 999
    assert p['kwh']['switch'] == 1
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert p['gas']['device_type'] == 3
    assert p['gas']['eid'] == '3238303131303031323332313337343132'
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 947.680
    assert p['gas']['valve'] == 1


def test_normal_packet_kaifa1_as_string():
    p = P1Packet(NORMAL_PACKET_KAIFA1)
    assert p['header'] == '/KFM5KAIFA-METER', "{0} is not as expected".format(str(p['header']))
    assert p['kwh']['eid'] == 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX'
    assert p['kwh']['low']['consumed'] == 498.215
    assert p['kwh']['high']['consumed'] == 550.159
    assert p['kwh']['low']['produced'] == 0.001
    assert p['kwh']['high']['produced'] == 0
    assert p['kwh']['tariff'] == 2
    assert p['kwh']['current_consumed'] == 0.235
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == None
    assert p['kwh']['switch'] == None
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert p['gas']['device_type'] == 3
    assert p['gas']['eid'] == '4730303235303033333337343136333136'
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('160905190000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 323.528
    assert p['gas']['valve'] == None
    assert p._datagram == NORMAL_PACKET_KAIFA1


def test_normal_packet_kaifa2_as_string():
    p = P1Packet(NORMAL_PACKET_KAIFA2)
    assert p['header'] == '/XMX5LGBBFFB231158062'
    assert p['kwh']['eid'] == 'XXXXXXXXSERIALXXXXXXXXXXX'
    assert p['kwh']['low']['consumed'] == 4018.859
    assert p['kwh']['high']['consumed'] == 2827.154
    assert p['kwh']['low']['produced'] == 0.002
    assert p['kwh']['high']['produced'] == 0
    assert p['kwh']['tariff'] == 1
    assert p['kwh']['current_consumed'] == 0.341
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == None
    assert p['kwh']['switch'] == None
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert p['gas']['device_type'] == 3
    assert p['gas']['eid'] == '4730303233353631323139373231393134'
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('160904220000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 5290.211
    assert p['gas']['valve'] == None
    assert p._datagram == NORMAL_PACKET_KAIFA2


def test_normal_packet_kaifa3_as_string():
    p = P1Packet(NORMAL_PACKET_KAIFA3)
    assert p['header'] == '/KFM5KAIFA-METER'
    assert p['kwh']['eid'] == 'XXXXXXXXSERIALXXXXXXXXXXX'
    assert p['kwh']['low']['consumed'] == 608.303
    assert p['kwh']['high']['consumed'] == 598.271
    assert p['kwh']['low']['produced'] == 0
    assert p['kwh']['high']['produced'] == 0
    assert p['kwh']['tariff'] == 1
    assert p['kwh']['current_consumed'] == 1.263
    assert p['kwh']['current_produced'] == 0
    assert p['kwh']['treshold'] == None
    assert p['kwh']['switch'] == None
    assert p['msg']['code'] == None
    assert p['msg']['text'] == None
    assert p['gas']['device_type'] == 3
    assert p['gas']['eid'] == '4730303332353631323639323539363136'
    assert p['gas']['measured_at'] == int(mktime(datetime.strptime('161106180000', "%y%m%d%H%M%S").timetuple()))
    assert p['gas']['total'] == 230.576
    assert p['gas']['valve'] == None
    assert p._datagram == NORMAL_PACKET_KAIFA3


def test_normal_packet_with_crc_check():
    p = P1Packet(NORMAL_PACKET_CRC_VALID)
    assert p['header'] == '/KFM5KAIFA-METER'
    assert p['kwh']['tariff'] == 2
    assert p['gas']['total'] == 1350.170
    assert p._datagram == NORMAL_PACKET_CRC_VALID


@raises(P1PacketError)
def test_normal_packet_with_invalid_crc_check():
    p = P1Packet(NORMAL_PACKET_CRC_INVALID)
