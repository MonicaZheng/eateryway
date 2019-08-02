from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
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

class Dim_Customer(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    Lname = db.Column(db.String(64), index=True)
    Fname = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    cell = db.Column(db.Integer, index=True)
    sales = db.relationship('Fact_Sale', backref='customer', lazy=True)

    def __init__(self, email, username, password, Lname, Fname, cell):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.Lname = Lname
        self.Fname = Fname
        self.cell = cell

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Dim_Address(db.Model):

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), index=True)
    sales = db.relationship('Fact_Sale', backref='customer', lazy=True)

    def __init__(self, id, address, customer_id):
        self.address = address
        self.customer_id = customer_id


class Order(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime(), index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),nullable=False)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
