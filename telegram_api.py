import telebot

from config import telegram_token

bot = telebot.TeleBot(telegram_token)

print('asdf')

chats = [747217883]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.id
    if user not in chats:
        bot.send_message(chat_id=user, text='Вы успешно подписались на бесполезную рассылку')
        chats.append(user)
    else:
        bot.send_message(chat_id=user, text='Вы уже подписаны')


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    user = message.from_user.id
    if user in chats:
        bot.send_message(chat_id=user, text='Вы успешно отписались от бесполезной рассылки')
        chats.remove(user)
    else:
        bot.send_message(chat_id=user, text='Вы не были подписаны')


bot.infinity_polling()
