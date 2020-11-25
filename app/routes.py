from flask import render_template, flash, redirect,session
from app import app, db
from app.forms import LoginForm, AddProductsForm, DeleteForm, RegistrationForm
from app.models import User, Product
from flask_login import current_user, login_user, logout_user
from flask.helpers import url_for
import sqlite3
from werkzeug.utils import secure_filename
import os

from flask import send_file, send_from_directory, safe_join, abort


PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['IMAGE_UPLOADS'] = PEOPLE_FOLDER
path = '/Users/xiaoxinhe/Desktop/amysBakeryWeb/app/static/images'

folder = os.fsencode(path)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
# @app.route('/index')
def index():

    # user = current_user


    # filenames = []
    # for file in os.listdir(folder):
    #     filename = "static/images/" + os.fsdecode(file)
    #     if filename.endswith( ('.jpeg') ):
    #         filenames.append(filename)
    
    # filenames.sort()
    # print(filenames)
    # , title = "home page", user = user, totalImages=filenames

    return render_template('index.html')
    
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


@app.route("/get-image")
def get_image():
    # filename = f"{image_name}.jpeg"
    full_filename = os.path.join(app.config['IMAGE_UPLOADS'], 'cake1.jpeg')

    # basepath = os.path.dirname(__file__)  
    # upload_file = os.path.join(basepath, 'static/images', secure_filename(filename))
    return render_template('image.html', upload_file = full_filename)
    
    # try:
    #     return send_from_directory(app.config["IMAGE_UPLOADS"], filename=filename, as_attachment=False)
    # except FileNotFoundError:
    #     abort(404)
    
    
############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/add', methods = ['GET', 'POST'])
def add_products():

    form = AddProductsForm()

    if form.validate_on_submit():
        product_name = form.product_name.data

        #add new products to database
        new_product = Product(product_name)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('list_products'))
    

    return render_template('add.html', form = form)

@app.route('/list')
def list_products():
    # Grab a list of products from database.
    products = Product.query.all()
    print(products)
    return render_template('list.html', products = products)
    
@app.route('/delete', methods=['GET', 'POST'])
def del_products():

    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        product_name = Product.query.get(id)
        db.session.delete(product_name)
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

if __name__ == '__main__':
   app.run(debug=True)