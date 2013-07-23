"""
finder_view.py -- A flask based sun search tool

TO DO: 
    Go Live: 
        change secret key 
        turn off debug


    Date - add a couple additional data points for date

    add flash messages

    Put text and links on map
    Change what labels show based on the zoom level of map

    Setup map to pop-up on first page and allow selection of neighborhood for autocomplete
    Put datepicker on results page

    clean up data passing in views form

    run linter
    
    setup ability to choose time

    polygon file - aquire for neihborhood - google maps has a way to apply polygon shape and make clickable

    Can set a loop to compare coordinates for closest to the central ones for neighborhood in local db?


    look into lscache - to store content on the local computer - would be good for storing weather

    utilize makefile or grunt to prepare the code and combine to push out
    look at github/pamalafox/everday/blob/master/application/urls.py - for additional ideas on user data to structure for users

    deployment

    get weather results ahead and cache

    Places API responses may include Listings provider attributions in HTML format that must be displayed to the user as provided. Put below search results 

QUESTIONS / ERROR:
    Help finding Ajax page that shows loading - jquery.post


"""

from flask import render_template, flash, redirect, session, url_for, request, jsonify
#login import
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import session as db_session, app, login_manager
# import model and assign to db_session variable
from models import Location, User
#import form objects 
from forms import LoginForm, CreateLogin
from config import G_KEY, FIO_KEY, WUI_KEY

import sun_functions
import weather_forecast
import json 

# user load callback - populates current user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# main index page
@app.route('/')
def index():
    # return redirect(url_for('search'))

    neighborhood = db_session.query(Location).all()
    l_form = LoginForm()
    
    return render_template('index.html', locations=neighborhood, l_form=l_form)

# Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = LoginForm()
    cl_form = CreateLogin()

    # login and validate the user exists in the database
    if l_form.validate_on_submit():
        user = db_session.query(User).filter(User.email==l_form.email.data).first()

        # if user exists then apply login user functionatlity to generate current_user session
        if user is not None:
            user_password = user.password
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('search'))
        else:
            flash('Incorrect Password')
            return redirect('login')
    return render_template('login.html', title="Login", l_form=l_form, cl_form=cl_form)

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
    cl_form = CreateLogin()
    l_form = LoginForm()
    neighborhood = db_session.query(Location).all()
    if cl_form.validate_on_submit():
        user = db_session.query(User).filter(User.email == cl_form.email.data).first()
        if user != None:
            user_email = user.email
            if user_email == cl_form.email.data:
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
    return render_template('create_login.html', title='Create Account Form', cl_form=cl_form, l_form=l_form, locations=neighborhood)


# FIX - view template to run Ajax spinner
@app.route("/ajax_search", methods = ['POST', 'GET'])
def ajax_search():
    # generate local neighborhood object
    neighborhood = db_session.query(Location).all()

    # # capture search form query text
    txt_query = request.form['query']
    # # catpure form date filter
    date = request.form['date']

#    date=request.args['date'] - calls through browser
#    txt_query=request.args['query']

    weather = sun_functions.search_results(G_KEY, FIO_KEY, WUI_KEY, neighborhood, date, txt_query)

    return render_template('search_result_partial.html', result=weather)
    print "hello"

# renders result page after a search 
@app.route('/search', methods=['POST'])
def search():
    # generate local neighborhood object
    neighborhood = db_session.query(Location).all()
    l_form = LoginForm() # FIX - passing to make the pages work but need to pull out of view

    txt_query = request.form['query']
    # # catpure form date filter
    date = request.form['date']

    
    return render_template('fast_result.html', locations=neighborhood, l_form=l_form, query= txt_query, date=date)


# about page
@app.route('/about')
def about():  
    neighborhood = db_session.query(Location).all()
    l_form = LoginForm()  
    return render_template('about.html', locations=neighborhood, l_form=l_form)

# terms of service page
@app.route('/tos')
def tos(): 
    neighborhood = db_session.query(Location).all()
    l_form = LoginForm()  
    return render_template('tos.html', locations=neighborhood, l_form=l_form)


# privacy policy page
@app.route('/privacy')
def privacy():    
    neighborhood = db_session.query(Location).all()
    l_form = LoginForm()  
    return render_template('privacy.html', locations=neighborhood, l_form=l_form)
    

# # create map view - set this up to test
# @app.route('/map_view')
# def map_view():
#     return render_template('map_view.html')


# create profile page view with favorites and ability report on validty of sun


# FIX - Json view - what Liz added to help with adding Ajax - need to rework
# @app.route('/some_json_route')
# def some_json():
#     return json.dumps({"thing" : "stuff"})

# runs app
if __name__ == "__main__":
    app.run(debug=True)