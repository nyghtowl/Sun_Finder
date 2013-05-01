"""
forms.py is the file to use to setup the databases

Go Live: Add this and database info to gitignore

"""

#import from flask wt forms
from flask.ext.wtf import Form, HiddenField, DateTimeField, BooleanField, TextField, IntegerField, PasswordField
from flask.ext.wtf import Required
from wtforms import validators as v
#import sun_model?


#generates login form
class LoginForm(Form):
  email = TextField('email', validators = [Required(), v.Email()])
  # utilize passwordfield out of wt form
  password = PasswordField('password', validators = [Required()])
  
#generates create account form
class CreateLogin(Form):
    fname = TextField('fname', validators = [Required()])
    lname = TextField('lname', validators = [Required()])
    mobile = TextField('mobile')
    zipcode = IntegerField('zipcode')
    email = TextField('email',validators = [Required(),
                    v.Email(),
                    v.EqualTo('confirm_email',
                    message = "Emails must match")])
    confirm_email = TextField('Repeat Email')
    password = PasswordField('first_password',
                    validators = [Required(),
                    v.EqualTo('confirm_password',
                    message = 'Passwords must match')])
    confirm_password = PasswordField('Repeat Password')
    accept_tos = BooleanField('accept_tos', validators = [Required()]) 
        # FIX - figure out syntax message = 'I accept the TOS'])
    
