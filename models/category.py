from app import db


class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    food = db.relationship("Food")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'name ' + self.name

    def new_category(self, category):
        db.session.add(category)
        db.session.commit()

    def delete_category(self, category):
        db.session.delete(category)
        db.session.commit()