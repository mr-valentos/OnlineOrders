from app import db
from models.order import Order
from models.food import Food


class FoodOrder(db.Model):
    __tablename__ = 'food_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey(Order.id), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey(Food.id), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    food = db.relationship("Food")
    order = db.relationship("Order")


    def __init__(self, order_id, food_id, count, price):
        self.order_id = order_id
        self.food_id = food_id
        self.count = count
        self.price = price

    def new_food_order(self, food_order):
        db.session.add(food_order)
        db.session.commit()