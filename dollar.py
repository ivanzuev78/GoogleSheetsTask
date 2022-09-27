import pandas as pd


def get_dollar():
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp'

    usd_code = 'USD'
    df = pd.read_xml(url1, encoding='cp1251')
    res = df.loc[df['CharCode'] == usd_code]

    return res['Value'].iloc[0]
