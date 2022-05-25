import sqlite3


def sql_dara_lowder(cursor):
    # Удалить таблицу
    cursor.execute('DROP TABLE IF EXISTS main_pages')
    cursor.execute('DROP TABLE IF EXISTS rez_pages')
    # создать таблицу
    data1 = """
    CREATE TABLE IF NOT EXISTS  main_pages  (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    last BOOLEAN,
    level INTEGER,
    next_level INTEGER,
    rez_page_id INTEGER,
    visebiliti BOOLEAN  NOT NULL DEFAULT true);
    """
    cursor.execute(data1)
    data2 = """

    CREATE TABLE IF NOT EXISTS  rez_pages  (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    index_r INTEGER);
    """
    cursor.execute(data2)

    # наполнеие таблицы
    data3 = """
    INSERT INTO
        main_pages (title, last, level, next_level, visebiliti, rez_page_id)
    VALUES
    ('EФС', false , 0, 1 , true , 1),
        ('Новый канал', false , 1, 2 , true , 1),
            ('Общая информация', true , 2, 2 , true , 0),
            ('Есть роблема',      false , 2, 0 , true , 1),

        ('Точки подключения', false , 1, 4 , true , 1),
            ('ПСИ', false , 4, 0 , true , 1),
            ('ПРОМ', false , 4, 0 , true , 1),
            ('ИФТ', false , 4, 0 , true , 1),
            ('НТ', false , 4, 0 , true , 1),

        ('Есть роблема', false , 1, 6 , true , 1),
            ('MQ', false , 6, 0 , true , 1),
            ('DPM', false , 6, 0 , true , 1),
            ('БД', false , 6, 0 , true , 1),
            ('Piline', false , 6, 0 , true , 1),
            ('СУП', false , 6, 0 , true , 1),
            ('OSE', false , 6, 0 , true , 1),
            ('Istio', false , 6, 0 , true , 1),
            ('Нечто другое', false , 6, 0 , true , 1),
            ('Парам-пам', false , 6, 0 , true , 1),
    ('ППРБ', false , 0, 5, true , 1),
        ('Есть роблема', true , 5, 1, false , 1)
    ;
    """
    cursor.execute(data3)
    data4 = """
    INSERT INTO rez_pages (text, index_r)
    VALUES
    ('hhhhhhhh' , 1),
    ('TExt response' , 2);
    """
    cursor.execute(data4)


try:
    connection = sqlite3.connect('sqlite_python.db')
    cursor = connection.cursor()
    sql_dara_lowder(cursor)

    sqlite_select_query = 'SELECT *  FROM main_pages WHERE level = 0;'
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("rezal ", record)
    connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
