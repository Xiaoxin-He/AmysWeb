from flask import render_template, flash, redirect,session, request, make_response,jsonify
from flask.globals import current_app
from app import app, db
from app.forms import LoginForm, AddProductsForm, DeleteForm, RegistrationForm
from app.models import User, Product
from flask_login import current_user, login_user, logout_user
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


import cv2
import time

from datetime import timedelta


if __name__ == '__main__':
    app.run(debug=True)

# app.config['SECRET_KEY'] = 'thisisasecret'
# app.config['UPLOADED_IMAGES_DEST'] = 'static/images'

# images = UploadSet('images', IMAGES)
# configure_uploads(app, images)



# PEOPLE_FOLDER = os.path.join('static', 'images')
# app.config['IMAGE_UPLOADS'] = PEOPLE_FOLDER
# path = '/Users/xiaoxinhe/Desktop/amysBakeryWeb/app/static/images'

# folder = os.fsencode(path)

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
    conn.close()

    return render_template('index.html', all_products_data = all_products_data)

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

# @app.route('/checkout/<username>')
# def checkout(username):

#     user = User.query.filter_by(username=username).first_or_404()

#     return render_template('checkout.html', user=user)



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

# @app.route('/admin_login', methods = ['GET', 'POST'])
# def admin_login():
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('admin_index'))
#     form = AdminLoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username = form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         # return redirect(url_for('admin_index'))
#         return render_template('admin_index.html')
#     return render_template('admin_login.html',title='Log in admin',form=form)

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
        # product_image = form.product_image.data
        
        # this 'filename' is the name in add.html!
        uploaded_file = request.files['fileName']
        filename = secure_filename(uploaded_file.filename)
        product_image = uploaded_file.filename

        if filename != '':
            uploaded_file.save(os.path.join('/Users/xiaoxinhe/Desktop/amysWeb/app/static/images', filename))
        new_product = Product(product_name, product_description, product_image)
        db.session.add(new_product)

        db.session.commit()

        return redirect(url_for('list_products'))

    return render_template('add.html', form = form)




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