import datetime
import logging
from typing import List

import gspread

from config import PATH_TO_CREDENTIALS, order_numb_col, cost_usd_col, delivery_date_col


def get_data_from_google_sheet(sheet_name: str, credentials: str = PATH_TO_CREDENTIALS):
    """
    Получаем данные с Google таблиц
    :param sheet_name: Наименование таблицы
    :param credentials:
    :return:
    """
    gspread_account = gspread.service_account(filename=credentials)
    wb = gspread_account.open(sheet_name)
    ws = wb.sheet1
    return ws.get_values()


def validate_and_process_order(order: List):
    """
    Проводим валидацию записи.
    Если запись валидна, то сразу же происходит обработка за счёт side effect
    :param order:
    :return:
    """
    try:
        order[order_numb_col] = int(order[order_numb_col])
        order[cost_usd_col] = float(order[cost_usd_col])
        order[delivery_date_col] = datetime.datetime.strptime(
            order[delivery_date_col], "%d.%m.%Y"
        )
        return True
    except ValueError:
        logging.debug(f"Невалидная запись: {order}")
        return False


def parse_orders_from_sheet(raw_data):
    return list(filter(validate_and_process_order, raw_data[1:]))
