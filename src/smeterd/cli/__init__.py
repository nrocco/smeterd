import logging

import click

from .read_meter import read_meter

logging.basicConfig(format="[%(asctime)-15s] %(levelname)s %(message)s")


@click.group()
@click.version_option()
def cli():
    """Read smart meter P1 packets"""


cli.add_command(read_meter)
