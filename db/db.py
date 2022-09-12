import sqlite3
import os.path

import os
import string
from turtle import st
from dotenv import load_dotenv

load_dotenv()



class Database():
    def __init__(self, gid:int):
        self.con = sqlite3.connect(os.getenv("DATABASE_NAME"))
        self.cur = self.con.cursor()
        self.gid = gid

    def close(self):
        self.con.close()

    @staticmethod
    def check_database():
        if (os.path.exists(os.getenv("DATABASE_NAME"))):
            print ("База данных загружена...")
            return True
        return False

    @staticmethod
    def create_database():
        con = sqlite3.connect(os.getenv("DATABASE_NAME"))
        print ("База данных успешно создана и загружена...")
        con.close

    # Проверка, существуют ли таблицы в БД и созданы ли все роли на сервере
    def check_tables(self):
        if len(self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='spy_user_{self.gid}'").fetchall()) == 0:
            self.create_spy_table()
            print ("Таблица наблюдения создана...")

    def create_spy_table(self):
        self.con.cursor().execute(f"""
        CREATE TABLE "spy_user_{self.gid}" (
            "id"	INTEGER,
            "uid"	TEXT DEFAULT 0,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
        pass

    def add_user_to_spy_table(self, uid: string):
        if self.check_spy_user(uid):
            return
        self.cur.execute(f"INSERT INTO spy_user_{self.gid} (uid) VALUES ({uid})")
        self.con.commit()

    def remove_user_from_spy(self, uid: string):
        self.cur.execute(f"DELETE FROM spy_user_{self.gid} WHERE uid={uid}")
        self.con.commit()

    
    def check_spy_user(self, uid: string):
        query = self.cur.execute(f"SELECT * FROM spy_user_{self.gid} WHERE uid={uid}").fetchall()
        if len(query) == 0:
            return False
        return True
