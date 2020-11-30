from flask import render_template, flash, redirect,session, request, make_response,jsonify, Response
from flask.globals import current_app
from app import app, db
from app.forms import LoginForm, AddProductsForm, DeleteForm, RegistrationForm, EditProfileForm, AdminLoginForm
from app.models import User, Product
from flask_login import current_user, login_user, logout_user, login_required
from flask.helpers import url_for
import sqlite3


# **************
import imghdr
import os
# from flask import Flask, render_template, request, redirect, url_for, abort, \
#     send_from_diresctory
from werkzeug.utils import secure_filename
# import os
# from flask_uploads import configure_uploads, IMAGES, UploadSet

# pip install pillow
from PIL import Image

from flask import url_for, current_app

from flask import send_file, send_from_directory, safe_join, abort

import json

# import cv2
import time

from datetime import timedelta


if __name__ == '__main__':
    app.run(debug=True)


def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
# @app.route('/index')
def index():

    # products = Product.query.all()
    
    conn = get_db_connection()
    # get all data for products table from database
    all_products_data = conn.execute('SELECT * FROM products;').fetchall()
    total_item_in_home_page = conn.execute('SELECT count(*) FROM products;').fetchone()
    get_price_high_to_low = conn.execute('''
    SELECT p.product_price, p.product_name, p.product_image,p.product_description
    FROM products p
    ORDER BY p.product_price DESC
    ''').fetchall()
    conn.close()

    return render_template('index.html', all_products_data = all_products_data, total_item_in_home_page = total_item_in_home_page)


@app.route('/high_price')
def high_price():
    conn = get_db_connection()
    total_item_in_home_page = conn.execute('SELECT count(*) FROM products;').fetchone()
    
    get_price_high_to_low = conn.execute('''
    SELECT p.product_price, p.product_name, p.product_image,p.product_description
    FROM products p
    ORDER BY p.product_price DESC
    ''').fetchall()
    conn.close()
    return render_template('high_price.html', get_price_high_to_low = get_price_high_to_low, total_item_in_home_page = total_item_in_home_page)


@app.route('/low_price')
def low_price():
    conn = get_db_connection()
    total_item_in_home_page = conn.execute('SELECT count(*) FROM products;').fetchone()
    
    get_price_high_to_low = conn.execute('''
    SELECT p.product_price, p.product_name, p.product_image,p.product_description
    FROM products p
    ORDER BY p.product_price ASC
    ''').fetchall()
    conn.close()
    return render_template('low_price.html', get_price_high_to_low = get_price_high_to_low, total_item_in_home_page = total_item_in_home_page)

@app.route('/my_shopping_cart/<username>')
def shopping_cart(username):
    conn = get_db_connection()
    # get all data for products table from database
    all_products_data = conn.execute('SELECT * FROM products;').fetchall()
    conn.close()
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('shopping_cart.html', user = user, all_products_data = all_products_data)
# @app.route('/userTransactions/<username>')
# def userTransactions(username):

#     user = User.query.filter_by(username=username).first_or_404()

#     conn = get_db_connection()
#     products = conn.execute('SELECT price FROM products;').fetchall()

#     conn.close()

  
#     return render_template('userTransactions.html', user=user, products = products)

