import datetime
import logging
from typing import List, Optional

import gspread

from config import (
    PATH_TO_CREDENTIALS,
    cost_usd_col,
    delivery_date_col,
    id_col,
    order_numb_col,
)
from database import Order


def get_data_from_google_sheet(sheet_name: str, credentials: str = PATH_TO_CREDENTIALS):
    """
    Получаем данные с Google таблиц
    :param sheet_name: Наименование таблицы
    :param credentials: файл с данными для подключения к Google Sheet
    :return:
    """
    gspread_account = gspread.service_account(filename=credentials)
    wb = gspread_account.open(sheet_name)
    ws = wb.sheet1
    return ws.get_values()


def validate_and_process_order(row: List) -> Optional[Order]:
    """
    Проводим валидацию записи и обработку записи
    """

    try:
        return Order(
            id=int(row[id_col]),
            order_numb=int(row[order_numb_col]),
            cost_usd=float(row[cost_usd_col]),
            delivery_date=datetime.datetime.strptime(
                row[delivery_date_col], "%d.%m.%Y"
            ).date(),
        )

    except ValueError:
        logging.warning(f"Невалидная запись: {row}")
        return None


def parse_orders_from_sheet(raw_data):
    return {
        data.order_numb: data
        for data in filter(bool, map(validate_and_process_order, raw_data[1:]))
    }
