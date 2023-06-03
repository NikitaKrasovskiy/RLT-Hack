from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/db'
app.app_context().push()
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.String)
    data = db.Column(db.String)
    user_vk_id = db.Column(db.String)

    def __init__(self, name, price, data, user_vk_id):
        self.name = name
        self.price = price
        self.data = data
        self.user_vk_id = user_vk_id

    def test_fun(self, order_data):
        name = order_data[1]
        price = order_data[2]
        data = order_data[3]
        user_vk_id = order_data[0]

        data = Order(name, price, data, user_vk_id)
        db.session.add(data)
        db.session.commit()
        # db.session.refresh()


