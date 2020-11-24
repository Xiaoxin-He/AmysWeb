from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask import session

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
    
    def setCurrentUser(self):
        login_user(self)
        session["USERNAME"] = self.username
    
    def getCurrentUserName():
        return session.get("USERNAME")



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64))
    description = db.Column(db.Text)
    price = db.Column(db.INTEGER)
    product_kind = db.Column(db.String(128))

    def __repr__(self) :
        return '<Product {}>'.format(self.product_name)

    
