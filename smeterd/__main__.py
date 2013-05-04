import sys
import os
from argparse import ArgumentParser

parser = ArgumentParser(description='Smeter App')
parser.add_argument('-b', '--bind', metavar='address:port',
                    default='0.0.0.0:8000', help='Inet socket to bind to')
parser.add_argument('-r', '--auto-reload',
                    action='store_true', help="Auto respawn server")
args = parser.parse_args()

parts = args.bind.split(':')
host = parts[0]
port = parts[1] if len(parts) > 1 else 8000

from smeterd import webserver
webserver.start_webserver(host, port, auto_reload=args.auto_reload)
