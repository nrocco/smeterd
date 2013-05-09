from bottle import route, run, response, request, install, template
from bottle_sqlite import SQLitePlugin

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





TABLE_TPL = '''<style>body { font-family: monospace; }</style>
<table width="100%">
<tr>
%for header in result[0].keys():
    <th style="text-align:left;">{{header}}</td>
%end
<tr/>
%for row in result:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>'''


@route('/', method='GET', apply=[catch_exceptions])
def index(db):
    data = storage.generate_report(db)
    if len(data) == 0:
        return ''
    return template(TABLE_TPL, result=data)

@route('/current', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def current():
    from smeterd.meter import read_one_packet
    return read_one_packet()



def start_webserver(host, port, db, auto_reload=False):
    db = utils.get_absolute_path(db)
    install(SQLitePlugin(dbfile=db))
    run(host=host, port=port, reloader=auto_reload)

