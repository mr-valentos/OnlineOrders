import os
from flask import Flask, render_template, request, redirect, session, Response, flash
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
from models.user import User, Role
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

@app.route('/registration', methods=['GET'])
def registration():
    return render_template('authorization/registration.html')

@app.route('/new_user', methods=['POST'])
def new_user():
    form = LoginForm()
    if request.form['password'] == request.form['password2']:
        user = User(request.form['login'], request.form['email'], request.form['phone'], request.form['password'])
        user.new_user(user)
        return render_template('authorization/login.html', form=form, current_user=current_user)
    flash('Введен не верный пароль')
    return render_template('authorization/registration.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user,\
                           admin=admin_permission)

@app.route('/index_id/<id>', methods=['GET'])
def index_id(id):
    category = Category.query.get(id)
    return render_template('index.html', categories=Category.query.all(), foods=category.food, user=current_user,\
                           admin=admin_permission, )

@app.route('/admin/users', methods=['GET'])
def users():
    return render_template('admin/users.html', users=User.query.all())


@app.route('/category/new', methods=['GET'])
def new_category():
    with admin_permission.require():
        return render_template('new.html')

@app.route('/category/create', methods=['POST'])
def create_category():
    category = Category(request.form['name'])
    category.new_category(category)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)

@app.route('/category/<id>', methods=['GET'])
def category(id):
    return render_template('category.html', category=Category.query.get(id), foods=Food.query.all())

@app.route('/posts/<id>/delete', methods=['GET'])
def delete_category(id):
    category = Category.query.get(id)
    category.delete_category(category)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)

@app.route('/new_food/<id>', methods=['GET'])
def new_food(id):
    with admin_permission.require():
        return render_template('newfood.html', category=Category.query.get(id))

@app.route('/create_food', methods=['POST'])
def create_food():
    food = Food(request.form['name'], request.form['description'], request.form['price'], request.form['image'],
                request.form['category_id'])
    food.new_food(food)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)

@app.route('/food/<id>', methods=['GET'])
def food(id):

    return render_template('food.html', food=Food.query.get(id))

@app.route('/food/<id>/delete', methods=['GET'])
def delete_food(id):
    food = Food.query.get(id)
    food.delete_food(food)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)

@app.route('/food/<id>/edit', methods=['POST'])
def edit_price(id):
    food = Food.query.get(id)
    food.price = request.form['price']
    food.new_food(food)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)


@app.route('/order', methods=['GET'])
def order():
    return render_template('order.html', user=current_user, order=order)


@app.route('/create_order', methods=['POST'])
def create_order():
    order = Order.query.filter_by(user_id=current_user.id, status='pending').first()
    order.address = request.form['address']
    order.status = 'done'
    order.time = request.form['time']
    order.new_order(order)
    return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                           admin=admin_permission)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    from datetime import datetime

    date_create_order= datetime.now()
    time_order= '00:00'

    order = Order.query.filter_by(user_id=current_user.id, status='pending').first()

    if not order:
        order = Order(user_id=current_user.id, status='pending', created_at=date_create_order, address='www', time=time_order)
        order.new_order(order)

    id = request.form['food_id']
    food = Food.query.get(id)

    if food:
        #logic- add dish to cart
        food_order=FoodOrder(order_id=order.id, food_id=food.id, count=1, price=food.price)
        food_order.new_food_order(food_order)
        return jsonify(food.name)
    else:
        requestJson =jsonify("Ошибка! Блюдо не найдено")
        requestJson.status_code = 401
        return requestJson


@app.route('/cart', methods=['GET'])
def cart():
        #redirect to home

    order=Order.query.filter_by(user_id=current_user.id, status='pending').first()

    if not order:
        return render_template('index.html', categories=Category.query.all(), foods=Food.query.all(), user=current_user, \
                               admin=admin_permission)
    id = order.id
    food_order=FoodOrder.query.filter_by(order_id=id).all()
    return render_template('cart.html', user=current_user, food_orders=food_order, order=order.id, admin=admin_permission)


@app.route('/cart_count_minus', methods=['POST'])
def cart_count_minus():
    food_order = FoodOrder.query.get(request.form['id'])

    if food_order:
        food_order.count = request.form['count_minus']
        food_order.new_food_order(food_order)
    return jsonify(count=food_order.count)

@app.route('/cart_count_plus', methods=['POST'])
def cart_count_plus():
    food_order = FoodOrder.query.get(request.form['id'])

    if food_order:
        food_order.count = request.form['count_plus']
        food_order.new_food_order(food_order)
    return jsonify(count=food_order.count)

@app.route('/orders', methods=['GET'])
def orders():
    return render_template('orders_all.html', user=current_user, orders=Order.query.all())

@app.route('/edit_order/<id>', methods=['GET'])
def edit_order(id):
    return render_template('cart.html', user=current_user, food_orders=FoodOrder.query.filter_by(order_id=id).all(),\
                           order=Order.query.get(id), admin=admin_permission)

@app.route('/delete_order/<id>', methods=['GET'])
def delete_order(id):
    order = Order.query.get(id)
    order.delete_order(order)
    return render_template('orders_all.html', user=current_user, orders=Order.query.all())

if __name__ == '__main__':
    app.run()
