"""
Sun Finder View -- Flask based sun search tool

TO DO: 
    
    TDD & OOP

    Rework results page format and add more weather details

    Map -
        Put links on map 
        Provide weather details within a radius of the search item
        Store weather searches in Redis for the day

    Setup SSL
    Add Oauth

    Move Login back to modal format

    Lock down format of user mobile info to enable Twillio

    Date/Time - setup ability to choose time

    run linter

    store searched weather results to leverage if searched again

    utilize makefile or grunt to prepare the code and combine to push out

    look at github/pamalafox/everday/blob/master/application/urls.py - for additional ideas on user data to structure for users


    Places API responses may include Listings provider attributions in HTML format that must be displayed to the user as provided. Put below search results 

    Simple
        change out presidio coord
        remove the print date in weather object and use javascript to print

"""

from flask import render_template, flash, redirect, session, url_for, request, jsonify, g
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import db, app, login_manager
from app.models import Location, User, ROLE_USER
from datetime import datetime
import time
from forms import LoginForm, CreateLogin, EditForm
from config import DATABASE_QUERY_TIMEOUT

import sun_functions
import unicodedata
import json 

# User load callback - populates current user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

    # Updated database with the last time user seen
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning('SLOW QUERY: %s\nParameters: %s\nDuration: %fs\Context: %s\n') % (query.statement, query.parameters, query.duration, query.context)
    return response

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('user', user=g.user))

    l_form = LoginForm()

    # Validate login
    if l_form.validate_on_submit():
        session['remember_me'] = l_form.remember_me.data
        user = User.query.filter(User.email==l_form.email.data).first()
 
        # If user exists then apply login user functionatlity to generate current_user session
        if user is not None:
            submitted_pwd = l_form.password.data
            if user.check_password(submitted_pwd):
                if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
                login_user(user, remember=remember_me)
                flash('Logged in successfully.',category="success")
                return redirect(url_for('index'))
            else:
                flash('Your password is incorrect. Please login again.', category="error")
        else:
            flash('Your email is incorrect or does not exist. Please login again.', category="error")
    return render_template('login.html', l_form=l_form)

@app.route('/logout')
@login_required # Confirms login
def logout():
    logout_user()
    flash('You are now logged out', category="success")
    return redirect(url_for('index'))


@app.route('/create_login', methods = ['POST', 'GET'])
def create_login():
    cl_form = CreateLogin()

    if cl_form.validate_on_submit():
        session['remember_me'] = cl_form.remember_me.data
        user = User.query.filter(User.email==cl_form.email.data).first()

        if user != None:
            user_email = user.email
            if user_email == cl_form.email.data:
                flash ('Email already exists. Please login or enter a different email.', category="warning")
                return redirect(url_for('login'))
        # If user doesn't exist, save from data in User object to commit to db
        if user == None:
            new_user = User(id = None,
                        email=cl_form.email.data,
                        password=User.set_password(cl_form.password.data),
                        fname=cl_form.fname.data,
                        lname=cl_form.lname.data,
                        mobile=cl_form.mobile.data,
                        zipcode=cl_form.zipcode.data,
                        # FIX - don't need to save this - can be assumed since required on form
                        accept_tos=True,
                        date_created=time.time(),
                        role=ROLE_USER)
            db.session.add(new_user)
            db.session.commit()
            flash('Account creation successful. Please login to your account.', category="success")
            if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
            login_user(new_user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template('create_login.html', form=cl_form)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    e_form = EditForm()
    if e_form.validate_on_submit():
        g.user.fname = e_form.fname.data
        g.user.bio = e_form.bio.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.', category="success")
        return redirect(url_for('user', user=g.user))
    elif request.method != "POST":
        e_form.fname.data = g.user.fname
        e_form.bio.data = g.user.bio
    return render_template('edit.html', form=e_form)

# Search shell
@app.route('/search', methods=['POST', 'GET'])
def search():
    # Search form input
    txt_query = str(request.form['query'])
    print 'search query', txt_query

    # Captures user-entered date format mm-dd-yy as string
    user_picked_time = request.form['date']
    
    print 'user picked time', type(user_picked_time)

    user_coord_unicode = request.form['user_coord']

    if user_coord_unicode:
        user_coord = unicodedata.normalize('NFKD', user_coord_unicode).encode('ascii','ignore')
    else:
        user_coord = None
    
    print 'user coord in search', user_coord
    # Get weather data
    weather = sun_functions.search_results(txt_query, user_picked_time, user_coord)

    print 'weather result in search', weather

    if not weather:
        flash("%s not found. Please try your search again." % txt_query, category="error")
        return redirect(url_for('index'))
 
    return render_template('search_results_partial.html', result=weather)
 

@app.route('/map_details', methods = ['GET'])
def map_details():
    # generate local neighborhood object
    neighborhoods = Location.query.all()
    
    daily_weather = sun_functions.daily_weather_report(neighborhoods) 

    if daily_weather == []:
        return ""
    else:
        return json.dumps({'locations':daily_weather})


@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    txt_so_far = None

    # Pull letters entered so far
    if request.method == 'POST':
        txt_so_far = str(request.form['msg'])

    # Lookup locations to recommend based on prefix
    if txt_so_far:
        txt_so_far = txt_so_far.capitalize() # Ensures all search on capitlalized letters
        locations = Location.query.filter(Location.n_hood.startswith(txt_so_far)).limit(8)         
        print locations
        predictions = [location.n_hood for location in locations]
        print predictions
    else:
        predictions = []

    return json.dumps({ "options": predictions})


@app.route('/about')
def about():  
    return render_template('about.html')

# Terms of service
@app.route('/tos')
def tos(): 
    return render_template('tos.html')


# Privacy policy
@app.route('/privacy')
def privacy():    
    return render_template('privacy.html')


# User view with favorites and ability to report on validity of sun
@app.route('/user/<fname>')
@login_required # Restricts page access without login
def user(fname):
    user = User.query.filter(User.fname == fname).first()

    if user == None:
        flash('User %(fname)s not found.', fname=fname, category="error")
        return redirect(url_for('index'))
    return render_template("user.html", 
        user=user)

