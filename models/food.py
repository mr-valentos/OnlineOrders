from app import db
from models.category import Category


class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer)
    image = db.Column(db.String(250), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    category = db.relationship("Category")


    def __init__(self, name, description, price, image, category_id):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.category_id = category_id

    def new_food(self, food):
        db.session.add(food)
        db.session.commit()

    def delete_food(self, food):
        db.session.delete(food)
        db.session.commit()
