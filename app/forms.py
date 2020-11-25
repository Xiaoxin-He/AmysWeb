from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='Username')])
    password = PasswordField('Password',validators=[DataRequired(message='Password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddProductsForm(FlaskForm):
    
    product_name = StringField('Name of Product:')
    submit = SubmitField('Add Puppy')

class DeleteForm(FlaskForm):

    id = IntegerField('Id Number of Product to Remove:')
    submit = SubmitField('Remove Product')

class AdminLoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='Username')])
    password = PasswordField('Password',validators=[DataRequired(message='Password')])
    secret_key = PasswordField('Secret_key',validators=[DataRequired(message='admin secret_key')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

