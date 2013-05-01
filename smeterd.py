#!/usr/bin/env python

import random
from datetime import datetime

from libs.bottle import route, run, response, request, install
from libs.bottle_sqlite import SQLitePlugin



def catch_exceptions(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            response.status= 400
            return '%s: %s\n' % (type(e).__name__, str(e))
    return wrapper


def respond_in_plaintext(fn):
    def wrapper(*args, **kwargs):
        response.content_type = 'text/plain; charset="UTF-8"'
        return fn(*args, **kwargs)
    return wrapper


#
##############################################################################
##############################################################################
#


@route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index(db):
    from subprocess import check_output
    return check_output(['bin/report.sh'])




#
##############################################################################
##############################################################################
#


if '__main__' == __name__:
    import sys
    import os
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Smeter App')
    parser.add_argument('-b', '--bind', metavar='address:port',
                        default='0.0.0.0:8000', help='Inet socket to bind to')
    parser.add_argument('-r', '--reload',
                        action='store_true', help="Auto respawn server")
    args = parser.parse_args()

    parts = args.bind.split(':')
    host = parts[0]
    port = parts[1] if len(parts) > 1 else 8000

    DBNAME = 'smeter.sqlite'
    install(SQLitePlugin(dbfile=DBNAME))
    run(host=host, port=port, reloader=args.reload)
