from myproject import app,db, csrf
from flask import render_template, redirect, request, url_for, flash, abort, session, jsonify
from flask_login import login_user,login_required,logout_user
from myproject.models import User, Food, Address
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exists


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/pick_up', methods=['GET', 'POST'])
@login_required
def pick_up():
    session['delivery_location'] = None
    if request.method == "POST": # Store the order pick-up or delivery location
        if request.form['store']:
            session["pk_location"] = request.form['store']
            return redirect(url_for('menu'))

    return render_template('pick_up.html')

@app.route('/delivery', methods=['GET', 'POST'])
@login_required
def delivery():
    session["pk_location"] = None
    if request.method == "POST": # Store the order pick-up or delivery location
        if request.form['postal_code']:
            session["delivery_location"] = request.form['autocomplete']
            session["apt_num"] = request.form['apt_num']
            address_input = request.form['autocomplete']
            apt_input = request.form['apt_num']

            user_id = session["current_user_id"]

            try:
                address_record = Address(address=address_input, apt_num=apt_input, user_id=user_id)

                db.session.add(address_record)
                db.session.commit()

            except:
                pass

            return redirect(url_for('menu'))

    return render_template('delivery.html')

@app.route('/catering')
def catering():
    return render_template('catering.html')

@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():

    cof_tea_items = Food.query.filter_by(category="cof_tea")
    baked_items = Food.query.filter_by(category="baked")
    blend_items = Food.query.filter_by(category="blend")
    return render_template('menu.html',cof_tea_items=cof_tea_items,baked_items=baked_items,blend_items=blend_items, cart=session["cart"], total_price=session["total_price"])

@app.route('/_add_cart', methods=['GET', 'POST'])
@login_required
def _add_cart():
    diction = request.args.to_dict(flat=False)

    diction["item_id"] = int(''.join(diction["item_id"]))
    diction["name"] = ''.join(diction["name"])
    diction["price"] = float((''.join(diction["price"])).replace("$", ""))
    diction["quantity"] = int(''.join(diction["quantity"]))
    print(diction)
    total_price = 0
    if not session["cart"]: #check if session["cart"] is empty
        session["cart"].append(diction)
        total_price += session["cart"][0]["price"]*session["cart"][0]["quantity"]
    else:
        session["cart"].append(diction)
        for idx,item in enumerate(session["cart"]):
            if idx <= len(session["cart"])-2: # Exclude(Not looking) the newly add one
                # If the food newly added already exists in the session["cart"],
                # then add the quantity to the original one and pop the new added one from the last of the list
                if item["item_id"] == diction["item_id"]:
                    print("already existed")
                    item["quantity"] += diction["quantity"]
                    session["cart"].pop()
            # Summation of the total price covers both two situations: If the newly added was not poped or If the newly added was poped.
            total_price += item["price"]*item["quantity"]

    session["total_price"] = round(total_price,2)
    return jsonify({"cart_info": session["cart"], "total_price":session["total_price"]})


@app.route('/_edit_cart', methods=['GET', 'POST'])
@login_required
def _edit_cart():
    diction = request.args.to_dict(flat=False)
    diction["item_id"] = int(''.join(diction["item_id"]))
    diction["quantity"] = int(''.join(diction["quantity"]))

    print(diction)
    total_price = 0
    for idx,item in enumerate(session["cart"]):
        if item["item_id"] == diction["item_id"]:
            item["quantity"] = diction["quantity"]
        total_price += item["price"]*item["quantity"]

    session["total_price"] = round(total_price,2)

    return jsonify({"cart_info":session["cart"], "total_price":session["total_price"]})

@app.route('/_remove_cart', methods=['GET', 'POST'])
@login_required
def _remove_cart():
    diction = request.args.to_dict(flat=False)
    diction["item_id"] = int(''.join(diction["item_id"]))

    print(diction)
    total_price = []
    for idx,item in enumerate(session["cart"]):
        if item["item_id"] == diction["item_id"]:
            locator = idx
        total_price.append(item["price"]*item["quantity"])

    session["cart"].pop(locator)
    total_price.pop(locator)

    total_price = sum(total_price)
    session["total_price"] = round(total_price,2)

    return jsonify({"cart_info":session["cart"], "total_price":session["total_price"]})

@app.route('/check_out')
@login_required
def check_out():
    amount_off = 0
    total_price = session["total_price"]
    list_promo = [{"code":"EXAMPLECODE","value":5}]
    promo_code = "EXAMPLECODE"
    for promo in list_promo:
        if promo_code == promo["code"]:
            amount_off = promo["value"]
            break

    total_price -= amount_off
    total_price = round(total_price,2)
    return render_template('check_out.html', num_items=len(session["cart"]), cart=session["cart"], total_price=total_price)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":


        error = None
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        user = User.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):

            login_user(user)
            flash(f'Logged in successfully.')


            session["cart"] = []
            session["current_user_id"] = user.get_id()
            session["total_price"] = None
            session["pk_location"] = None
            session['delivery_location'] = None
            session['apt_num'] = None

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('home')

            return redirect(next)

        else:
            error = f"Check Your Email or Password."
            flash(error)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        error=None
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = User(email=email,
                    username=username,
                    password=password)
        if not db.session.query(exists().where(User.email==email)).scalar():
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering. Now you can login.')
            return redirect(url_for('login'))
        else:
            error = 'Email {} is already registered.'.format(email)
            flash(error)
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
