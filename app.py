import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models.category import Category
from models.food import Food


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', categories=Category.query.all())


@app.route('/category/<id>', methods=['GET'])
def category(id):

    return render_template('category.html', category=Category.query.get(id))

if __name__ == '__main__':
    app.run()
