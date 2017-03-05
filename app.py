import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    from models.food import Food
    return render_template('index.html', foods=Food.query.all())

if __name__ == '__main__':
    app.run()
