import re
import telebot
from datetime import datetime

income = 0
expense = 0
month = datetime.today().month

with open('secret') as f:
    data = f.readlines()
    token = data[0].strip()
    users = [int(i) for i in data[1].split()]
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global income
    global expense
    global month
    if datetime.today().month != month:
        month = datetime.today().month
        income = 0
        expense = 0
    if message.from_user.id in users and 'покупка' in message.text.lower(): # expense
        text = re.findall(r"покупка \d*\.*\d+", message.text.lower())
        try:
            value = sum(abs(float(i.strip().split()[-1])) for i in text)
        except:
            value = 0.0
        expense += value
        bot.send_message(message.from_user.id, f"{value}/{expense}")
    elif message.from_user.id in users and '+' not in message.text and ('-' in message.text or 'налич' in message.text.lower() or 'перевод' in message.text.lower()):     # expense
        values = re.findall(r"[-+]?(?:\d*\.*\d+)", message.text.replace(',', '.'))
        try:
            value = sum(abs(float(i)) for i in values)
        except:
            value = 0.0
        expense += value
        bot.send_message(message.from_user.id, f"{value}/{expense}")
    elif message.from_user.id in users and '-' not in message.text and ('+' in message.text or 'зарплата' in message.text.lower()):            # income
        values = re.findall(r"[-+]?(?:\d*\.*\d+)", message.text.replace(',', '.'))
        try:
            value = sum(abs(float(i)) for i in values)
        except:
            value = 0.0
        income += value
        bot.send_message(message.from_user.id, f"{value}/{income}")
#    elif message.text == '/start':
#        users.append(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")
    for user in users:
        try:
            diff = round(income-expense, 2)
            bot.send_message(user, f'За {month} месяц:\nДоход: {income}, Расход: {expense},\nРазница: {"+" if diff > 0 else ""}{diff}')
        except:
            pass

bot.polling(none_stop=True, interval=0)

