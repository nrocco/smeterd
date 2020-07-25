import unittest

from datetime import datetime
from smeterd.meter import P1Packet
from smeterd.meter import P1PacketError
from tests import BROKEN_PACKET
from tests import NORMAL_PACKET
from tests import NORMAL_PACKET_CRC_INVALID
from tests import NORMAL_PACKET_CRC_VALID
from tests import NORMAL_PACKET_KAIFA1
from tests import NORMAL_PACKET_KAIFA2
from tests import NORMAL_PACKET_KAIFA3
from time import mktime


class PackageTestCase(unittest.TestCase):
    def test_default_packet_as_string(self):
        p = P1Packet(NORMAL_PACKET)
        self.assertEqual(p['header'], '/ISk5\2ME382-1004')
        self.assertEqual(p['kwh']['eid'], 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX')
        self.assertEqual(p['kwh']['low']['consumed'], 608.400)
        self.assertEqual(p['kwh']['high']['consumed'], 490.342)
        self.assertEqual(p['kwh']['low']['produced'], 0.001)
        self.assertEqual(p['kwh']['high']['produced'], 0)
        self.assertEqual(p['kwh']['tariff'], 1)
        self.assertEqual(p['kwh']['current_consumed'], 1.51)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], 999)
        self.assertEqual(p['kwh']['switch'], 1)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '3238303131303031323332313337343132')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 947.680)
        self.assertEqual(p['gas']['valve'], 1)
        self.assertEqual(p._datagram, NORMAL_PACKET)

    def test_default_packet_as_array(self):
        p = P1Packet(NORMAL_PACKET)
        self.assertEqual(p['header'], '/ISk5\2ME382-1004')
        self.assertEqual(p['kwh']['eid'], 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX')
        self.assertEqual(p['kwh']['low']['consumed'], 608.400)
        self.assertEqual(p['kwh']['high']['consumed'], 490.342)
        self.assertEqual(p['kwh']['low']['produced'], 0.001)
        self.assertEqual(p['kwh']['high']['produced'], 0)
        self.assertEqual(p['kwh']['tariff'], 1)
        self.assertEqual(p['kwh']['current_consumed'], 1.51)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], 999)
        self.assertEqual(p['kwh']['switch'], 1)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '3238303131303031323332313337343132')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 947.680)
        self.assertEqual(p['gas']['valve'], 1)
        self.assertEqual(p._datagram, NORMAL_PACKET)

    def test_BROKEN_PACKET(self):
        p = P1Packet(BROKEN_PACKET)
        self.assertEqual(p['header'], None)
        self.assertEqual(p['kwh']['eid'], None)
        self.assertEqual(p['kwh']['low']['consumed'], None)
        self.assertEqual(p['kwh']['high']['consumed'], None)
        self.assertEqual(p['kwh']['low']['produced'], None)
        self.assertEqual(p['kwh']['high']['produced'], None)
        self.assertEqual(p['kwh']['tariff'], None)
        self.assertEqual(p['kwh']['current_consumed'], 1.51)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], 999)
        self.assertEqual(p['kwh']['switch'], 1)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '3238303131303031323332313337343132')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('130810180000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 947.680)
        self.assertEqual(p['gas']['valve'], 1)

    def test_normal_packet_kaifa1_as_string(self):
        p = P1Packet(NORMAL_PACKET_KAIFA1)
        self.assertEqual(p['header'], '/KFM5KAIFA-METER', "{0} is not as expected".format(str(p['header'])))
        self.assertEqual(p['kwh']['eid'], 'XXXXXXXXXXXXXXMYSERIALXXXXXXXXXXXXXX')
        self.assertEqual(p['kwh']['low']['consumed'], 498.215)
        self.assertEqual(p['kwh']['high']['consumed'], 550.159)
        self.assertEqual(p['kwh']['low']['produced'], 0.001)
        self.assertEqual(p['kwh']['high']['produced'], 0)
        self.assertEqual(p['kwh']['tariff'], 2)
        self.assertEqual(p['kwh']['current_consumed'], 0.235)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], None)
        self.assertEqual(p['kwh']['switch'], None)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '4730303235303033333337343136333136')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('160905190000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 323.528)
        self.assertEqual(p['gas']['valve'], None)
        self.assertEqual(p._datagram, NORMAL_PACKET_KAIFA1)

    def test_normal_packet_kaifa2_as_string(self):
        p = P1Packet(NORMAL_PACKET_KAIFA2)
        self.assertEqual(p['header'], '/XMX5LGBBFFB231158062')
        self.assertEqual(p['kwh']['eid'], 'XXXXXXXXSERIALXXXXXXXXXXX')
        self.assertEqual(p['kwh']['low']['consumed'], 4018.859)
        self.assertEqual(p['kwh']['high']['consumed'], 2827.154)
        self.assertEqual(p['kwh']['low']['produced'], 0.002)
        self.assertEqual(p['kwh']['high']['produced'], 0)
        self.assertEqual(p['kwh']['tariff'], 1)
        self.assertEqual(p['kwh']['current_consumed'], 0.341)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], None)
        self.assertEqual(p['kwh']['switch'], None)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '4730303233353631323139373231393134')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('160904220000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 5290.211)
        self.assertEqual(p['gas']['valve'], None)
        self.assertEqual(p._datagram, NORMAL_PACKET_KAIFA2)

    def test_normal_packet_kaifa3_as_string(self):
        p = P1Packet(NORMAL_PACKET_KAIFA3)
        self.assertEqual(p['header'], '/KFM5KAIFA-METER')
        self.assertEqual(p['kwh']['eid'], 'XXXXXXXXSERIALXXXXXXXXXXX')
        self.assertEqual(p['kwh']['low']['consumed'], 608.303)
        self.assertEqual(p['kwh']['high']['consumed'], 598.271)
        self.assertEqual(p['kwh']['low']['produced'], 0)
        self.assertEqual(p['kwh']['high']['produced'], 0)
        self.assertEqual(p['kwh']['tariff'], 1)
        self.assertEqual(p['kwh']['current_consumed'], 1.263)
        self.assertEqual(p['kwh']['current_produced'], 0)
        self.assertEqual(p['kwh']['treshold'], None)
        self.assertEqual(p['kwh']['switch'], None)
        self.assertEqual(p['msg']['code'], None)
        self.assertEqual(p['msg']['text'], None)
        self.assertEqual(p['gas']['device_type'], 3)
        self.assertEqual(p['gas']['eid'], '4730303332353631323639323539363136')
        self.assertEqual(p['gas']['measured_at'], int(mktime(datetime.strptime('161106180000', "%y%m%d%H%M%S").timetuple())))
        self.assertEqual(p['gas']['total'], 230.576)
        self.assertEqual(p['gas']['valve'], None)
        self.assertEqual(p._datagram, NORMAL_PACKET_KAIFA3)

    def test_normal_packet_with_crc_check(self):
        p = P1Packet(NORMAL_PACKET_CRC_VALID)
        self.assertEqual(p['header'], '/KFM5KAIFA-METER')
        self.assertEqual(p['kwh']['tariff'], 2)
        self.assertEqual(p['gas']['total'], 1350.170)
        self.assertEqual(p._datagram, NORMAL_PACKET_CRC_VALID)

    def test_normal_packet_with_invalid_crc_check(self):
        with self.assertRaises(P1PacketError):
            P1Packet(NORMAL_PACKET_CRC_INVALID)
