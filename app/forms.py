"""
Forms

Apply WTF using classes to setup content db

"""

from flask.ext.wtf import Form, HiddenField, DateTimeField, BooleanField, TextField, TextAreaField, IntegerField, PasswordField, RecaptchaField
from flask.ext.wtf import Required, Optional, Length
from wtforms import validators as v


#generates login form
class LoginForm(Form):
  email = TextField('Email', validators = [Required(), v.Email()])
  # utilize passwordfield out of wt form
  password = PasswordField('Password', validators = [Required()])
  remember_me = BooleanField('Remember Me', default = False)
  
#generates create account form. Note the names in quotes are labels that can be created
class CreateLogin(Form):
    fname = TextField('*First Name', validators = [Required()])
    lname = TextField('Last Name', validators = [Optional(strip_whitespace=True)])
    mobile = TextField('Mobile', validators = 
                    # sets optional entry and strips whitespace
                    [Optional(strip_whitespace=True), 
                    v.Length(max=15,
                    message='Mobile exceeds length')])
    zipcode = IntegerField('Zipcode', validators = 
                    [Optional(strip_whitespace=True)])
                    # v.NumberRange(max=9, 
                    # message='Zipcode exceeds length')])
    email = TextField('*Email',validators = [Required(),
                    v.Email(),
                    v.EqualTo('confirm_email',
                    message = "Emails must match")])
    confirm_email = TextField('*Confirm Email')
    bio = TextAreaField('Bio', validators = [Length(min = 0, max = 140)])
    password = PasswordField('*Password',
                    validators = [Required(),
                    v.EqualTo('confirm_password',
                    message = '*Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
    remember_me = BooleanField('Remember Me', default = False)
    recaptcha = RecaptchaField('*Person Test')

class EditForm(Form):
    fname = TextField('*First Name', validators = [Required()])
    bio = TextAreaField('Bio', validators = [Length(min = 0, max = 140)])