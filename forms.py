from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField


class LoginForm(Form):
    email = StringField()
    password = PasswordField()