import logging
import sqlite3 as sq


base = sq.connect('sqlite_python.db')
cur = base.cursor()


def get_stage1(sql):
    logging.info(f'Recived sql: {sql}')
    cur.execute(sql)

    types = cur.fetchall()
    logging.info(f'Data SQL. Pass the parametr categories {types}')
    return(types)
