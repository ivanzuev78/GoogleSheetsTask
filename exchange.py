import logging
from asyncio import sleep

import pandas as pd

from config import CBR_URL, exchange_rate_update_sec


class ExchangeRatio:
    """
    Класс для обновления курса валют
    Полезен, чтобы к курсу был доступ из разных задач в loop
    """

    def __init__(self, currency_code):
        self.currency_code = currency_code
        self.ratio = None
        self.update_exchange_ratio()

    def update_exchange_ratio(self):
        """
        Запрос и парсинг курса
        """
        logging.debug("Обновляем курс")
        df = pd.read_xml(CBR_URL, encoding="cp1251")
        res = df.loc[df["CharCode"] == self.currency_code]
        self.ratio = float(res["Value"].iloc[0].replace(",", "."))

    async def update_exchange_ratio_task(self):
        """
        Корутина для регулярного обновления курса
        """
        while True:
            self.update_exchange_ratio()
            logging.info(f"курс доллара обновлен: {self.ratio}")
            await sleep(exchange_rate_update_sec)
