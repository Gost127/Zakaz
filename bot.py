
import telebot
import sqlite3
from aiogram import  Bot,Dispatcher,types
from aiogram.types.web_app_info import WebAppInfo

name = None
klass = None
oo = None

bot = telebot.TeleBot('6483712057:AAEe6E3WsKWAVOQtgrKAUyWbfLnaGrzpnB8')

@bot.message_handler(commands=['start'])
def start(message):
    conn =sqlite3.connect("school.sql")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), klass varchar(50), oo varchar(50), points varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    
    bot.send_message(message.chat.id, "Введите ваше ФИО")
    bot.register_next_step_handler(message, user_name)
    
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш класс')
    bot.register_next_step_handler(message, user_klass)
def user_klass(message):
    global klass
    klass = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш ОО')
    bot.register_next_step_handler(message, user_oo)
def user_oo(message):
    global oo
    oo = message.text.strip()
    bot.send_message(message.chat.id, 'Введите количество баллов')
    bot.register_next_step_handler(message, user_points)
def user_points(message) :
    points = message.text.strip()
    conn =sqlite3.connect("school.sql")
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, klass, oo, points) VALUES ("%s", "%s", "%s", "%s")' % (name, klass, oo, points))
    conn.commit()
    cur.close()
    conn.close()

    # bot.send_message(message.chat.id, 'Вот ссылка на список пользователей', reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    conn = sqlite3.connect('school.sql')

    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    
    users = cur.fetchall()
    
    info = ''
    for el in users:
        info += f'ФИО: {el[1]}, Класс: {el[2]}, ОО: {el[3]}, Баллы: {el[3]}\n'
    
    bot.send_message(call.message.chat.id, info)
    
    cur.close()
    conn.close()

async def user_points(message= types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.keyboard_button("Открыть сайт", web_app=WebAppInfo(url="https://www.youtube.com/watch?v=y65BZbNB0YA&list=LL&index=23")))
    await message.answer("Вот сайт", reply_markup=markup)

bot.infinity_polling()