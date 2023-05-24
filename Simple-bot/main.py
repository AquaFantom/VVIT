import telebot
from telebot import types
import datetime
import psycopg2

token = '5999829012:AAEIJCd_bH_3hHHFvqL2GOdsRetJu_gZHik'

bot = telebot.TeleBot(token)

conn = psycopg2.connect(dbname="mtuci_table", host="localhost", user="postgres", password="db_pass",
                        port="5432")
cursor = conn.cursor()

keyboard = types.ReplyKeyboardMarkup()
keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
             "Расписание на следующую неделю")


def week_type():
    today = datetime.date.today()
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        return "Чётная"
    else:
        return "Нечётная"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Выберите опцию.\nЧтобы просмотреть список команд, введите /help.',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def bot_info(message):
    bot.send_message(message.chat.id, '/help - выводит список команд\n/start - запускает бота\n/week - показывает, '
                                      'какая сейчас неделя\n/mtuci - выводит официальный сайт МТУСИ')


@bot.message_handler(commands=['week'])
def week_info(message):
    if week_type() == "Чётная":
        bot.send_message(message.chat.id, "Текущая неделя - четная")
    else:
        bot.send_message(message.chat.id, "Текущая неделя - нечетная")


@bot.message_handler(commands=['mtuci'])
def mtuci_info(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def controller(message):
    if message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]:
        day_answer(message)
    elif message.text == "Расписание на текущую неделю":
        week_answer(message, True)
    elif message.text == "Расписание на следующую неделю":
        week_answer(message, False)
    else:
        bot.send_message(message.chat.id, "Я не понимаю, о чём вы. Пожалуйста, выберите опцию ниже или введите /help "
                                          "для получения списка комманд.", reply_markup=keyboard)


def day_answer(message):
    cursor.execute('''SELECT
                              timetable.day,
                              subject.name AS subject_name,  
                              timetable.room_numb, 
                              timetable.start_time, 
                              teacher.full_name AS teacher_name
                            FROM 
                              timetable 
                              INNER JOIN subject ON timetable.subject = subject.id 
                              INNER JOIN teacher ON timetable.subject = teacher.subject
                            WHERE 
                              timetable.day = %s AND
                              timetable.week = %s
                            ORDER BY 
                                timetable.start_time;''', (message.text.capitalize(), week_type()))
    records = list(cursor.fetchall())
    if records:
        string = f"{records[0][0]}\n"
        for record in records:
            string += f"{record[1]} | {record[2]} | {record[3]} | {record[4]}\n"
        bot.send_message(message.chat.id, string)
    else:
        bot.send_message(message.chat.id, "На сегодня пар нет. Отдыхайте!")


def week_answer(message, current_week=True):
    if current_week:
        w_type = week_type()
    else:
        if week_type() == "Чётная":
            w_type = "Нечётная"
        else:
            w_type = "Чётная"
    string = ""
    for day_type in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]:
        cursor.execute('''SELECT
                                  timetable.day,
                                  subject.name AS subject_name,  
                                  timetable.room_numb, 
                                  timetable.start_time, 
                                  teacher.full_name AS teacher_name
                                FROM 
                                  timetable 
                                  INNER JOIN subject ON timetable.subject = subject.id 
                                  INNER JOIN teacher ON timetable.subject = teacher.subject
                                WHERE
                                  timetable.day = %s AND
                                  timetable.week = %s
                                ORDER BY
                                    timetable.start_time;''', (day_type, w_type))
        records = list(cursor.fetchall())
        if not records:
            continue
        string += f"\n\n{records[0][0]}\n"
        for record in records:
            string += f"{record[1]} | {record[2]} | {record[3]} | {record[4]}\n"
    bot.send_message(message.chat.id, string)


bot.polling(none_stop=True)
