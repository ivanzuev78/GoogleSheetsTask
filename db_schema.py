from typing import List

from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy_utils import create_database, database_exists

from database import Base, Session


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer)
    order_numb = Column(Integer, primary_key=True)
    cost_usd = Column(Float)
    delivery_date = Column(Date)
    cost_rub = Column(Float)


def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


def update_data(data: List[List], usd_rub: float):
    with Session() as session:
        all_orders_numbs = set(d[1] for d in data)
        orders_to_update_query = session.query(Order).filter(
            Order.order_numb.in_(all_orders_numbs)
        )
        orders_to_update = orders_to_update_query.all()
        orders_to_update_numbs = {order.order_numb for order in orders_to_update}

        orders_to_delete_query = session.query(Order).filter(
            Order.order_numb.not_in(all_orders_numbs)
        )
        orders_to_delete_query.delete()

        new_orders_numbs = all_orders_numbs - orders_to_update_numbs

        create_new_orders(
            session, [row for row in data if row[1] in new_orders_numbs], usd_rub
        )

        session.commit()


def create_new_orders(session, data: List[List], usd_rub):
    for order in data:
        id_, ord_numb, cost_usd, date = order
        cost_rub = int(cost_usd) * usd_rub

        order = Order(
            id=id_,
            order_numb=ord_numb,
            cost_usd=cost_usd,
            delivery_date=date,
            cost_rub=cost_rub,
        )
        session.add(order)
