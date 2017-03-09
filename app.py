import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models.category import Category
from models.food import Food
from models.user import User

principals = Principal(app)
login_manager = LoginManager(app)





'''
@login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return datastore.find_user(id=userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        # Retrieve the user from the hypothetical datastore
        user = datastore.find_user(email=form.email.data)

        # Compare passwords (use password hashing production)
        if form.password.data == user.password:
            # Keep the user info in the session using Flask-Login
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            return redirect(request.args.get('next') or '/')

    return render_template('login.html', form=form)'''


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all())

@app.route('/admin/users', methods=['GET'])
def users():
    return render_template('admin/users.html', users=User.query.all())


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

@app.route('/new_food', methods=['GET'])
def new_food():
    return render_template('newfood.html')

@app.route('/create_food', methods=['POST'])
def create_food():
    from models.food import Food

    food = Food(request.form['name'], request.form['description'], request.form['price'], request.form['image'],
                request.form['category_id'])
    db.session.add(food)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all())

@app.route('/food/<id>', methods=['GET'])
def food(id):

    return render_template('food.html', food=Food.query.get(id))

@app.route('/food/<id>/delete', methods=['GET'])
def delete_food(id):
    from models.food import Food
    from app import db
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all())

@app.route('/food/<id>/edit', methods=['POST'])
def edit_price(id):

    from app import db
    food = Food.query.get(id)
    food.price = request.form['price']
    db.session.add(food)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all())

if __name__ == '__main__':
    app.run()
