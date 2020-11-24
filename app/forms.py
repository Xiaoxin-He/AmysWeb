from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='Username')])
    password = PasswordField('Password',validators=[DataRequired(message='Password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
