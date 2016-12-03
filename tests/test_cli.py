import mock
from smeterd.cli import parse_and_run


@mock.patch('smeterd.cli.read_meter.SmartMeter')
def test_cli_default_options(mocked_meter):
    result = parse_and_run(['read-meter'])

    assert mocked_meter.call_args[0][0] == '/dev/ttyUSB0'
    assert mocked_meter.call_args[1]['baudrate'] == 9600
    assert mocked_meter.call_args[1]['bytesize'] == 7
    assert mocked_meter.call_args[1]['parity'] == 'E'
    assert mocked_meter.call_args[1]['stopbits'] == 1
    assert mocked_meter.call_args[1]['timeout'] == 10
    assert mocked_meter.call_args[1]['xonxoff'] == False

    assert 0 == result


@mock.patch('smeterd.cli.read_meter.SmartMeter')
def test_cli_custom_options(mocked_meter):
    result = parse_and_run([
        'read-meter',
        '--serial-port', '/foo/bar',
        '--serial-baudrate', '115200',
        '--serial-bytesize', '8',
        '--serial-parity', 'N',
        '--serial-stopbits', '2',
        '--serial-timeout', '5',
        '--serial-xonxoff'
    ])

    assert mocked_meter.call_args[0][0] == '/foo/bar'
    assert mocked_meter.call_args[1]['baudrate'] == 115200
    assert mocked_meter.call_args[1]['bytesize'] == 8
    assert mocked_meter.call_args[1]['parity'] == 'N'
    assert mocked_meter.call_args[1]['stopbits'] == 2
    assert mocked_meter.call_args[1]['timeout'] == 5
    assert mocked_meter.call_args[1]['xonxoff'] == True

    assert 0 == result


@mock.patch('smeterd.cli.read_meter.SmartMeter')
def test_cli_legacy_options(mocked_meter):
    result = parse_and_run([
        'read-meter',
        '--baudrate', '115200',
    ])

    assert mocked_meter.call_args[1]['baudrate'] == 115200

    assert 0 == result
