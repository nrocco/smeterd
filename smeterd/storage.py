import sqlite3



SQL_SCHEMA= '''\
CREATE TABLE IF NOT EXISTS data (
    date TEXT UNIQUE,
    kwh1 INTEGER,
    kwh2 INTEGER,
    gas INTEGER
);'''

SQL_INSERT_PACKET = '''INSERT INTO data VALUES(?,?,?,?);'''

SQL_REPORT = '''\
SELECT
    {group_by} as 'date',
    ((MAX(kwh1) - MIN(kwh1))+(MAX(kwh2) - MIN(kwh2))) as 'kwh_total',
    (MAX(gas) - MIN(gas)) as 'gas_total',
    MIN(kwh1)  as 'kwh1_min',
    MIN(kwh2)  as 'kwh2_min',
    MIN(gas)   as 'gas_min',
    MAX(kwh1)  as 'kwh1_max',
    MAX(kwh2)  as 'kwh2_max',
    MAX(gas)   as 'gas_max'
FROM data
WHERE {where}
GROUP BY {group_by};'''




def get_database(dbfile=':memory:', create=False):
    if type(dbfile) is str:
        db = sqlite3.connect(dbfile)
    else:
        db = dbfile
    db.row_factory = sqlite3.Row

    if create:
        db.execute(SQL_SCHEMA)
        db.commit()
    return db


def store_single_packet(dbfile, packet):
    db = get_database(dbfile)
    db.execute(SQL_INSERT_PACKET, (packet.date,
                                   packet.kwh1_asint(),
                                   packet.kwh2_asint(),
                                   packet.gas_asint()))
    db.commit()


def generate_report(dbfile, type='daily', period=None):
    db = get_database(dbfile)
    if type == 'daily':
        params = {
            'group_by': 'DATE(date)',
            'where':    '1',
        }
    elif type == 'day':
        params = {
            'group_by': 'STRFTIME(\'%H:00\', date)',
            'where':    'DATE(date) = \'%s\'' % period,
        }
    else:
        raise Exception('Type %s not implemented yet.' % type)
    result = db.execute(SQL_REPORT.format(**params))
    return [row for row in result]


def get_all_data(dbfile):
    db = get_database(dbfile)
    return [r for r in db.execute('SELECT * FROM data')]
