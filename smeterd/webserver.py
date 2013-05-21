from bottle import Bottle, response, run, jinja2_template as template
from bottle_sqlite import SQLitePlugin

from smeterd import storage
from smeterd import utils


app = Bottle()


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

##
#########################################################################
#########################################################################
##

@app.route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index(db):
    data = db.execute('SELECT * FROM data ORDER BY date DESC LIMIT 1').fetchone()
    return template('active_usage', data=data)


@app.route('/report', method='GET') #, apply=[catch_exceptions])
def report(db, period='daily'):
    result = storage.generate_report(db)
    return template('daily_report', data=result)


@app.route('/report/<period>', method='GET') #, apply=[catch_exceptions])
def report(db, period):
    result = storage.generate_report(db, type='day', period=period)
    return template('daily_report', data=result)


@app.route('/rrd/total.png', method='GET')
def rrd_image():
    response.content_type = 'image/png'
    return open('kwh.png', 'r').read()


@app.route('/current', method='GET', apply=[respond_in_plaintext])
def current():
    from smeterd.meter import read_one_packet
    return read_one_packet()

##
#########################################################################
#########################################################################
##

def start_webserver(host, port, db, auto_reload=False, debug=True):
    global app
    app.install(SQLitePlugin(dbfile=db))
    run(app=app, host=host, port=port, debug=debug, reloader=auto_reload)
