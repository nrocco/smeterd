from smeterd import __version__
from pycli_tools.parsers import get_argparser

from smeterd.cli.read_meter import ReadMeterCommand


def parse_and_run(args=None):
    parser = get_argparser(
        prog='smeterd',
        version=__version__,
        arguments=args,
        logging_format='[%(asctime)-15s] %(levelname)s %(message)s',
        description='Read smart meter P1 packets'
    )

    parser.add_commands([
        ReadMeterCommand(),
    ])

    args = parser.parse_args(args)

    return args.func(args, parser=parser)
