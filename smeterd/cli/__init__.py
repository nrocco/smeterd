import click
import logging

from smeterd import __version__
from .read_meter import read_meter


logging.basicConfig(format='[%(asctime)-15s] %(levelname)s %(message)s')


@click.group()
@click.version_option(version=__version__)
def cli():
    """Read smart meter P1 packets"""
    pass


cli.add_command(read_meter)
