from app import db
from models.user import User


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250))
    time = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")


    def __init__(self, created_at, address, time, user_id, status):
        self.created_at = created_at
        self.address = address
        self.time = time
        self.user_id = user_id
        self.status = status


    def __repr__(self):
       return 'address: ' + self.address

    def new_order(self, order):
        db.session.add(order)
        db.session.commit()

    def delete_order(self, order):
        db.session.delete(order)
        db.session.commit()