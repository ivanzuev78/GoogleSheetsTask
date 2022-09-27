import time

import gspread

from db_schema import generate_test_data, create_db_engine, create_db

scopes = ["https://docs.google.com/spreadsheets/d/1Bjr3AqTbZbZH4kvwHAq-JEUvmMPjfzOVtrodxpTaYZE"]
filename = "credentials.json"


# Open a sheet from a spreadsheet in one go

def connect_sheet(sheet_name: str = "testIvanZuev"):
    gspread_account = gspread.service_account()
    wb = gspread_account.open(sheet_name)

    return wb

def get_data_from_sheet(wb):
    ws = wb.sheet1
    data = ws.get_all_values()
    metadata = wb.fetch_sheet_metadata()
    wb._properties.update(metadata["properties"])
    last_update_time = wb.lastUpdateTime
    print(wb.lastUpdateTime, data[0])
    return data


if __name__ == '__main__':
    engine = create_db_engine()
    create_db(engine)
    while True:
        wb = connect_sheet()

        data = get_data_from_sheet(wb)
        generate_test_data(engine, data[1:], 60)
        time.sleep(1)
