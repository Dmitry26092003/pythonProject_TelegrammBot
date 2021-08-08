import sqlite3


class DataBase:
    def __init__(self, path_db):
        if 'data' not in __import__('os').listdir('.'):
            __import__('os').mkdir('data')

        self.conn = sqlite3.connect(f'data/{path_db}', isolation_level=None, check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute('PRAGMA foreign_key=1')

        # create table users
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY NOT NULL,
        platform TEXT, 
        department TEXT,
        group_number TEXT,
        date_of_birth TEXT,
        gender TEXT,
        name TEXT,
        surname TEXT,
        tel TEXT,
        email TEXT);''')

        # create table member
        cur.execute('''
            CREATE TABLE IF NOT EXISTS member(
            user_id INT PRIMARY KEY NOT NULL,
            status TEXT, 
            post TEXT,
            warning INT,
            reprimand INT,
            score INT);''')

        # create table event
        cur.execute('''
            CREATE TABLE IF NOT EXISTS event(
            id_event INT PRIMARY KEY NOT NULL,
            address TEXT, 
            name_event TEXT,
            date_event TEXT,
            time_event TEXT,
            participants TEXT,
            required TEXT);''')
        cur.close()

    def __del__(self):
        self.conn.close()

    # USSERS

    def add_user(self, user_id) -> bool:
        cur = self.conn.cursor()
        try:
            if not self.is_user(user_id):
                cur.execute("""
                INSERT INTO users 
                VALUES(:user_id, :platform, :department, :group_number, :date_of_birth, :gender, :name, 
                :surname, :tel, :email)""", {
                    "user_id": user_id,
                    "platform": "NULL",
                    "department": "NULL",
                    "group_number": "NULL",
                    "date_of_birth": "NULL",
                    "gender": "NULL",
                    "name": "NULL",
                    "surname": "NULL",
                    "tel": "NULL",
                    "email": "NULL",
                })

                print('Пользователь {} добавлен.'.format(user_id))
            else:
                print('Пользователь {} уже существует!'.format(user_id))
                cur.close()
                return False
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def delete_user(self, user_id) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с id {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""DELETE FROM users
                                           WHERE user_id = :user_id""",
                            {
                                'user_id': user_id
                            })

        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_platform_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET platform = :platform WHERE user_id = :user_id;""", {
                    "platform": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_department_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET department = :department WHERE user_id = :user_id;""", {
                    "department": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_group_number_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET group_number = :group_number WHERE user_id = :user_id;""", {
                    "group_number": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_date_of_birth_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET date_of_birth = :date_of_birth WHERE user_id = :user_id;""", {
                    "date_of_birth": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_gender_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET gender = :gender WHERE user_id = :user_id;""", {
                    "gender": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_name_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET name = :name WHERE user_id = :user_id;""", {
                    "name": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_surname_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET surname = :surname WHERE user_id = :user_id;""", {
                    "surname": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_tel_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET tel = :tel WHERE user_id = :user_id;""", {
                    "tel": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_email_user(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE users SET email = :email WHERE user_id = :user_id;""", {
                    "email": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def is_user(self, user_id) -> bool:
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM users WHERE user_id = :user_id""", {
            'user_id': user_id,
        })
        rez = cur.fetchall()
        cur.close()
        if rez:
            print('user_id существует')
        else:
            print('user_id не существует')
        print(rez)
        return bool(rez)

    def id_user_name(self, name, surname) -> bool:
        cur = self.conn.cursor()
        cur.execute("""SELECT user_id FROM users WHERE name = :name and surname = :surname""", {
            'name': name,
            'surname': surname,
        })
        rez = cur.fetchall()
        cur.close()
        if rez:
            print('пользователь существует')
        else:
            print(f'пользователя с именем {name} {surname} не существует')
        print(rez)
        return rez

    def get_user_entry(self, user_id: str = '', get_all: bool = False) -> list:
        cursor = self.conn.cursor()
        result = []

        if get_all:
            try:
                cursor.execute("""SELECT * FROM users""")
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
        else:
            try:
                cursor.execute("""SELECT * FROM users
                                WHERE user_id = :user_id""",
                                {
                                   'user_id': user_id,
                               })
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
            try:
                result = result[0]
            except IndexError:
                pass
        return result

    # MEMBER

    def add_member(self, user_id, post) -> bool:
        cur = self.conn.cursor()
        try:
            if not self.is_member(user_id):
                cur.execute("""
                        INSERT INTO member 
                        VALUES(:user_id, :status, :post, :warning, :reprimand, :score)""", {
                    "user_id": user_id,
                    "status": "New",
                    "post": post,
                    "warning": "0",
                    "reprimand": "0",
                    "score": "0",
                })
                print('Пользователь {} добавлен.'.format(user_id))
            else:
                print('Пользователь {} уже существует!'.format(user_id))
                cur.close()
                return False
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_status_member(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE member SET status = :status WHERE user_id = :user_id;""", {
                    "status": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_warning_member(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE member SET warning = :warning WHERE user_id = :user_id;""", {
                    "warning": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_reprimand_member(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE member SET reprimand = :reprimand WHERE user_id = :user_id;""", {
                    "reprimand": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def update_score_member(self, user_id, date) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с номером {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""UPDATE member SET score = :score WHERE user_id = :user_id;""", {
                    "score": date,
                    "user_id": user_id,
                })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def delete_member(self, user_id) -> bool:
        cur = self.conn.cursor()
        try:
            exist_entry = self.get_user_entry(user_id)
            if not exist_entry:
                print('Пользователь с id {} не существует!'.format(user_id))
                return False
            else:
                cur.execute("""DELETE FROM member
                                           WHERE user_id = :user_id""",
                            {
                                'user_id': user_id
                            })
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def is_member(self, user_id) -> bool:
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM member WHERE user_id = :user_id and status <> 'New' """, {
            'user_id': user_id,
        })
        rez = cur.fetchall()
        cur.close()
        if rez:
            print('user_id существует')
        else:
            print('user_id не существует')
        print(rez)
        return bool(rez)

    def get_admin_member(self) -> list:
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM member WHERE status = 'Admin'""")
        rez = []
        for i in cur.fetchall():
            rez.append(i[0])
        cur.close()
        return rez

    def get_member_entry(self, user_id: str = '', get_all: bool = False) -> list:
        cursor = self.conn.cursor()
        result = []

        if get_all:
            try:
                cursor.execute("""SELECT * FROM member
                                WHERE status <> 'New' """)
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
        else:
            try:
                cursor.execute("""SELECT * FROM member
                                WHERE user_id = :user_id""",
                                {
                                   'user_id': user_id,
                               })
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
            try:
                result = result[0]
            except IndexError:
                pass
        return result

    def get_new_member_entry(self) -> list:
        cursor = self.conn.cursor()
        result = []
        try:
            cursor.execute("""SELECT * FROM member
                            WHERE status = 'New' """)
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
        else:
            result = cursor.fetchall()
        cursor.close()
        print('Список новых заявок')
        print(result)
        return result

    # EVENT

    def add_event(self, address, name, date, time, users, required):
        cur = self.conn.cursor()
        try:
            cur.execute("""
                            INSERT INTO event 
                            VALUES(:adres, :name_event, :date_event, :time_event, :participants, :required)""", {
                "name_event": address,
                "address": name,
                "date_event": date,
                "time_event": time,
                "participants": users,
                "required": required,
            })
            print('Мероприятие добавлено.')
            cur.close()
        except sqlite3.DatabaseError as error:
            print('Error: ', error)
            cur.close()
            return False
        else:
            cur.close()
            return True

    def get_event_entry(self, event_id: str = '', get_all: bool = False) -> list:
        cursor = self.conn.cursor()
        result = []

        if get_all:
            try:
                cursor.execute("""SELECT * FROM event""")
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
        else:
            try:
                cursor.execute("""SELECT * FROM member
                                WHERE event_id = :event_id""",
                                {
                                   'event_id': event_id,
                               })
            except sqlite3.DatabaseError as error:
                print('Error: ', error)
            else:
                result = cursor.fetchall()
            cursor.close()
            try:
                result = result[0]
            except IndexError:
                pass
        return result
