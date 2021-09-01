from threading import *
import telebot
from DB import DataBase
import string
from bot_function import *
import json
import datetime

bot = telebot.TeleBot(config.token)
db = DataBase('db.db')
print('Bot Started')
data = [[]]
with open("data\mess.json", "w") as write_file:
    json.dump(data, write_file)


def loop():
    pass


def main():
    def I_do_not_understand(user_id):
        bot.send_message(user_id, "Извини, я тебя не понимаю что ты написал, ты можешь "
                                  "воспользоваться командой /help")
        bot.send_message(user_id, "Sorry, I don't understand what you wrote, you can "
                                  "use the command /help")
        print("Извини, я тебя не понимаю что ты написал, ты можешь "
              "воспользоваться командой /help")
        print("Sorry, I don't understand what you wrote, you can "
              "use the command /help")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        user_id = message.from_user.id
        if not db.is_user(user_id):
            db.add_user(user_id)
        print(message.text)
        mes = message.text.translate(str.maketrans('', '', string.punctuation)).lower().split()
        U = Users(bot, db)
        if (message.text == '/start') or (
                len(config.hello & set(mes)) != 0):
            U.hello(user_id)

        elif message.text == "/help":  # Меню помощи
            U.help_(user_id)

        elif ((user_id in db.get_admin_member()
              ) or user_id == 422633743) and "!" in message.text:  # Комманды для Администрации
            A = Admin(bot, db)
            if '!help' in message.text:
                A.help_(message)

            elif '!event' in message.text:
                A.event(message)

            elif '!list_member' in message.text:
                A.list_member(message)

            elif '!list_new_member' in message.text:
                A.list_new_member(message)

            elif '!info' in message.text:
                A.info(message)

            elif '!profile' in message.text:
                A.profile(message)

            elif '!status' in message.text:
                A.status(message)

            elif ('!create_event' in message.text) or (
                    len({"создать", "мероприятие"} & set(mes)) != 0):
                A.create_event(message)

            elif ('!del_event' in message.text) or (
                    len({"удалить", "мероприятие"} & set(mes)) != 0):
                A.del_event(message)

            elif ('!list_event' in message.text) or (
                    len({"список", "мероприятий"} & set(mes)) != 0):
                A.list_event(message)

            elif ('!update_event' in message.text) or (
                    len({"редактировать", "мероприятие"} & set(mes)) != 0):
                A.update_event(message)

            elif '!send_member' in message.text:
                A.send_member(message)

            elif '!send_all' in message.text:
                A.send_all(message)
            else:
                I_do_not_understand(user_id)
        elif message.text[0] == '!':
            U.Not_Admin(user_id)

        elif (message.text == '/reg') or (  # Регистрация в боте
                len({"зарегистрироваться", "регистрация"} & set(mes)) != 0):
            R = Reg(bot, db)
            R.reg(message=message)

        elif (message.text == '/join') or (  # Вступить в СС
                len({"вступить"} & set(mes)) != 0):
            J = Join(bot, db)
            J.join(message=message)

        else:
            I_do_not_understand(user_id)


if __name__ == '__main__':
    t1 = Thread(target=main)
    t2 = Thread(target=loop)

    t1.start()
    t2.start()

    bot.infinity_polling()

# bot.polling(none_stop=True, interval=0)
