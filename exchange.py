import pandas as pd

from config import CBR_URL


def get_exchange_ratio(currency_code):
    df = pd.read_xml(CBR_URL, encoding="cp1251")
    res = df.loc[df["CharCode"] == currency_code]
    return float(res["Value"].iloc[0].replace(",", "."))
