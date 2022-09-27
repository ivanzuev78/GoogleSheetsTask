from typing import Optional

from sqlalchemy import (Column, ForeignKey, String,
                        create_engine, Date, text, Integer, Float)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.sql import func

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer)
    order_numb = Column(Integer, primary_key=True)
    cost_usd = Column(Float)
    delivery_date = Column(Date)
    cost_rub = Column(Float)


def create_db_engine():
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = 5432
    database_name = 'money_db'
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")
    return engine


def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)



def generate_test_data(engine, data, usd_rub: float):
    Session = sessionmaker(engine)
    with Session() as session:
        for row in data:
            id_, ord_numb, cost_usd, date = row
            cost_rub = int(cost_usd) * usd_rub
            order = Order(id=id_, order_numb=ord_numb, cost_usd=cost_usd, delivery_date=date,
                          cost_rub=cost_rub)
            session.add(order)
        session.commit()


if __name__ == '__main__':
    engine = create_db_engine()
    create_db(engine)