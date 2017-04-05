import os
from flask import Flask, render_template, request, redirect, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_principal import Principal, Permission, RoleNeed, identity_changed, current_app, Identity, AnonymousIdentity, \
identity_loaded, UserNeed
from flask.ext.jsonpify import jsonify



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


from models.category import Category
from models.food import Food
from models.user import User
from models.food_order import FoodOrder
from models.order import Order

from forms import LoginForm

principals = Principal(app)
login_manager = LoginManager(app)

user_role = RoleNeed('user')
user_permission = Permission(user_role)

admin_role = RoleNeed('admin')
admin_permission = Permission(admin_role)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        # Retrieve the user from the hypothetical datastore
        user = User.query.filter_by(login=form.login.data).first()

        # Compare passwords (use password hashing production)
        if form.password.data == user.password:
            # Keep the user info in the session using Flask-Login
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            return redirect(request.args.get('next') or '/')

    return render_template('authorization/login.html', form=form, current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.login', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

@app.route('/admin/users', methods=['GET'])
def users():
    return render_template('admin/users.html', users=User.query.all())


@app.route('/category/new', methods=['GET'])
def new_category():
    with admin_permission.require():
        return render_template('new.html')

@app.route('/category/create', methods=['POST'])
def create_category():
    from models.category import Category

    category = Category(request.form['name'])
    db.session.add(category)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

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
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

@app.route('/new_food', methods=['GET'])
def new_food():
    with admin_permission.require():
        return render_template('newfood.html')

@app.route('/create_food', methods=['POST'])
def create_food():
    from models.food import Food

    food = Food(request.form['name'], request.form['description'], request.form['price'], request.form['image'],
                request.form['category_id'])
    db.session.add(food)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

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
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

@app.route('/food/<id>/edit', methods=['POST'])
def edit_price(id):

    from app import db
    food = Food.query.get(id)
    food.price = request.form['price']
    db.session.add(food)
    db.session.commit()
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user)

@app.route('/look_order', methods=['GET'])
def look_order():

    return render_template('look_order.html', user=current_user, order=Order.query.all())

@app.route('/order', methods=['GET'])
def order():

    return render_template('order.html', user=current_user, order=Order.query.all())


@app.route('/create_order', methods=['POST'])
def create_order():
    from models.order import Order

    order = Order(request.form['address'], request.form['user_id'], request.form['created_at'], request.form['time'])
    db.session.add(order)
    db.session.commit()
    return render_template('look_order.html', user=current_user, order=Order.query.all())


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    from models.food_order import FoodOrder
    from models.order import Order

    user=current_user

    for order in user.order:
        ord_id=order.id

    id = request.form['food_id']
    food = Food.query.get(id)

    if food:
        #логика добавления товара в корзину
        food_order=FoodOrder(order_id=ord_id, food_id=food.id, count=1, price=food.price)
        db.session.add(food_order)
        db.session.commit()
        return jsonify(food.name)
    else:
        requestJson =jsonify("Ошибка! Блюдо не найдено")
        requestJson.status_code = 401
        return requestJson



if __name__ == '__main__':
    app.run()
