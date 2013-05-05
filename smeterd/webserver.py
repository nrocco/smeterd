from bottle import route, run, response, request, install
#from bottle_sqlite import SQLitePlugin

from smeterd import storage
from smeterd import utils



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
def index():
    data = storage.generate_report(DBNAME)
    return utils.dictionary_list_to_plaintext_table(data)


DBNAME = ''

def start_webserver(host, port, db, auto_reload=False):
    #install(SQLitePlugin(dbfile=DBNAME))
    global DBNAME
    DBNAME = utils.get_absolute_path(db)
    run(host=host, port=port, reloader=auto_reload)

