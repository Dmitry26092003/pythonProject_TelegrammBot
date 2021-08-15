from telebot import types
import random
import config
import datetime


# Регистрация
class BotFun:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db


class Reg(BotFun):
    def reg(self, message):
        user_id = message.from_user.id
        if "NULL" not in self.db.get_user_entry(user_id):
            self.bot.send_message(user_id, f"{self.db.get_user_entry(user_id)[6]}, "
                                           f"Вы уже зарегистрированны в боте и можете пользоваться всеми стандартными "
                                           f"функциями")
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, 'Ты уверен, что хочешь начать?', reply_markup=keyboard)
            self.bot.register_next_step_handler(message, self.platform)

    def platform(self, message):
        if message.text.lower() in ['no', 'нет']:
            return
        user_id = message.from_user.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Приморский, 63", "Энгельса, 23"]
        keyboard.add(*buttons)
        self.bot.send_message(user_id, 'И так... Да начнется "Регистрация"')
        self.bot.send_message(user_id, 'С какой ты площадки?', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.department)

    def department(self, message):
        user_id = message.from_user.id
        self.db.update_platform_user(user_id, message.text)
        self.bot.send_message(user_id, "С какого ты отделения?", reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.group_number)

    def group_number(self, message):
        user_id = message.from_user.id
        self.db.update_department_user(user_id, message.text)
        self.bot.send_message(user_id, "Какой у тебя номер группы?")
        self.bot.register_next_step_handler(message, self.date_of_birth)

    def date_of_birth(self, message):
        user_id = message.from_user.id
        self.db.update_group_number_user(user_id, message.text)
        self.bot.send_message(user_id, "Когда ты родилcя? (ОТВЕТ В ФОРМАТЕ ДД:ММ:ГГГГ)")
        self.bot.register_next_step_handler(message, self.gender)

    def gender(self, message):
        user_id = message.from_user.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["М", "Ж"]
        keyboard.add(*buttons)
        self.db.update_date_of_birth_user(user_id, message.text)
        self.bot.send_message(user_id, 'Ты Парень или Девушка? (ОТВЕТ В ФОРМАТЕ "М"/"Ж")', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.name)

    def name(self, message):
        user_id = message.from_user.id
        self.db.update_gender_user(user_id, message.text)
        self.bot.send_message(user_id, 'Как тебя зовут? (ПОЛНОЕ ИМЯ)', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.surname)

    def surname(self, message):
        user_id = message.from_user.id
        self.db.update_name_user(user_id, message.text)
        self.bot.send_message(user_id, 'Какая у тебя фамилия?')
        self.bot.register_next_step_handler(message, self.tel)

    def tel(self, message):
        user_id = message.from_user.id
        self.db.update_surname_user(user_id, message.text)
        self.bot.send_message(user_id, 'Твой номер телефона в формате +7(XXX) XXX XX-XX')
        self.bot.register_next_step_handler(message, self.email)

    def email(self, message):
        user_id = message.from_user.id
        self.db.update_tel_user(user_id, message.text)
        self.bot.send_message(user_id, 'И на последок твоя электронная почта')
        self.bot.register_next_step_handler(message, self.reg_end)

    def reg_end(self, message):
        user_id = message.from_user.id
        self.db.update_email_user(user_id, message.text)
        self.bot.send_message(user_id, 'Супер, давай проверим данные')
        date = self.db.get_user_entry(user_id)
        self.bot.send_message(user_id, f'''{date[6]} {date[7]} {date[4]}
        ПОЛ: {date[5]}
        {date[1]}
        {date[2]}
        Группа №{date[3]}
        {date[8]}
        {date[9]}''')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Да", "Нет"]
        keyboard.add(*buttons)
        self.bot.send_message(user_id, 'Все правильно?', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.reg_end_)

    def reg_end_(self, message):
        user_id = message.from_user.id
        if message.text.lower() in ['да', 'yes']:
            self.bot.send_message(user_id, 'Супер)))', reply_markup=types.ReplyKeyboardRemove())
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, 'Хочешь заполнить анкету заново?', reply_markup=keyboard)
            self.bot.register_next_step_handler(message, self.platform)


