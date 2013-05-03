"""
finder_view.py -- A flask based sun search tool

TO DO: 
    Go Live: 
        change secret key 
        turn off debug

    Currently small sample used and picking center of neighborhood. Future would be good to find a better way to apply

    Need to add neighborhood to query - still not perfect but will help center
    Set radius and cetnral coordinates to cover bay area
    Can set a loop to compare coordinates for closest to the central ones for neighborhood in local db?

QUESTIONS / ERROR:
    Help finding Ajax page that shows loading - jquery.post
    Clean up trying to setup login on the results page
    Revise logn if code to make into switch



TOP TO DO:

    Finish linking up just date - put on both pages
    Put text and links on map

    Setup map to pop-up on first page and allow selection of neighborhood for autocomplete
    
    finish setting up ajax 

    setup ability to choose time

    polygon file - aquire for neihborhood - google maps has a way to apply polygon shape and make clickable
    flask login

    look into lscache - to store content on the local computer - would be good for storing weather

    utilize makefile or grunt to prepare the code and combine to push out
    look at github/pamalafox/everday/blob/master/application/urls.py - for additional ideas on user data to structure for users


"""

from flask import Flask, render_template, redirect, url_for, session, flash
# import model and assign to db_session variable
from sun_model import session as db_session, Location, User
#login import
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user
#import form objects 
from forms import LoginForm, CreateLogin
# expect to need for pulling api key from environment
import os
import sun_functions
import weather_forecast
import json 

# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
#app.secret_key = os.environ.get('flask_key')
app.secret_key = 'key'

app.config.from_object(__name__) # allows for setting all caps var as global var

# pull api keys from environment
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

#login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

# user load callback - populates current user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# main index page
@app.route('/')
def index():
    return redirect(url_for('search'))

# Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # login and validate the user exists in the database
    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email==form.email.data).first()

        # if user exists then apply login user functionatlity to generate current_user session
        if user is not None:
            user_password = user.password
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('search'))
        else:
            flash('Incorrect Password')
            return redirect('login')
    return render_template('login.html', title="Login", form=form)

#logout
@app.route('/logout')
@login_required # confirms if user_id in session - sends to login view if not
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('search', locations=None))

#create user form view
@app.route('/create_login', methods = ['POST', 'GET'])
def create_login():
    form = CreateLogin()
    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email == form.email.data).first()
        if user != None:
            user_email = user.email
            if user_email == form.email.data:
                flash ('email already exists')
                return redirect(url_for('login'))
        #if user doesn't exist, save from data in User object to commit to db
        if user == None:
            new_user = User(id = None,
                        email=form.email.data,
                        password=form.password.data,
                        fname=form.fname.data,
                        lname=form.lname.data,
                        mobile=form.mobile.data,
                        zipcode=form.zipcode.data,
                        #don't need to save this - can be assumed since required on form
                        accept_tos=True,
                        timestamp=time.time())
            db_session.add(new_user)
            db_session.commit()
            flash('Account creation successful. Please login to your account.')
            return redirect('/')
    return render_template('create_login.html', title='Create Account Form', form=form)

# Display main search / index page
@app.route('/search')
def display_search():
    # create object of neighborhoods from db
    neighborhood = db_session.query(Location).all()
    session['n_hood'] = 5
    print session
    
    return render_template('search.html', locations=neighborhood)

@app.route("/ajax_search", methods=["POST"])
def ajax_search():
    return render_template('search_results_partial.html', result = sun_functions.search_results(G_KEY, FIO_KEY, WUI_KEY, neighborhood=None))

# renders result page after a search 
@app.route('/search', methods=['POST'])
def search():
    #neighborhood = session.get('n_hood')
    neighborhood = db_session.query(Location).all()
    print session
    return render_template('fast_result.html', result = sun_functions.search_results(G_KEY, FIO_KEY, WUI_KEY, neighborhood), locations=neighborhood)

# Below were used to test session variable and prove its working
@app.route("/test1")
def test1():
    session['forecast'] = 5
  
    session['squid'] = 5
    return ""
    
 
@app.route("/test2")
def test2():
    print session
    return ""

# create extended view that of weather results (Note need trailing slash to avoid 404 error if web page access trys to add it) - example of session to leverage elsewhere
# @app.route('/more_details/')
# def more_details():
#     forecast_details = session.get('forecast')
#     print forecast_details
#     #print forecast_details
#     return render_template('more_details.html', details=forecast_details)
#     session.pop('forecast', None)

# create map view - set this up to test
@app.route('/map_view')
def map_view():
    return render_template('map_view.html')


# create profile page view with favorites and ability report on validty of sun



# FIX - Json view - what Liz added to help with adding Ajax - need to rework
# @app.route('/some_json_route')
# def some_json():
#     return json.dumps({"thing" : "stuff"})

# runs app
if __name__ == "__main__":
    app.run(debug=True)