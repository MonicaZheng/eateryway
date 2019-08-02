from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    address = db.relationship('Address', backref='user', lazy=True)
    order = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), unique=True, index=True)
    apt_num = db.Column(db.String(64), unique=True, index=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, address, apt_num, user_id):
        self.address = address
        self.apt_num = apt_num
        self.user_id = user_id


class Order(db.Model):

    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow(), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    orderitem = db.relationship('OrderItem', backref='order', lazy=True)


    def __init__(self, order_date, user_id):
        self.order_date = order_date
        self.user_id = user_id


class Food(db.Model):

    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    unit_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(256), index=False)
    category = db.Column(db.String(64), index=True)
    orderitem = db.relationship('OrderItem', backref='food', lazy=True)

    def __init__(self, name, unit_price, category):
        self.name = name
        self.unit_price = unit_price
        self.category = category

class PaymentType(db.Model):

    __tablename__ = 'pay_type'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(64), unique=True, nullable=False)
    payment = db.relationship('Payment', backref='pay_type', lazy=True)

    def __init__(self, type):
        self.type = type


class OrderItem(db.Model):

    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, index=True, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)


    def __init__(self, quantity, food_id, order_id):
        self.quantity = quantity
        self.food_id = food_id
        self.order_id = order_id


class Payment(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    balance = db.Column(db.Float, index=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    pay_type_id = db.Column(db.Integer, db.ForeignKey('pay_type.id'), nullable=False)

    def __init__(self, balance, order_id, pt_id):
        self.balance = balance
        self.order_id = order_id
        self.pay_type_id = pay_type_id
