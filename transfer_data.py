import datetime
import logging
from asyncio import sleep
from typing import Dict, List

from config import GOOGLE_SHEET_NAME, refresh_time_sec
from database import Order, Session
from exchange import ExchangeRatio
from telegram_api import send_notify
from work_with_google import get_data_from_google_sheet, parse_orders_from_sheet


async def save_data_to_db(google_data: Dict[int, Order], usd_rub: ExchangeRatio):
    """
    Сохранение данных в БД и отправка уведомлений
    :param google_data: Обработанные данные с Гугл таблицы
    :param usd_rub: Контейнер с курсом валюты
    """
    with Session() as session:
        all_orders_numbs = set(google_data.keys())

        # Ищем записи для обновления
        orders_to_update = (
            session.query(Order).filter(Order.order_numb.in_(all_orders_numbs)).all()
        )
        update_orders(orders_to_update, google_data, usd_rub)

        # Добавляем новые записи в БД
        orders_to_update_numbs = {order.order_numb for order in orders_to_update}
        new_orders_numbs = all_orders_numbs - orders_to_update_numbs
        new_orders = create_new_orders(
            session,
            [
                row
                for order_numb, row in google_data.items()
                if order_numb in new_orders_numbs
            ],
            usd_rub,
        )

        # Удаляем удаленные записи из БД, которых нет в Гугл таблицах
        delete_orders(all_orders_numbs, session)

        # Посылаем уведомления по просроченным заказам
        await check_delivery_deadline(new_orders + orders_to_update)

        session.commit()


def delete_orders(all_orders_numbs, session):
    orders_to_delete_query = session.query(Order).filter(
        Order.order_numb.not_in(all_orders_numbs)
    )
    orders_to_delete_query.delete()


def create_new_orders(session, data: List[Order], usd_rub: ExchangeRatio):
    """
    Сохранение в БД новых заявок
    :param session: сессия БД
    :param data: Данные для сохранения
    :param usd_rub: Контейнер с курсом валюты
    """
    new_orders = []

    for order in data:
        order.cost_rub = order.cost_usd * usd_rub.ratio
        new_orders.append(order)

    session.add_all(new_orders)
    return new_orders


def update_orders(
    db_data: List[Order], google_data_dict: Dict[int, Order], usd_rub: ExchangeRatio
):
    """
    :param db_data:
    :param google_data_dict: Заказы в виде словаря. Ключ - номер заказа, значение - данные заказа
    :param usd_rub: Контейнер с курсом валюты
    """
    for order in db_data:
        google_order = google_data_dict[order.order_numb]
        if order.id != google_order.id:
            order.id = google_order.id
        if order.cost_usd != google_order.cost_usd:
            order.cost_usd = google_order.cost_usd
        if order.delivery_date != google_order.delivery_date:
            order.delivery_date = google_order.delivery_date
            # Если дата стала подходящей для уведомления, то нужно будет уведомить в будущем
            if (
                order.notify_sent
                and google_order.delivery_date >= datetime.datetime.now().date()
            ):
                order.notify_sent = False
        cost_rub = order.cost_usd * usd_rub.ratio
        if order.cost_rub != cost_rub:
            order.cost_rub = cost_rub


async def check_delivery_deadline(orders: List[Order]):
    """
    Проверка срока поставки
    :param orders:
    :return:
    """
    now = datetime.datetime.now().date()
    orders_to_notify = []
    for order in orders:
        if not order.notify_sent and order.delivery_date < now:
            orders_to_notify.append(str(order.order_numb))
            order.notify_sent = True

    await send_notify(orders_to_notify)


async def transfer_google_sheet(usd_rub: ExchangeRatio):
    while True:
        logging.debug("Копирование таблицы")

        data = parse_orders_from_sheet(get_data_from_google_sheet(GOOGLE_SHEET_NAME))
        await save_data_to_db(data, usd_rub)

        logging.debug("таблица скопирована")
        await sleep(refresh_time_sec)
