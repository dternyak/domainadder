# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired

class AddDomainForm(Form):
    name = TextField('Domain Name', validators=[DataRequired()])
