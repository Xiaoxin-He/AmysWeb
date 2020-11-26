from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask import session
from wtforms import FileField

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    # def setCurrentUser(self):
    #     login_user(self)
    #     session["USERNAME"] = self.username
    
    # def getCurrentUserName():
    #     return session.get("USERNAME")



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# class Product(db.Model):
#     __tablename__ = 'products'

#     id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String(64))
#     description = db.Column(db.Text)
#     price = db.Column(db.INTEGER)
#     product_kind = db.Column(db.String(128))

#     def __Init__(self, product_name):
#         self.product_name = product_name

#     def __repr__(self) :
#         return '<Product {}>'.format(self.product_name)
    

    
class Product(db.Model):
    
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key = True)
    product_name = db.Column(db.Text)
    product_description = db.Column(db.Text)
    product_image = FileField('picture')


    def __init__(self,product_name, product_description):
        self.product_name = product_name
        # self.id = id
        self.product_description = product_description

    def __repr__(self):
        return f"Product name: {self.product_name}  --- id is : {self.id}  --- description : {self.product_description}"

class admin(db.Model):
    __tablename__ = 'administrator'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    secret_key = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
            return '<Admin_User {}>'.format(self.username)
    
    def set_secret_key(self, secret_key):
        self.secret_key = generate_password_hash(secret_key)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
