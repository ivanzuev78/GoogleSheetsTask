import asyncio

from database import engine, create_db
from exchange import ExchangeRatio
from telegram_api import bot
from transfer_data import transfer_google_sheet


def main():
    create_db(engine)
    usd_rub = ExchangeRatio("USD")

    loop = asyncio.new_event_loop()
    loop.create_task(
        usd_rub.update_exchange_ratio_task()
    )  # Регулярное обновление курса валют
    loop.create_task(transfer_google_sheet(usd_rub))  # Копирование таблицы в БД
    loop.create_task(bot.polling())  # Телеграм бот
    loop.run_forever()


if __name__ == "__main__":
    main()
