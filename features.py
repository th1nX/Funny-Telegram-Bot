import sqlite3


with sqlite3.connect('database.db') as cursor:
        command = """
        CREATE TABLE IF NOT EXISTS text (Id INTEGER PRIMARY KEY, 'Текст' TEXT);
        """
        cursor.execute(command)
class db:
    def __init__(self, number, id, name, status, count): # string, int, string, string, int
        self.number = number
        self.id = id
        self.name = name
        self.status = status
        self.count = count

    def insert_canal(number, id, name, status, count):
        with sqlite3.connect('database.db') as cursor:
            command = """
            INSERT OR REPLACE INTO tgcanals(id, 'ID Группы', 'Название группы', 'Статус', 'Кол-во участников')
            VALUES
            (?, ?, ?, ?, ?);
            """
            cursor.execute(command, (number, id, name, status, count))

    def del_canal_by_id(id):
        with sqlite3.connect('database.db') as cursor:
            command = """
            DELETE FROM tgcanals WHERE "ID Группы" = ?;
            """
            return cursor.execute(command, (id,))

    def del_canal_by_name(name):
        with sqlite3.connect('database.db') as cursor:
            command = """
            DELETE FROM tgcanals WHERE "Название группы" = ?;
            """
            return cursor.execute(command, (name,))

    def get_count_by_name(name):
        with sqlite3.connect('database.db') as cursor:
            command = """
            SELECT "Кол-во участников" FROM tgcanals WHERE "Название группы" = ?;
            """
            return cursor.execute(command, (name,)).fetchone()[0]

    def get_count_by_id(id):
        with sqlite3.connect('database.db') as cursor:
            command = """
            SELECT "Кол-во участников" FROM tgcanals WHERE "ID Группы" = ?;
            """
            return cursor.execute(command, (id,)).fetchone()[0]

    def get_all_id():
        with sqlite3.connect('database.db') as cursor:
            command = """
            SELECT "ID Группы" FROM tgcanals;
            """
            ids = []
            for i in cursor.execute(command).fetchall():
                ids.append(int(i[0]))
            return ids
    def update_text(id, text):
        with sqlite3.connect('database.db') as cursor:
            command = """
            INSERT OR REPLACE INTO text(Id, 'Текст')
            VALUES
            (?, ?);
            """
            cursor.execute(command, (id, text,))

    def get_text(id):
        with sqlite3.connect('database.db') as cursor:
            command = """
            SELECT "Текст" FROM text WHERE "Id" = ?;
            """
            return cursor.execute(command, (id,)).fetchone()[0]

    def create_db(self):
        with sqlite3.connect('database.db') as cursor:
                command = """
                CREATE TABLE IF NOT EXISTS tgcanals (Id INTEGER PRIMARY KEY, 'ID Группы' TEXT, 'Название группы' TEXT, 'Статус' TEXT, 'Кол-во участников' INTEGER);
                """
                cursor.execute(command)

