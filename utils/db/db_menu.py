import logging
import sqlite3 as sq
import datetime
import time

base = sq.connect('sqlite_python.db')
cur = base.cursor()


class Tree:
    def __init__(self, name, id):
        self.name = name
        self.child = []
        self.id = id

    def add_node(self, child, parent_name, id):
        if ((self.name == parent_name) and (self.id != id)):
            self.child.append(child)
        for i in self.child:
            i.add_node(child, parent_name, id)

    def output(self, level):
        buff = ""
        if level > 1:
            buff += "┕━"
        if level == 1:
            buff += "┣━"

        for _ in range(0, level, 1):
            if level == 1:
                break
            buff = "   " + buff
        buff += " " + self.name + "\n"
        for i in self.child:
            buff += i.output(level + 1)
        if level == 1:
            return buff
        return "┃" + buff
        if level == 0:
            return buff
        return buff


def get_stage1(sql):
    logging.info(f'Recived sql: {sql}')
    cur.execute(sql)

    types = cur.fetchall()
    logging.info(f'Data SQL. Pass the parametr categories {types}')
    return (types)


def add_user(usr, usr_full_name):
    try:
        logging.info(f'Adding {usr}, {usr_full_name} in db')
        sql = ('INSERT or IGNORE INTO users (user_id, subsribe, usr_full_name)'
               + f' VALUES ({usr},false,"{usr_full_name}")')
        cur.execute(sql)
        logging.info('Done')
        base.commit()
    except sq.Error as error:
        logging.info("Ошибка", error)


def all_users():
    try:
        cur.execute('SELECT * FROM users')
        cur_all = cur.fetchall()
        return(cur_all)
    except sq.Error as error:
        logging.info("Ошибка", error)


def all_menu(i):
    sql = f'SELECT title,last FROM main_pages WHERE level like ("{int(i)}%")'
    cur.execute(sql)
    all_menu = cur.fetchall()
    return (all_menu)


# def all_menu2(array, level):
#    if not array[level]


def menu3():
    sql = 'select title,level, next_level from main_pages order by level'
    cur.execute(sql)
    menu3 = cur.fetchall()
    root = Tree("Root", -1)
    for i in menu3:
        for j in menu3:
            if i[1] == 0:
                root.add_node(Tree(i[0], i[1]), "Root", j[1])
                break
            if i[1] == j[2]:
                root.add_node(Tree(i[0], i[1]), j[0], i[1])
    return (root.output(0))


# Добавление кнопки в бд передаем параметры
# /текушего ур./ Текста кнопки/ Пред.Ур
# ИД след уровня генерится по юникс времени в genLevel
def add_button(pre_level, level, btn_type, rez_id, btn_header, btn_text):
    sql_button = ('INSERT INTO main_pages '
                  '(last, title, level, next_level, '
                  'rez_page_id, visebiliti, previous_level) '
                  'VALUES '
                  f'({btn_type}, "{btn_header}", {level}, '
                  f'{rez_id}, {rez_id}, 1, {pre_level}); ')
    print(sql_button)
    cur.execute(sql_button)
    base.commit()
    if btn_text is not None:
        sql_rez_pages = ('INSERT INTO rez_pages '
                         '(text, index_r) '
                         'VALUES '
                         f'("{btn_text}", {rez_id})')
        cur.execute(sql_rez_pages)
        base.commit()


def gen_level():
    present_date = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(present_date)
    # print(int(unix_timestamp))
    print(int(unix_timestamp) % 10000000)
    return int(unix_timestamp % 10000000)

# Функция получения пачки tgId по группе подписки
def get_subscribers(subGroup):
    try:
        cur.execute(f'SELECT user_Id FROM users WHERE groups like ("%{subGroup}%")')
        cur_all = cur.fetchall()
        if len(cur_all) == 0:
            logging.info(f'[get_subscribers] Нет подписчиков для группы: "{subGroup}"')
            return 0
        return cur_all
    except sq.Error as error:
        logging.info('[get_subscribers] Ошибка', error)