# http://localhost:5000/checkout/shirley1
@app.route('/checkout/<username>', methods = ['POST'])
def checkout(username):

    user = User.query.filter_by(username=username).first_or_404()

    user_id = user.id
    cart_items = request.json

    connection=sqlite3.connect('app.db')
    cursor=connection.cursor()
    # cursor.execute('INSERT INTO orders (user_id) VALUES (?)',(user_id,))
    # order_id = cursor.lastrowid
    # print("order id", cursor.lastrowid)
    connection.commit()

    item_price = 0
    count = 0
    for key in cart_items:
        item = cart_items[key]
        count = item["inCart"]
        # print("count", item["price"])
        item_price = item["price"]
        cursor.execute('INSERT INTO orders (incart_number, user_id) VALUES (?,?)',(count,user_id))
        order_id = cursor.lastrowid
        product_id = item["product_id"]
        for i in range(count):
           cursor.execute("INSERT INTO order_items (order_id, product_id) VALUES (?,?)",(order_id, product_id))
           
        #    order_id = cursor.lastrowid
           connection.commit()
    connection.close()

    item_price = float(item_price)
    count = float(count)
    # str
    # print("type of price", type(item_price))
    # print("type of count", type(count))
    # print("total", item_price*count)
    # total_price = item_price*count
    # total_cost(total_price)

    return render_template('checkout.html', user=user)

 

@app.route('/order_history/<username>')
def order_history(username):
    user = User.query.filter_by(username=username).first_or_404()
    # SELECT u.id, COUNT(order_id) FROM users u, orders o WHERE u.id = o.user_id GROUP BY o.order_id LIMIT 1;
    conn = get_db_connection()


    get_order_count_user = conn.execute('''
SELECT COUNT(DISTINCT o.order_id)
FROM orders o,
(
SELECT DISTINCT u.username, o.order_id, p.product_name
FROM orders o, users u, order_items oi, products p
INNER JOIN users ON u.id = o.user_id
INNER JOIN order_items ON o.order_id = oi.order_id
INNER JOIN products ON p.id = oi.product_id
GROUP BY u.id
)as ORDER_number
   ''').fetchall()
    
    get_order_details = conn.execute('''
SELECT DISTINCT u.username, o.order_id, p.product_name, p.product_image, p.product_price, o.incart_number
FROM orders o, users u, order_items oi, products p
INNER JOIN users ON u.id = o.user_id
INNER JOIN order_items ON o.order_id = oi.order_id
    ''').fetchall()

    conn.close()

    return render_template('order_history.html', user=user, get_order_count_user = get_order_count_user, get_order_details = get_order_details)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',title='Log in',form=form)

@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('admin_index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return redirect(url_for('admin_index'))
        return redirect(url_for('index'))
    return render_template('admin_login.html',title='Log in admin',form=form)

@app.route('/admin_index')
def admin_index():
    return render_template('admin_index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/add', methods = ['GET', 'POST'])
def add_products():

    form = AddProductsForm()
    #get uploaded file here1
    # uploaded_file = request.files['file']
    # filename = secure_filename(uploaded_file.filename)

    if form.validate_on_submit():
        product_name = form.product_name.data
        product_description = form.product_description.data
        product_price = form.product_price.data
        # product_image = form.product_image.data
        
        # this 'filename' is the name in add.html!
        uploaded_file = request.files['fileName']
        filename = secure_filename(uploaded_file.filename)
        product_image = uploaded_file.filename

        if filename != '':
            uploaded_file.save(os.path.join('/Users/xiaoxinhe/Desktop/amysWeb/app/static/images', filename))
        new_product = Product(product_name, product_description, product_image, product_price)
        db.session.add(new_product)

        db.session.commit()

        return redirect(url_for('list_products'))

    return render_template('add.html', form = form)

# @app.route('/test_get_data', methods=['POST'])
# def get_data():


@app.route('/list')
def list_products():
    # Grab a list of products from database.
    products = Product.query.all()
    print(products)

    files = os.listdir('/Users/xiaoxinhe/Desktop/amysWeb/app/static/images')

    return render_template('list.html', products = products, files = files)
    
@app.route('/delete', methods=['GET', 'POST'])
def del_products():

    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        product_name = Product.query.get(id)
        product_description = Product.query.get(id)
        db.session.delete(product_name)
        db.session.delete(product_description)
        db.session.commit()

        return redirect(url_for('list_products'))
    return render_template('delete.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory('/Users/xiaoxinhe/Desktop/amysWeb/app/static/images', filename)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
     
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)