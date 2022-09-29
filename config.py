import configparser
import logging

config = configparser.ConfigParser()
config.read(r"config\settings.ini")

GOOGLE_SHEET_NAME = config["DEFAULT"]["google_sheet_name"]
PATH_TO_CREDENTIALS = config["DEFAULT"]["path_to_credentials"]
CBR_URL = config["DEFAULT"]["cbr_url"]
log_level = int(config["DEFAULT"]["log_level"])

refresh_time_sec = int(config["DEFAULT"]["refresh_time_sec"])
exchange_rate_update_sec = int(config["DEFAULT"]["exchange_rate_update_sec"])

id_col = int(config["COL_MAP"]["id"])
order_numb_col = int(config["COL_MAP"]["order_numb"])
cost_usd_col = int(config["COL_MAP"]["cost_usd"])
delivery_date_col = int(config["COL_MAP"]["delivery_date"])

logging.basicConfig(filename="example.log", filemode="w", level=log_level)
