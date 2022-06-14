import datetime
import logging
import sqlite3 as sq

base = sq.connect('sqlite_python.db')
cur = base.cursor()


class Tree:
    def __init__(self, name, level, next, db_id):
        self.name = name
        self.child = []
        self.level = level
        self.next = next
        self.db_id = db_id

    def add_node(self, child, parent_name, level, next, db_id):
        # if ((self.name == parent_name) and (self.db_id != db_id)):
        #     self.child.append(child)
        if ((self.level == -1) and (self.name == parent_name)):
            self.child.append(child)
        if ((self.next == child.level)):
            self.child.append(child)
        for i in self.child:
            i.add_node(child, parent_name, level, next, db_id)

    def find_db_ids(self, db_id):
        if self.db_id == db_id:
            return self
        if self.child != 0:
            for i in self.child:
                i = i.find_db_ids(db_id)
                if i.db_id == db_id:
                    self = i
                    break
        return self

    def output(self, level):
        buff = ""
        if level > 1:
            buff += "┕━"
        if level == 1:
            buff += "┣━"

        for _ in range(level):
            if level == 1:
                break
            buff = f"   {buff}"
        buff += f" {self.name}" + "\n"
        for i in self.child:
            buff += i.output(level + 1)
        if level == 1:
            return buff
        return f"┃{buff}"

    def get_db_ids(self):
        buff = f'\'{self.db_id}\', '

        for i in self.child:
            buff += i.get_db_ids()
        return f"{buff}"


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
        return cur.fetchall()
    except sq.Error as error:
        logging.info("Ошибка", error)


def create_tree():
    sql = ('SELECT title, level, next_level, _id '
           'FROM main_pages ORDER BY level')
    cur.execute(sql)
    draw_tree = cur.fetchall()
    root = Tree("Root", -1, -1, -1)
    for i in draw_tree:
        for j in draw_tree:
            if i[1] == 0:
                root.add_node(Tree(i[0], i[1], i[2], i[3]), "Root", i[1], i[2], i[3])
                break
            if i[1] == j[2]:
                root.add_node(Tree(i[0], i[1], i[2], i[3]), j[0], i[1], i[2], i[3])
    return root
    # Рабочая конфигурация получения всех ойдишников цепочки
    # которую надо удалить

    # return root.find_db_ids(20).get_db_ids()[:-2]


def draw_tree(tree):
    # Рабочая конфигурация получения всех ойдишников цепочки
    # которую надо удалить
    return tree.output(0)


# Добавление кнопки в бд передаем параметры
# /текушего ур./ Текста кнопки/ Пред.Ур
# ИД след уровня генерится по юникс времени в genLevel
def add_button(pre_level, level, btn_type, rez_id, btn_header, btn_text):
    sql_button = ('INSERT INTO main_pages '
                  '(last, title, level, next_level, '
                  'rez_page_id, visebiliti, previous_level) '
                  'VALUES '
                  f"({btn_type}, '{btn_header}', {level}, "
                  f'{rez_id}, {rez_id}, 1, {pre_level}); ')
    print(sql_button)
    cur.execute(sql_button)
    base.commit()
    if btn_text is not None:
        sql_rez_pages = ('INSERT INTO rez_pages '
                         '(text, index_r) '
                         'VALUES '
                         f"('{btn_text}', {rez_id})")
        cur.execute(sql_rez_pages)
        base.commit()


def delete_button(btn_id):
    try:
        cur.execute('DELETE FROM main_pages WHERE _id IN '
                    f'({create_tree().find_db_ids(btn_id).get_db_ids()[:-2]})')
        base.commit()
    except sq.Error as error:
        logging.info("Ошибка", error)


def show_delete(db_ids):
    return create_tree().find_db_ids(db_ids)


def gen_level():
    present_date = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(present_date)
    # print(int(unix_timestamp))
    print(int(unix_timestamp) % 10000000)
    return int(unix_timestamp % 10000000)
