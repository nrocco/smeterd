import sqlite3

SQL_SCHEMA_CREATE = '''CREATE TABLE IF NOT EXISTS data (date TEXT UNIQUE, kwh1 INTEGER, kwh2 INTEGER, gas INTEGER)'''
SQL_INSERT_DATA = '''INSERT INTO data VALUES(?,?,?,?)'''
SQL_DAILY_RESULTS = '''SELECT DATE(date) AS 'date',
((MAX(kwh1)-MIN(kwh1))+(MAX(kwh2)-MIN(kwh2)))*1.0/1000 AS 'total_kwh',
(MAX(gas)-MIN(gas))*1.0/1000 AS 'total_gas',
MAX(kwh1)*0.001 as 'kwh1',
MAX(kwh2)*0.001 as 'kwh2',
MAX(gas)*0.001 as 'gas'
FROM data
GROUP BY DATE(date)'''



def store_single_packet(dbfile, packet):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute(SQL_SCHEMA_CREATE)
    c.execute(SQL_INSERT_DATA, (packet.date,
                                int(packet.kwh1 * 1000),
                                int(packet.kwh2 * 1000),
                                int(packet.gas * 1000)))
    conn.commit()
    conn.close()


def generate_report(dbfile):
    conn = sqlite3.connect(dbfile)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    _result = [r for r in c.execute(SQL_DAILY_RESULTS)]
    conn.close()
    return _result


def get_all_data(dbfile):
    conn = sqlite3.connect(dbfile)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    _result = [r for r in c.execute('SELECT * FROM data')]
    conn.close()
    return _result

