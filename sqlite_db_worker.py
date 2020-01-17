import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('sqlite_users.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            text        TEXT NOT NULL
        )
    ''')

    # Сохранить изменения
    conn.commit()
    #for row in c.execute('SELECT user_id FROM user_message'):
        #print(row[0])


@ensure_connection
def add_message(conn, user_id: int, text: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()


@ensure_connection
def count_messages(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ? LIMIT 1', (user_id, ))
    (res, ) = c.fetchone()
    return res


@ensure_connection
def list_messages(conn, user_id: int, limit: int = 10):
    c = conn.cursor()
    c.execute('SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()

@ensure_connection
def delete_message(conn, user_id: int):
    c = conn.cursor()
    c.execute('DELETE FROM user_message WHERE user_id = ?', (user_id, ))
    conn.commit()

#функция, которая должна проверять есть переменная в базе или нет
@ensure_connection
def user_id_in_base(conn, user_id: int):
    user_in_base = False
    c = conn.cursor()
    for row in c.execute("SELECT user_id FROM user_message"):
        if row[0] == user_id:
            user_in_base = True
            break
        else:
            user_in_base = False
            print(row[0], user_id)
            continue

    return user_in_base

#функция, которая выводит в цикл весь список пользователей из базы
@ensure_connection
def list_of_user_ids(conn):
    c = conn.cursor()
    c.execute("SELECT user_id FROM user_message")
    return c.fetchall()



if __name__ == '__main__':
    init_db()


