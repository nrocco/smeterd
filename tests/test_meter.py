import unittest

from smeterd.meter import SmartMeter
from smeterd.meter import SmartMeterError
from tests import BROKEN_PACKET
from tests import LONG_BROKEN_PACKET
from tests import NORMAL_PACKET
from tests import NORMAL_PACKET_1003
from unittest import mock


class MeterTestCase(unittest.TestCase):
    def test_meter_typeerror(self):
        with self.assertRaises(TypeError):
            SmartMeter()

    def test_meter_tty_not_available(self):
        with self.assertRaises(SmartMeterError):
            SmartMeter('/dev/ttyUSB0')

    def test_meter_tty_not_available_again(self):
        with self.assertRaises(SmartMeterError):
            SmartMeter('/dev/ttyUSB0').read_one_packet()

    @mock.patch('serial.Serial')
    def test_meter_connect_twice(self, mocked_serial):
        mocked_serial.return_value.isOpen.side_effect = [True, True, True, True, True]
        meter = SmartMeter('/dev/ttyUSB0')
        self.assertTrue(meter.connected())

        meter.connect()
        mocked_serial.return_value.open.assert_not_called()
        self.assertTrue(meter.connected())

        meter.connect()
        mocked_serial.return_value.open.assert_not_called()
        self.assertTrue(meter.connected())

    @mock.patch('serial.Serial')
    def test_meter_disconnect_twice(self, mocked_serial):
        mocked_serial.return_value.isOpen.side_effect = [True, True, False, False, False]
        meter = SmartMeter('/dev/ttyUSB0')
        self.assertTrue(meter.connected())
        meter.disconnect()
        mocked_serial.return_value.close.assert_called()
        mocked_serial.return_value.close.reset_mock()
        self.assertFalse(meter.connected())
        meter.disconnect()
        mocked_serial.return_value.close.assert_not_called()
        self.assertFalse(meter.connected())

    @mock.patch('serial.Serial')
    def test_meter_disconnect_and_connect(self, mocked_serial):
        mocked_serial.return_value.isOpen.side_effect = [True, True, False, False, True]
        meter = SmartMeter('/dev/ttyUSB0')
        self.assertTrue(meter.connected())
        mocked_serial.return_value.isOpen.assert_called()
        meter.disconnect()
        mocked_serial.return_value.isOpen.assert_called()
        self.assertFalse(meter.connected())
        mocked_serial.return_value.isOpen.assert_called()
        meter.connect()
        mocked_serial.return_value.isOpen.assert_called()
        self.assertTrue(meter.connected())
        mocked_serial.return_value.isOpen.assert_called()

    @mock.patch('serial.Serial', **{'return_value.name': '/dev/ttyUSB0'})
    def test_meter_ok(self, mocked_serial):
        mocked_serial.return_value.isOpen.return_value = True
        meter = SmartMeter('/dev/ttyUSB0')
        self.assertTrue(meter.connected())
        self.assertEqual(meter.port, '/dev/ttyUSB0')

    @mock.patch('serial.Serial')
    def test_meter_read_one_packet(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET.splitlines(True)
        p = SmartMeter('/dev/ttyUSB0').read_one_packet()
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
        self.assertEqual(p['gas']['total'], 947.680)
        self.assertEqual(p['gas']['valve'], 1)
        self.assertEqual(p._datagram, NORMAL_PACKET)

    @mock.patch('serial.Serial')
    def test_meter_read_one_packet_1003(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET_1003.splitlines(True)
        p = SmartMeter('/dev/ttyUSB0').read_one_packet()
        self.assertEqual(p['header'], '/ISk5\2ME382-1003')
        self.assertEqual(p['kwh']['eid'], '5A424556303035303933313937373132')
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
        self.assertEqual(p._datagram, NORMAL_PACKET_1003)

    @mock.patch('serial.Serial')
    def test_meter_read_broken_packet(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = BROKEN_PACKET.splitlines(True)
        with self.assertRaises(SmartMeterError):
            SmartMeter('/dev/ttyUSB0').read_one_packet()

    @mock.patch('serial.Serial')
    def test_meter_read_long_broken_packet(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = LONG_BROKEN_PACKET.splitlines(True)
        with self.assertRaises(SmartMeterError):
            SmartMeter('/dev/ttyUSB0').read_one_packet()
