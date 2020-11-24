from flask import render_template, flash, redirect,session
from app import app, db
from app.forms import LoginForm
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
@app.route('/index')
def index():

    user = current_user


    filenames = []
    for file in os.listdir(folder):
        filename = "static/images/" + os.fsdecode(file)
        if filename.endswith( ('.jpeg') ):
            filenames.append(filename)
    
    filenames.sort()
    print(filenames)

    return render_template('index.html', title = "home page", user = user, totalImages=filenames)
    
@app.route('/userTransactions/<username>')
def userTransactions(username):

    user = User.query.filter_by(username=username).first_or_404()

    conn = get_db_connection()
    products = conn.execute('SELECT price FROM products;').fetchall()

    conn.close()

  
    return render_template('userTransactions.html', user=user, products = products)

@app.route('/checkout/<username>')
def checkout(username):

    user = User.query.filter_by(username=username).first_or_404()

    return render_template('checkout.html', user=user)



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
    
    


if __name__ == '__main__':
   app.run(debug=True)