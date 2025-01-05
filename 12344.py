import telebot
import sqlite3
from telebot import types

TOKEN = '7884162208:AAFqqeelbKSvN0tPccvVPELHk9lmDu-LLIg'
name = ''

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def main(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, money TEXT)')
    conn.commit()
    cur.close()
    conn.close()

    bot.reply_to(message, "hello")
    chat_id = message.chat.id
    image_path = r'C:\Users\SEX-машины\Desktop\f491c937-80b9-464f-93e8-e5100e4b30c4.png'

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to site', url="https://example.com")
    btn2 = types.InlineKeyboardButton('Регистрация', callback_data="message_2")
    btn3 = types.InlineKeyboardButton('Количество игроков', callback_data="message_3")

    markup.add(btn1)
    markup.add(btn2, btn3)

    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def Call_button(call):
    chat_id = call.message.chat.id
    image_path = r'C:\Users\SEX-машины\Desktop\f491c937-80b9-464f-93e8-e5100e4b30c4.png'

    if call.data == "message_2":
        bot.send_message(chat_id, "Вы нажали на кнопку Message 2!")
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
            bot.send_message(chat_id, "давай тебя зарагестрирую, введите ваше имя")
            bot.register_next_step_handler(call.message, user_name)  # Передаем call.message, а не chat_id

    elif call.data == "message_3":
        bot.send_message(chat_id, "Вы нажали на кнопку Message 3!")
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''
        for el in users:
            info += f'Имя:{el[1]}, money:{el[2]}\n'

        cur.close()
        conn.close()
        bot.send_message(chat_id, info)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "теперь сколько у вас монеток")
    bot.register_next_step_handler(message, user_money)

def user_money(message):
    money_player = message.text.strip()

    try:
        money_player = int(money_player)
    except ValueError:
        bot.send_message(message.chat.id,"ЕБОНАТ!!!??")
        return
        
    conn = sqlite3.connect("database.sql")
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, money) VALUES (?, ?)', (name, money_player))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id,"вы зареганы")

bot.polling(none_stop=True)
