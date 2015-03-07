# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class AddDomainForm(Form):
    name = TextField('Task Name', validators=[DataRequired()])


class RegisterForm(Form):
    name = TextField(
        'Username',
        validators=[DataRequired(),
        Length(min=6, max=25)]
    )
    email = TextField(
        'Email',
        validators=[DataRequired(),
        Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
        Length(min=6, max=40)])
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password',
        message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