class Join(BotFun):
    def join(self, message):
        user_id = message.from_user.id
        if "NULL" in self.db.get_user_entry(user_id):
            self.bot.send_message(user_id, 'Перед тем как вступить в СС зарегистрируйтесь в боте (команда /reg)')
            return
        if self.db.get_member_entry(user_id):
            self.bot.send_message(user_id, f"{self.db.get_user_entry(user_id)[6]}, "
                                           f"Вы уже состоите в СС")
            return
        else:
            self.bot.send_message(user_id, 'Чем ты можешь помочь СС? Чем занимаетесь?')
            self.bot.register_next_step_handler(message, self.join_)

    def join_(self, message):
        user_id = message.from_user.id
        self.db.add_member(user_id, message.text)
        self.bot.send_message(user_id, 'Твоя заявка отправлена администрации CC')
        print('member')
        print(self.db.get_admin_member())
        for id in self.db.get_admin_member() + [422633743]:
            print(self.db.get_member_entry(user_id))
            text = f'Привет, {self.db.get_user_entry(id)[6]}. \n ' \
                   f'{self.db.get_user_entry(user_id)[6]} {self.db.get_user_entry(user_id)[7]} хочет' \
                   f' вступить в СС. \n' \
                   f'User_id: {user_id}\n' \
                   f'Родился {self.db.get_user_entry(user_id)[4]}\n' \
                   f'Обучается по адресу {self.db.get_user_entry(user_id)[1]}\n' \
                   f'Отделение {self.db.get_user_entry(user_id)[2]}\n' \
                   f'Группа № {self.db.get_user_entry(user_id)[3]}\n' \
                   f'Чем он может помочь СС, чем занимается\n\n' \
                   f'{self.db.get_member_entry(user_id)[2]}\n\n\n\n' \
                   f'НАпишите !list_new_member чтобы увидеть не расмотренные заявки'
            self.bot.send_message(id, text)
            print(f'send by {id}')
            print(text)


class Admin(BotFun):
    def help_(self, message):
        user_id = message.from_user.id
        print('Выводится список команд для администрации')
        self.bot.send_message(user_id, '''
                    Привет ниже ты увидишь список команд доступных только администрации
                    !help - вывести данное меню))
                    !profile [id|Имя Фамилия] - Открыть профиль пользователя
                    !info [id|Имя Фамилия] - Подробная информация о пользователе бота
                    !list_member - Вывести список всех участников студенческого совета
                    !list_new_member - Вывести список заявок на поступление в СС
                    !event - Редактор мероприятий''')

    def event(self, message):
        user_id = message.from_user.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Создать мероприятие',
                   'Cписок мероприятий',
                   'Редактировать мероприятие',
                   'Удалить мероприятие']
        keyboard.add(*buttons)
        self.bot.send_message(user_id, f'{self.db.get_user_entry(user_id)[6]}, Вы находитесь '
                                       f'в редакторе мероприятий))', reply_markup=keyboard)

    def event_(self, message):
        user_id = message.from_user.id
        if message.text == 'Создать мероприятие':
            self.create_event(message)
        elif message.text == 'Cписок мероприятий':
            self.list_event(message)
        elif message.text == 'Редактировать мероприятие':
            self.update_event(message)
        elif message.text == 'Удалить мероприятие':
            self.del_event(message)

    def create_event(self, message):
        user_id = message.from_user.id
        self.bot.send_message(user_id, 'Введите название ')

    def del_event(self, message):
        user_id = message.from_user.id

    def update_event(self, message):
        user_id = message.from_user.id

    def list_event(self, message):
        user_id = message.from_user.id
        print(f"Выполнен запрос списка Мероприятий пользователем с id {user_id}")
        for i in self.db.get_event_entry(get_all=True):
            id = i[0]
            address = i[1]
            name_event = i[2]
            date_event = i[3]
            time_event = i[4]
            description = i[6]
            participants = i[7]
            required = i[8]
            print(i)
            self.bot.send_message(user_id, f'''
        ID: {id}
        Название: {name_event}
        {date_event} {time_event}
        Адресс: {address}
        
        {description}
        
        Требуются: {required}
        Участники: {participants}
        
        ''')

    def list_member(self, message):
        user_id = message.from_user.id
        print(f"Выполнен запрос списка участников студенческого совета пользователем с id {user_id}")
        for i in self.db.get_user_entry(get_all=True):
            id = i[0]
            platform = i[1]
            department = i[2]
            group_number = i[3]
            date_of_birth = i[4]
            name = i[6]
            surname = i[7]
            tel = i[8]
            email = i[9]
            print(i)
            if self.db.is_member(user_id=id):
                b = self.db.get_member_entry(user_id=id)
                print(b)
                status = b[1]
                post = b[2]
                warning = b[3]
                reprimand = b[4]
                score = b[5]
                self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
Его статус {status}
Чем занимается: {post}
    Выговоры: {warning}
    Предупреждения: {reprimand}
    Балы: {score}''')
            else:
                self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
В студенческом совете не стостоит''')
            print(i)

    def list_new_member(self, message):
        user_id = message.from_user.id
        print(f"Выполнен запрос списка заявок на вступление в СС пользователем с id {user_id}")
        new_member_list = self.db.get_new_member_entry()
        print(f'new_member_list: {new_member_list}')
        if new_member_list == []:
            self.bot.send_message(user_id, 'Заявок на вступление в сс нет')
        else:
            i = new_member_list[0]
            id = i[0]
            i = self.db.get_user_entry(user_id=id)
            platform = i[1]
            department = i[2]
            group_number = i[3]
            date_of_birth = i[4]
            name = i[6]
            surname = i[7]
            tel = i[8]
            email = i[9]
            print("пум")
            print(i)
            b = self.db.get_member_entry(user_id=id)
            print(b)
            post = b[2]
            self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
