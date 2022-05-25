import logging
import sqlite3 as sq
import time
import datetime

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

        for i in range(0, level, 1):
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

 
#Добавление кнопки в бд передаем параметры /текушего ур./ Текста кнопки/ Пред.Ур
#ИД след уровня генерится по юникс времени в genLevel
def add_question(currLevel, text, prevLevel):
    insQ = f'INSERT INTO main_pages (last,title, level, next_level, rez_page_id, visebiliti, previous_level) ' \
           f'VALUES ("{1}","{text}", "{currLevel}", "{genLevel()}", "{1}", "{1}", "{prevLevel}"); '
    print(insQ)
    cur.execute(insQ)
    base.commit()

    
def gen_level():
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)
    print(int(unix_timestamp))
    return int(unix_timestamp)

