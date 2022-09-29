from sqlalchemy import Boolean, Column, Date, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

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


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer)
    order_numb = Column(Integer, primary_key=True, comment="Номер заказа")
    cost_usd = Column(Float, comment="стоимость,$")
    delivery_date = Column(Date, comment="Срок поставки")
    cost_rub = Column(Float, comment="Стоимость, руб")
    notify_sent = Column(Boolean, default=False, comment="Уведомление отправлено")
    # TODO Я бы добавил столбец "Заказ выполнен"


class TelegramUser(Base):
    __tablename__ = "notification_users"
    user_id = Column(Integer, primary_key=True)

    # Поля не используются, но могут быть полезными
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


def create_db(engine):
    # TODO Добавить проверку на валидность БД, если она уже существует
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db(engine)
