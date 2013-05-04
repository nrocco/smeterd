from subprocess import check_output

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






@route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index(db):
    return check_output(['bin/report.sh'])


def start_webserver(host, port, auto_reload=False):
    DBNAME = 'smeter.sqlite'
    install(SQLitePlugin(dbfile=DBNAME))
    run(host=host, port=port, reloader=auto_reload)
