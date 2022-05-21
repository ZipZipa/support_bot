import logging
import sqlite3 as sq

base = sq.connect('sqlite_python.db')
cur = base.cursor()

class Tree:
    def __init__(self, name, id):
        self.name = name
        self.child = []
        self.id = id

    def addNode(self, child, parentName, id):
        if ((self.name == parentName) and (self.id != id)):
            self.child.append(child)
        for i in self.child:
            i.addNode(child, parentName, id)

    def output(self,level):
        buff = ""
        if level > 1:
            buff += "┕━"
        if level == 1:
            buff += "┣━"
        for i in range(0,level,1):
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
        return  buff

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
    q=f'SELECT title,last FROM main_pages WHERE level like ("{int(i)}%")'
    cur.execute(q)
    all_menu = cur.fetchall()
    return(all_menu)



#def all_menu2(array, level):
#    if not array[level]


def menu3():
        q = f'select title,level, next_level from main_pages order by level'
        cur.execute(q)
        menu3 = cur.fetchall()
        root = Tree("Root", -1)
        for i in menu3:
            for j in menu3:
                if i[1] == 0:
                    root.addNode(Tree(i[0], i[1]), "Root", j[1])
                    break
                if i[1] == j[2]:
                    root.addNode(Tree(i[0], i[1]), j[0], i[1])
        return (root.output(0))
