import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models.category import Category
from models.food import Food


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', categories=Category.query.all())

@app.route('/category/new', methods=['GET'])
def new_category():
    return render_template('new.html')

@app.route('/category/create', methods=['POST'])
def create_category():
    from models.category import Category

    category = Category(request.form['name'])
    db.session.add(category)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all())

@app.route('/category/<id>', methods=['GET'])
def category(id):

    return render_template('category.html', category=Category.query.get(id))

@app.route('/posts/<id>/delete', methods=['GET'])
def delete_category(id):
    from models.category import Category
    from app import db
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all())


if __name__ == '__main__':
    app.run()
