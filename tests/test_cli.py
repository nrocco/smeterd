import mock

from smeterd.cli import parse_and_run

@mock.patch('smeterd.cli.read_meter.SmartMeter')
@mock.patch('smeterd.cli.read_meter.ReadMeterCommand')
def test_cli_default_options(mocked_command, mocked_meter):
    foo = parse_and_run(['read-meter', '--serial-port', '/foo/bar'])

    print(mocked_command.run)
    print(mocked_command.call_args)
    print(mocked_command.run.call_count)

    #assert mocked_command.run.call_args[0][0]['serial_port'] == '/foo/bar'

    assert 0 == foo
