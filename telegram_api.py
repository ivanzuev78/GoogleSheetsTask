import asyncio

from telebot.async_telebot import AsyncTeleBot

from config import telegram_token
from database import Session
from db_schema import TelegramUser

bot = AsyncTeleBot(telegram_token)

SUBSCRIBE_SUCCESSFUL = 'Вы успешно подписались на бесполезную рассылку'
ALREADY_SUBSCRIBED = 'Вы уже подписаны'

UNSUBSCRIBE_SUCCESSFUL = 'Вы успешно отписались от бесполезной рассылки'
ALREADY_UNSUBSCRIBED = 'Вы не были подписаны'


@bot.message_handler(commands=['start'])
async def subscribe(message):
    user = message.from_user
    user_id = user.id
    with Session() as session:
        user_from_db = session.query(TelegramUser).filter(
            TelegramUser.user_id == user_id
        )
        user_from_db = user_from_db.all()

        if not user_from_db:
            text = SUBSCRIBE_SUCCESSFUL
            telegram_user = TelegramUser(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
            session.add(telegram_user)
            session.commit()
        else:
            text = ALREADY_SUBSCRIBED

        await bot.send_message(chat_id=user_id, text=text)


@bot.message_handler(commands=['stop'])
async def unsubscribe(message):
    user = message.from_user
    user_id = user.id
    with Session() as session:
        user_from_db = session.query(TelegramUser).filter(
            TelegramUser.user_id == user_id
        )
        user_from_db.all()
        users = user_from_db.all()
        user_from_db.delete()
        session.commit()

    await bot.send_message(chat_id=user_id, text=UNSUBSCRIBE_SUCCESSFUL if users else ALREADY_UNSUBSCRIBED)


if __name__ == '__main__':
    # Для проверки подписки на бота
    loop = asyncio.new_event_loop()
    loop.create_task(bot.polling())
    loop.run_forever()
