from app import db
from flask_login import UserMixin


association_table = db.Table('users_roles', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    roles = db.relationship("Role", secondary=association_table)

    def __init__(self, login, password, phone):
        self.login = login
        self.password = password
        self.phone = phone

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.login, self.phone)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%d/%s" % (self.id, self.name)
