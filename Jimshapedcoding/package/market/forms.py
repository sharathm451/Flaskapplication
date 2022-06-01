from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import  Length, EqualTo, Email , DataRequired, ValidationError
from market.models import User 

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! please try a different username')
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


# Note: here flaskform takes care about the validate_variablename functions, there are no any special functions 
#  like validate_username but all the logic is only validate and underscore the next existing database variable name so 
#  it automatically becomes a function and start validating of that parameter values.
#  the same method to the username_to_check,email_address_to_check.   

    username = StringField(label='Username',validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address',validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm password',validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label = 'Password:', validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


# to create secret key app.config  commands required 
# cmd python
# import os 
# os.urandom(12).hex() 
# copy it and paste in main __init__ file

