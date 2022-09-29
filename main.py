import datetime
import time
import logging

from config import (
    GOOGLE_SHEET_NAME,
    exchange_rate_update_sec,
    refresh_time_sec,
)
from database import engine
from db_schema import create_db, update_data
from exchange import get_exchange_ratio
from work_with_google import parse_orders_from_sheet, get_data_from_google_sheet


def main():
    create_db(engine)
    current_exchange_ratio = get_exchange_ratio("USD")
    ratio_updated_time = datetime.datetime.now()
    while True:
        logging.debug(f"Старт обновления данных")
        if (
            datetime.datetime.now() - ratio_updated_time
        ).seconds > exchange_rate_update_sec:
            current_exchange_ratio = get_exchange_ratio("USD")
            ratio_updated_time = datetime.datetime.now()
            logging.info(f"курс доллара обновлен: {current_exchange_ratio}")
        data = parse_orders_from_sheet(get_data_from_google_sheet(GOOGLE_SHEET_NAME))
        update_data(data, current_exchange_ratio)
        logging.debug(f"Окончание обновления данных")
        time.sleep(refresh_time_sec)


if __name__ == "__main__":
    main()
