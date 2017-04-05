from app import db
from models.user import User


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")


    def __init__(self, created_at, address, time, user_id):
        self.created_at = created_at
        self.address = address
        self.time = time
        self.user_id = user_id


    def __repr__(self):
       return 'address: ' + self.address

