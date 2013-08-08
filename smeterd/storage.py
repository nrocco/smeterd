import sqlite3



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
    db.execute(SQL_INSERT_PACKET, (packet.date,
                                   packet.kwh1_asint(),
                                   packet.kwh2_asint(),
                                   packet.gas_asint()))
    db.commit()
