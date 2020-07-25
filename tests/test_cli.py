import unittest

from click.testing import CliRunner
from smeterd.cli import cli
from tests import BROKEN_PACKET
from tests import NORMAL_PACKET
from unittest import mock


class CliTestCase(unittest.TestCase):
    @mock.patch('serial.Serial')
    def test_cli(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET.splitlines(True)
        runner = CliRunner()
        result = runner.invoke(cli, [
            'read-meter',
        ])
        mocked_serial.assert_called_with('/dev/ttyUSB0', baudrate=9600, bytesize=7, parity='E', stopbits=1.0, xonxoff=False, timeout=10)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('serial.Serial')
    def test_cli_broken(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = BROKEN_PACKET.splitlines(True)
        runner = CliRunner()
        result = runner.invoke(cli, [
            'read-meter',
        ])
        mocked_serial.assert_called_with('/dev/ttyUSB0', baudrate=9600, bytesize=7, parity='E', stopbits=1.0, xonxoff=False, timeout=10)
        self.assertEqual(result.exit_code, 1)

    @mock.patch('serial.Serial')
    def test_cli_custom_options(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET.splitlines(True)
        runner = CliRunner()
        result = runner.invoke(cli, [
            'read-meter',
            '--serial-port', '/foo/bar',
            '--serial-baudrate', '115200',
            '--serial-bytesize', '8',
            '--serial-parity', 'N',
            '--serial-stopbits', '2',
            '--serial-timeout', '5',
            '--serial-xonxoff'
        ])
        mocked_serial.assert_called_with('/foo/bar', baudrate=115200, bytesize=8, parity='N', stopbits=2.0, xonxoff=True, timeout=5)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('serial.Serial')
    def test_cli_raw(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET.splitlines(True)
        runner = CliRunner()
        result = runner.invoke(cli, [
            'read-meter',
            '--raw',
        ])
        mocked_serial.assert_called_with('/dev/ttyUSB0', baudrate=9600, bytesize=7, parity='E', stopbits=1.0, xonxoff=False, timeout=10)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('serial.Serial')
    def test_cli_all_output(self, mocked_serial):
        mocked_serial.return_value.readline.side_effect = NORMAL_PACKET.splitlines(True)
        runner = CliRunner()
        result = runner.invoke(cli, [
            'read-meter',
            '--tsv',
            '--show-output=time',
            '--show-output=kwh_eid',
            '--show-output=gas_eid',
            '--show-output=consumed',
            '--show-output=tariff',
            '--show-output=gas_measured_at',
            '--show-output=produced',
            '--show-output=current',
        ])
        mocked_serial.assert_called_with('/dev/ttyUSB0', baudrate=9600, bytesize=7, parity='E', stopbits=1.0, xonxoff=False, timeout=10)
        self.assertEqual(result.exit_code, 0)
