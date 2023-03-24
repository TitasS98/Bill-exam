from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo
import app

class registerform(FlaskForm):
    fullname = StringField('Full Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeatpassword =  PasswordField('Repeat Password', [EqualTo('password', 'password different' )])
    submit = SubmitField("Register")
    
    
    # def validate_email(self, email):
    #     customer = app.Customer.query.filter.by(customer=email.data).first()
    #     if customer:
    #         raise ValidationError('This email address has already been added!')



class loginform(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField("Login")




class Groups(FlaskForm):
    groupsid = StringField('GroupsID', [DataRequired()])
    tripto = StringField('Trip to', [DataRequired()])
    submit = SubmitField("Add")


class bills(FlaskForm):
    ammount = IntegerField('Amount', [DataRequired()])
    descriptionn = StringField('Description', [DataRequired()])
    submit = SubmitField("Add")