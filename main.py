from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wassa456@localhost/db'
app.app_context().push()
db = SQLAlchemy(app)

class OKVED(db.Model):
    __tablename__ = "okveds"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    id_format = db.Column(db.String)
    link = db.Column(db.String)

    def to_json_okved(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_format': self.id_format,
            'link': self.link
        }

    def get_by_okved_name(self, name_other):
        okveds = OKVED.query.filter_by(name=str(name_other)).all()
        okved_json = [okved.to_json_okved() for okved in okveds]
        return okved_json


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.String)
    data = db.Column(db.String)
    user_vk_id = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'data': self.data,
            'user_vk_id': self.user_vk_id
        }

    def __init__(self, name, price, data, user_vk_id):
        self.name = name
        self.price = price
        self.data = data
        self.user_vk_id = user_vk_id

    def test_fun(self, order_data):
        name = order_data[1]
        price = order_data[2]
        data = order_data[3]
        user_vk_id = int(order_data[0])

        data = Order(name, price, data, user_vk_id)
        db.session.add(data)
        db.session.commit()

    def select_orders_by_user_vk_id(self,user_vk_id):
        orders = Order.query.filter_by(user_vk_id=user_vk_id).all()
        orders_json = [order.to_json() for order in orders]
        return orders_json
        # db.session.refresh()

        # def get order select * from orders As o where o.user_vk_id = inner.user_vk_id
