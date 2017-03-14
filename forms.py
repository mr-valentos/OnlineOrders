from flask_wtf import FlaskForm, validators
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from models.user import User

class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