Чем занимается: {post}''')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["ДА", "НЕТ"]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, 'Хотите принять его в СС?', reply_markup=keyboard)
            self.bot.register_next_step_handler(message, self.list_new_member_)
            self.id = id
            print(i)

    def list_new_member_(self, message):
        user_id = message.from_user.id
        if message.text == "ДА":
            self.db.update_status_member(self.id, "Member")
            self.bot.send_message(user_id, 'Заявка принята', reply_markup=types.ReplyKeyboardRemove())
            self.list_new_member(message=message)
        else:
            self.db.delete_member(user_id=self.id)
            self.bot.send_message(user_id, 'Заявка отклонена', reply_markup=types.ReplyKeyboardRemove())
            self.list_new_member(message=message)

    def info(self, message):
        user_id = message.from_user.id
        id = message.text[6:]
        if len(id.split()) == 2:
            id = self.db.id_user_name(id.split()[0], id.split()[1])
            print(id)
            if id:
                id = id[0][0]
            else:
                self.bot.send_message(user_id, 'Пользователя не существует')
        print(id)
        i = self.db.get_user_entry(user_id=id)
        platform = i[1]
        department = i[2]
        group_number = i[3]
        date_of_birth = i[4]
        name = i[6]
        surname = i[7]
        tel = i[8]
        email = i[9]
        if self.db.is_member(user_id=id):
            b = self.db.get_member_entry(user_id=id)
            status = b[1]
            post = b[2]
            warning = b[3]
            reprimand = b[4]
            score = b[5]
            self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
Его статус {status}
Чем занимается: {post}
    Выговоры: {warning}
    Предупреждения: {reprimand}
    Балы: {score}''')
        else:
            self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
