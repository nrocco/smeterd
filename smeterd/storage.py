import sqlite3

from datetime import datetime



SQL_SCHEMA= '''CREATE TABLE IF NOT EXISTS data (date TEXT UNIQUE, kwh1 INTEGER, kwh2 INTEGER, gas INTEGER);'''
SQL_INSERT_PACKET = '''INSERT INTO data VALUES(?,?,?,?);'''


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
    kwh1 = int(packet['kwh1_in'] * 1000)
    kwh2 = int(packet['kwh2_in'] * 1000)
    gas = int(packet['gas'] * 1000)
    db.execute(SQL_INSERT_PACKET,
               (datetime.now(), kwh1, kwh2, gas))
    db.commit()
