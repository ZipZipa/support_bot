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

def add_user(usr,usr_full_name):
    try:
        logging.info(f'Adding {usr}, {usr_full_name} in db')
        q = f'INSERT or IGNORE INTO users (user_id, subsribe, usr_full_name) VALUES ({usr},false,"{usr_full_name}")'
        cur.execute(q)
        logging.info(f'Done')
        base.commit()
    except sq.Error as error:
        logging.info("Ошибка", error)

def all_users():
    try:
        cur.execute('SELECT * FROM users')
        all = cur.fetchall()
        return(all)
    except sq.Error as error:
        logging.info("Ошибка", error)

def all_menu(i):
    q=f'SELECT title FROM main_pages WHERE level like ("{int(i)}%")'
    cur.execute(q)
    all_menu = cur.fetchall()
    return(all_menu)

#def all_menu2(array, level):
#    if not array[level]