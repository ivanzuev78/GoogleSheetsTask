from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

Base = declarative_base()


def create_db_engine():
    host = config["POSTGRES"]["host"]
    port = config["POSTGRES"]["port"]
    user = config["POSTGRES"]["user"]
    password = config["POSTGRES"]["password"]
    database = config["POSTGRES"]["database"]
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    return engine


engine = create_db_engine()
Session = sessionmaker(bind=engine)  # сессии для транзакций
