from typing import List, Dict

from sqlalchemy import Column, Date, Float, Integer, String, Boolean
from sqlalchemy_utils import create_database, database_exists

from config import order_numb_col, id_col, cost_usd_col, delivery_date_col
from database import Base, Session, engine


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer)
    order_numb = Column(Integer, primary_key=True)
    cost_usd = Column(Float)
    delivery_date = Column(Date)
    cost_rub = Column(Float)
    notify_sent = Column(Boolean, default=False)


class TelegramUser(Base):
    __tablename__ = "notification_users"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


def update_data(google_data: Dict[int, List], usd_rub: float):
    with Session() as session:
        all_orders_numbs = set(google_data.keys())

        # Ищем записи для обновления
        orders_to_update_query = session.query(Order).filter(
            Order.order_numb.in_(all_orders_numbs)
        )
        orders_to_update = orders_to_update_query.all()
        orders_to_update_numbs = {order.order_numb for order in orders_to_update}
        update_values(orders_to_update, google_data, usd_rub)

        # Добавляем новые записи в БД
        new_orders_numbs = all_orders_numbs - orders_to_update_numbs
        create_new_orders(
            session, [row for order_numb, row in google_data.items() if order_numb in new_orders_numbs], usd_rub
        )

        # Удаляем удаленные записи из БД, которых нет в Гугл таблицах
        orders_to_delete_query = session.query(Order).filter(
            Order.order_numb.not_in(all_orders_numbs)
        )
        orders_to_delete_query.delete()

        session.commit()


def create_new_orders(session, data: List[List], usd_rub: float):
    orders = []

    for order in data:
        order = Order(
            id=order[id_col],
            order_numb=order[order_numb_col],
            cost_usd=order[cost_usd_col],
            delivery_date=order[delivery_date_col],
            cost_rub=order[cost_usd_col] * usd_rub,
        )
        orders.append(order)

    session.add_all(orders)


def update_values(db_data: List[Order], google_data_dict: Dict[int, List], usd_rub: float):
    for order in db_data:
        google_order = google_data_dict[int(order.order_numb)]
        if order.id != google_order[id_col]:
            order.id = google_order[id_col]
        if order.cost_usd != google_order[cost_usd_col]:
            order.cost_usd = google_order[cost_usd_col]
        if order.delivery_date != google_order[delivery_date_col]:
            order.delivery_date = google_order[delivery_date_col]
        if order.cost_rub != order.cost_usd * usd_rub:
            order.cost_rub = order.cost_usd * usd_rub

if __name__ == '__main__':
    create_db(engine)