В студенческом совете не стостоит''')

    def profile(self, message):
        self.message = message
        user_id = message.from_user.id
        id = message.text[9:]
        if len(id.split()) == 2:
            id = self.db.id_user_name(id.split()[0], id.split()[1])
            print(id)
            if id:
                id = id[0][0]
            else:
                self.bot.send_message(user_id, 'Пользователя не существует')
        print(id)
        i = self.db.get_user_entry(user_id=id)
        self.id = id
        platform = i[1]
        department = i[2]
        group_number = i[3]
        date_of_birth = i[4]
        name = i[6]
        surname = i[7]
        tel = i[8]
        email = i[9]
        if self.db.is_member(user_id=id):
            b = self.db.get_member_entry(user_id=id)
            status = b[1]
            post = b[2]
            warning = b[3]
            reprimand = b[4]
            score = b[5]
            self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
Его статус {status}
Чем занимается: {post}
    Выговоры: {warning}
    Предупреждения: {reprimand}
    Балы: {score}''')
            self.bot.send_message(user_id, 'Вы находитесь в профиле данного пользователя')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Статус", "Балы", "Предупреждения", "Выговоры", "Написать пользователю", "Выйти из профиля"]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, 'Что вы хотите изменить?', reply_markup=keyboard)
            self.bot.register_next_step_handler(message, self.profile_)
        else:
            self.bot.send_message(user_id, f'''
ID: {id}
Имя: {name} {surname}
Дата рождения: {date_of_birth}
Тлефон: {tel}
E-mail: {email}
Обучается по адрессу {platform} в {department} № группы {group_number}
В студенческом совете не стостоит''')

    def profile_(self, message):
        user_id = message.from_user.id
        print(message.text)
        if message.text == "Статус":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Админ", "Участник СС", "Исключен из СС"]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, 'Выберите статус который хотите присвоить пользователю',
                                  reply_markup=keyboard)
            self.bot.register_next_step_handler(message, self.profile_status)
        elif message.text == "Балы":
            score = self.db.get_member_entry(user_id=self.id)[-1]
            self.bot.send_message(user_id, f'Счет пользователя {score}')
            self.bot.send_message(user_id, 'Напишите сколько дабавить или убрать балов пользователю в формате (+/- X,'
                                           ' где X - количество балов)')
            self.bot.register_next_step_handler(message, self.profile_score)
        elif message.text == "Предупреждения":
            reprimand = self.db.get_member_entry(user_id=self.id)[-2]
            self.bot.send_message(user_id, f'Предупреждения пользователя {reprimand}')
            self.bot.send_message(user_id, 'Напишите сколько дабавить или убрать предувреждений пользователю в формате '
                                           '(+/- X, где X - количество балов)')
            self.bot.register_next_step_handler(message, self.profile_reprimand)
        elif message.text == "Выговоры":
            warning = self.db.get_member_entry(user_id=self.id)[-3]
            self.bot.send_message(user_id, f'Выговоры пользователя {warning}')
            self.bot.send_message(user_id,
                                  'Напишите сколько дабавить или убрать выговоров пользователю в формате (+/- X,'
                                  ' где X - количество балов)')
            self.bot.register_next_step_handler(message, self.profile_warning)
        elif message.text == "Написать пользователю":
            self.bot.send_message(user_id, 'Напишите свое сообщение')
            self.bot.register_next_step_handler(message, self.profile_send_message)
        elif message.text == "Выйти из профиля":
            self.id = None
            self.bot.send_message(user_id, "Вы вышли", reply_markup=types.ReplyKeyboardRemove())

    def profile_status(self, message):
        print("profile_status")
        user_id = message.from_user.id
        if message.text == "Админ":
            self.db.update_status_member(user_id=self.id, date="Admin")
            self.bot.send_message(user_id, f"Пользователю с ID: {self.id} присвоен статус Админ", reply_markup=types.ReplyKeyboardRemove())
            self.profile(message=self.message)
        elif message.text == "Участник СС":
            self.db.update_status_member(user_id=self.id, date="Member")
            self.bot.send_message(user_id, f"Пользователь с ID: {self.id} теперь Участник СС", reply_markup=types.ReplyKeyboardRemove())
            self.profile(message=self.message)
        elif message.text == "Исключен из СС":
            self.db.delete_member(user_id=self.id)
            self.bot.send_message(user_id, f"Пользователь с ID: {self.id} Исключен из СС", reply_markup=types.ReplyKeyboardRemove())

    def profile_score(self, message):
        print("profile_score")
        user_id = message.from_user.id
        print(self.db.get_member_entry(user_id=self.id))
        print(eval(str(self.db.get_member_entry(user_id=self.id)[-1]) + message.text))
        score = eval(str(self.db.get_member_entry(user_id=self.id)[-1]) + message.text)
        print(score)
        self.db.update_score_member(user_id=self.id, date='' + str(score))
        self.bot.send_message(user_id, f'Счет пользователя {score}')
        self.profile(message=self.message)

    def profile_reprimand(self, message):   # не работает
        print("profile_reprimand")
        user_id = message.from_user.id
        print(self.db.get_member_entry(user_id=self.id))
        reprimand = eval(str(self.db.get_member_entry(user_id=self.id)[-2]) + message.text)
        print(reprimand)
        self.db.update_score_member(user_id=self.id, date='' + str(reprimand))
        self.bot.send_message(user_id, f'Предупреждения пользователя {reprimand}')
        self.profile(message=self.message)

    def profile_warning(self, message):   # не работает
        print("profile_warning")
        user_id = message.from_user.id
        print(self.db.get_member_entry(user_id=self.id))
        warning = eval(str(self.db.get_member_entry(user_id=self.id)[-3]) + message.text)
        print(warning)
        self.db.update_score_member(user_id=self.id, date='' + str(warning))
        self.bot.send_message(user_id, f'Выговоры пользователя {warning}')
        self.profile(message=self.message)

    def profile_send_message(self, message):
        user_id = message.from_user.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["ДА", "Изменить", "Отмена"]
        keyboard.add(*buttons)
        self.m = message.text
        self.bot.send_message(user_id, 'Отправить?', reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.profile_send_message_)

    def profile_send_message_(self, message):
        user_id = message.from_user.id
        if message.text == "ДА":
            self.bot.send_message(self.id, f'{self.db.get_user_entry(user_id=user_id)[6]} '
                                           f'{self.db.get_user_entry(user_id=user_id)[7]}: {self.m}')
            self.bot.send_message(user_id, "Сообщение отправленно", reply_markup=types.ReplyKeyboardRemove())
            self.profile(message=self.message)
        elif message.text == "Изменить":
            self.bot.send_message(user_id, "Напишите сообщение")
            self.bot.register_next_step_handler(message, self.profile_send_message)
        elif message.text == "Отмена":
            self.bot.send_message(user_id, 'Отправка отменена', reply_markup=types.ReplyKeyboardRemove())
            self.profile(message=self.message)

    def send_all(self, message):
        pass


class Member(BotFun):
    pass


class Users(BotFun):
    def hello(self, user_id):
        self.bot.send_message(user_id, random.choice(["Приветствую тебя, углеродная форма жизни.",
                                                      "Приветствую мой Гасподин."]))
        self.bot.send_message(user_id, "Чем я могу Вам помочь?")

    def help_(self, user_id):
        self.bot.send_message(user_id, config.help_text)

    def Not_Admin(self, user_id):
        self.bot.send_message(user_id, 'В доступе отказанно')
