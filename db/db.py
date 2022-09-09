import sqlite3
import os.path

import os
import string
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
        if len(self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user_data_{self.gid}'").fetchall()) == 0:
            self.create_user_table()
            print ("Таблица пользователь загружена...")
        if len(self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='level_pattern_{self.gid}'").fetchall()) == 0:
            self.create_level_table()
            print ("Таблица пользователь загружена...")

    def create_user_table(self):
        self.con.cursor().execute(f"""
        CREATE TABLE "user_data_{self.gid}" (
            "id"	INTEGER,
            "uid"	TEXT DEFAULT 0,
            "level"	INTEGER DEFAULT 0,
            "xp"	INTEGER DEFAULT 0,
            "level_role"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)

    def create_level_table(self):
        self.con.cursor().execute(f"""
        CREATE TABLE "level_pattern_{self.gid}" (
            "level"	INTEGER,
            "xp"	INTEGER,
            "name"	TEXT,
            "r"	INTEGER DEFAULT 0,
            "g"	INTEGER DEFAULT 0,
            "b"	INTEGER DEFAULT 0,
            "roleid"	TEXT
        );
        """)

        self.con.cursor().execute(f"""INSERT INTO level_pattern_{self.gid} (level,xp,name) VALUES (1,0,'Стандартный')""")
        self.con.commit()

        pass

    # Обновление роли для уровня
    def update_roleid_on_table(self,level:int, roleid:string ):
        self.cur.execute(f"UPDATE level_pattern_{self.gid} SET roleid={roleid} WHERE level={level}")
        self.con.commit()
    ####SETS
    def set_level(self, uid: string, level: int):
        self.cur.execute(f"UPDATE user_data_{self.gid} SET level={level} WHERE uid={uid}")
        self.con.commit()

    def set_xp(self, uid: string, xp: int):
        self.cur.execute(f"UPDATE user_data_{self.gid} SET xp={xp} WHERE uid={uid}")
        self.con.commit()

    def set_roleid(self, uid: string, roleid: string):
        self.cur.execute(f"UPDATE user_data_{self.gid} SET level_role={roleid} WHERE uid={uid}")
        self.con.commit()
    ####

    ####GETS
    def get_role(self, uid: int):
        return self.cur.execute(f"SELECT level_role FROM user_data_{self.gid} WHERE uid={uid}").fetchall()[0][0]

    def get_level(self, uid: int):
        return self.cur.execute(f"SELECT level FROM user_data_{self.gid} WHERE uid={uid}").fetchall()[0][0]

    def get_xp(self, uid: int):
        return self.cur.execute(f"SELECT xp FROM user_data_{self.gid} WHERE uid={uid}").fetchall()[0][0]

    # Выгрузка уровня и его имени
    def get_level_pattern(self):
        return self.cur.execute(f"SELECT level,name,r,g,b,roleid FROM level_pattern_{self.gid}").fetchall()
    ####


    ####ADD
    # Добавление опыта
    def add_exp(self, uid: string, xp: int):
        self.cur.execute(f"UPDATE user_data_{self.gid} SET xp=xp+{xp} WHERE uid={uid}")
        level_up = self.check_user_level(uid) #возвращает bool повысился уровень или нет
        self.con.commit()
        print(f"Пользваотелю {uid} с сервера {self.gid} добавлено {xp} опыта")
        return level_up

    # Добавление уровня
    def add_level(self, uid: string, level: int):
        self.cur.execute(f"UPDATE user_data_{self.gid} SET level=level+{level} WHERE uid={uid}")
        self.set_xp(uid,0)
        self.con.commit()

        change_role = self.check_user_level(uid) #возвращает bool (надо обновлять роль или нет)
        print(f"Пользваотелю {uid} с сервера {self.gid} добавлен {level} уровнь")
        return change_role
    ####


    ####CHECKS
    # Проверка, есть ли пользователь в базе
    # Если нет, то добавить и назначить роль
    def check_newbie_user(self,uid: string):
        data = self.cur.execute(f"SELECT id FROM user_data_{self.gid} WHERE uid={uid}").fetchall()
        if len(data) == 0:          
            roleid = self.requeried_roleid(level=1)  
            self.cur.execute(f"INSERT INTO user_data_{self.gid} (uid,level_role) VALUES ({uid},{roleid})")
            self.con.commit()
            print(f"пользваотель с id {uid} с сервера {self.gid} добавлен в базу")
            return roleid
        return None

    
    # Проверка соответствия уровня опыту
    # Если достаточно опытна для поднятия уровня, TRUE
    def check_user_level(self, uid: string):
        xp = self.get_xp(uid)
        level = self.get_level(uid)
        if xp >= 1000:
            self.add_level(uid, 1)
            return True
        return False

    def check_role(self, uid):
        requeried_roleid = self.requeried_roleid(self.get_level(uid))
        if self.get_role(uid) != requeried_roleid:
            print(f"Для {uid} требуется обновление роли на {requeried_roleid}")
            return requeried_roleid
        return None
    ###

    # Роль соотвутствующая уровню
    def requeried_roleid(self, level: int):
        return self.cur.execute(f"SELECT roleid FROM level_pattern_{self.gid} WHERE level<={level} ORDER BY level DESC LIMIT 1").fetchall()[0][0]
    