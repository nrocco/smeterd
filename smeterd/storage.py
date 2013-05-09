import sqlite3



SQL_SCHEMA_CREATE = '''CREATE TABLE IF NOT EXISTS data (date TEXT UNIQUE, kwh1 INTEGER, kwh2 INTEGER, gas INTEGER)'''
SQL_INSERT_DATA = '''INSERT INTO data VALUES(?,?,?,?)'''
SQL_DAILY_RESULTS = '''SELECT DATE(date) AS 'date',
((MAX(kwh1)-MIN(kwh1))+(MAX(kwh2)-MIN(kwh2)))*0.001 AS 'total_kwh',
(MAX(gas)-MIN(gas))*0.001 AS 'total_gas',
MAX(kwh1)*0.001 as 'kwh1',
MAX(kwh2)*0.001 as 'kwh2',
MAX(gas)*0.001 as 'gas'
FROM data
GROUP BY DATE(date)'''


def get_database(dbfile):
    if type(dbfile) is str:
        db = sqlite3.connect(dbfile)
    else:
        db = dbfile
    db.row_factory = sqlite3.Row
    return db


def store_single_packet(dbfile, packet):
    db = get_database(dbfile)
    db.execute(SQL_SCHEMA_CREATE)
    db.execute(SQL_INSERT_DATA, (packet.date,
                                 packet.kwh1_asint(),
                                 packet.kwh2_asint(),
                                 packet.gas_asint()))
    db.commit()


def generate_report(dbfile):
    db = get_database(dbfile)
    return [r for r in db.execute(SQL_DAILY_RESULTS)]


def get_all_data(dbfile):
    db = get_database(dbfile)
    return [r for r in db.execute('SELECT * FROM data')]
