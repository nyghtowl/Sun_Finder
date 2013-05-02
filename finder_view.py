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
    Help finding Apache page that shows loading


TOP TO DO:
    Create WT form and Login...
    Finish linking up just date
    Put text and links on map
    Setup autopopulate
    Setup map to pop-up on first page and allow selection of neighborhood for autocomplete
    
    Build out autocomplete w/ Liz direction
    ajax - send off request and use ajax to pull in bits to load


    setup ability to choose time

    polygon file - aquire for neihborhood - google maps has a way to apply polygon shape and make clickable
    flask login

    look into lscache - to store content on the local computer - would be good for storing weather

    utilize makefile or grunt to prepare the code and combine to push out
    look at github/pamalafox/everday/blob/master/application/urls.py - for additional ideas on user data to structure for users


"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
# import model and assign to db_session variable
from sun_model import session as db_session, Location, User
#login import
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user
#import form objects 
from forms import LoginForm, CreateLogin
# expect to need for pulling api key from environment
import os
# leverage for reporting time result
import datetime
import time
import sun_functions
import weather_forecast

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
    # login and validate the user...
    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email==form.email.data).first()
        user_password = user.password

        if user is not None:
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
    return redirect(url_for('search'))

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
                return redirect(url_for('form'))
        if user == None:
            fname = form.fname.data
            lname = form.lname.data
            mobile = form.mobile.data
            email = form.email.data
            password = form.password.data
            zipcode = form.zipcode.data
            accept_tos = True #don't need to save this - can be assumed since required on form
            timestamp = time.time()
          
            #save from data in User object to commit to db
            new_user = User(id = None,
                        email=email,
                        password=password,
                        fname=fname,
                        lname=lname,
                        mobile=mobile,
                        zipcode=zipcode,
                        accept_tos=accept_tos,
                        timestamp=timestamp)
            db_session.add(new_user)
            db_session.commit()
            flash('Account creation successful. Please login to your account.')
            return redirect('/')
    return render_template("create_login.html", title="Create Account Form", form=form)

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
    return render_template('search.html')

# create search function 
@app.route('/search', methods=['POST'])
def search():
    session.pop('forecast', None)

    # capture the form results
    txt_query = request.form['query']
    
    # FIX - search by specif time

    date_query = request.form['date']

    # determine date captured to utilize
    if not(date_query):
        as_of = datetime.datetime.now()
    else:
        #grabs date that is entered and combines with automatically generated time
        #FIX - all entering time
        #as_of_time = datetime.datetime.now().time()
        as_of_date = datetime.datetime.strptime(date_query, "%Y-%m-%d")
        as_of = datetime.datetime.combine(as_of_date,as_of_time)
    
    # pull coordinates from Google Places
    forecast_result = sun_functions.get_coord(txt_query, G_KEY, FIO_KEY, WUI_KEY)
    
    #FIX - push certain results back to Google Places to improve weigh results for neighborhoods & potentially still use local db on neighborhoods

    # validate there are coordinates and then get the forecast
    if forecast_result:
        forecast_result.validate_day(as_of)
        #x_test = validate_day_test(get_forecast_test(coord_result['lat'],coord_result['lng']))

        #forecast_result['loc_name'] = txt_query.title()
        session['forecast'] = forecast_result
        #print session["forecast"]

        return render_template('fast_result.html', result = forecast_result)
    
    #FIX flash a message to try search again if coord_result is not valid

    '''
    First Solution: Utilizing sample local db - may still use

    # query data model file to match name of location to lat & long and then assign to variables
    loc_match = db_session.query(Location).filter(Location.n_hood.ilike("%" + question + "%")).one()
    
    # confirm the infromation captured matches db; otherwise throw error and ask to search again 
    if loc_match:
        # if there is a match the pass to get forecast, validate its day and then get elements to pop results
        forecast_result = validate_day(get_forecast(loc_match))
        forecast_result['loc_name'] = question.title()
        #return redirect(url_for('fast_result'), result=forecast_result)
        return render_template('fast_result.html', result = forecast_result)
    else:
        # FIX using flash or a result on the html page...
        print "Sorry, we are not covering that area at this time. Please try again."
        return redirect(url_for('search'))
    '''

    # FIX add image and tempurature to a dictionary that is passed to page

# FIX - session not working

# create extended view that of weather results (Note need trailing slash to avoid 404 error if web page access trys to add it)
@app.route('/more_details/')
def more_details():
    forecast_details = session.get('forecast')
    print forecast_details
    #print forecast_details
    return render_template('more_details.html', details=forecast_details)

# create map view - set this up to test
@app.route('/map_view')
def map_view():
    return render_template('map_view.html')

# Below were used to test session variable and prove its working
# @app.route("/test1")
# def test1():
#   session['forecast'] = 5

#   session['squid'] = 5
#   return ""

# @app.route("/test2")
# def test2():
#   print session
#   return ""

# create profile page view with favorites and ability report on validty of sun

# runs app
if __name__ == "__main__":
    app.run(debug=True)