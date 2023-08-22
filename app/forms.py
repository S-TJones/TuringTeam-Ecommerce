# from itertools import product
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    retypePassword = StringField('Re-enter Password', validators=[InputRequired()])

#----------------------------------------------------------------------

class UserUpdate(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    role = StringField('role', validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

#----------------------------------------------------------------------

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price= StringField('Price', validators=[InputRequired()])
    image = FileField('Image',validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'Select image files only.')])
    
#----------------------------------------------------------------------

class UpdateOrder(FlaskForm):
    status_options= SelectField('status', validators=[DataRequired()])

