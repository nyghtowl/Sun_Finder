"""
Sun Finder View -- Flask based sun search tool

TO DO: 
    Change setup of static assets for postgres

    Map - Possibly change to popover if can fix problem
        Put text and links on map - populate autocomplete based on click
        Change what labels show based on the zoom level of map

    Add TDD

    Weather Data - change returned data to populate page through jason & remove fui

    Date - add a couple additional data points for date
        setup ability to choose time

    run linter

    look into lscache - to store content on the local computer - would be good for storing weather
    get weather results ahead and cache

    utilize makefile or grunt to prepare the code and combine to push out
    look at github/pamalafox/everday/blob/master/application/urls.py - for additional ideas on user data to structure for users


    Places API responses may include Listings provider attributions in HTML format that must be displayed to the user as provided. Put below search results 

"""

from flask import render_template, flash, redirect, session, url_for, request, jsonify, g
from app import db, app, login_manager
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import Location, User
from forms import LoginForm, CreateLogin

import sun_functions
import weather_forecast
import json 

# User load callback - populates current user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# FIX - build out for user
# @app.before_request
# def before_request():
#     g.user = current_user

#     # Updated database with the last time user seen
#     if g.user.is_authenticated():
#         g.user.last_seen = datetime.utcnow()
#         db.session.add(g.user)
#         db.session.commit()

# @app.after_request
# def after_request(response):
#     for query in get_debug_queries():
#         if query.duration >= DATABASE_QUERY_TIMEOUT:
#             app.logger.warning('SLOW QUERY: %s\nParameters: %s\nDuration: %fs\Context: %s\n') % (query.statement, query.parameters, query.duration, query.context)
#     return response

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = LoginForm()

    # Validate login
    if l_form.validate_on_submit():
        user = User.query.filter(User.email==l_form.email.data).first()
 
        # If user exists then apply login user functionatlity to generate current_user session
        if user is not None:
            user_password = user.password
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('search'))
        else:
            flash('Your email or password are incorrect. Please login again.')
    return render_template('login.html', l_form=l_form)

@app.route('/logout')
@login_required # Confirms login
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('index'))


@app.route('/create_login', methods = ['POST', 'GET'])
def create_login():
    cl_form = CreateLogin()

    if cl_form.validate_on_submit():

        user = User.query.filter(User.email==cl_form.email.data).first()

        if user != None:
            user_email = user.email
            if user_email == cl_form.email.data:
                flash ('%(email)s already exists. Please login or enter a different email.', email = user_email)
                return redirect(url_for('login'))
        # If user doesn't exist, save from data in User object to commit to db
        if user == None:
            new_user = User(id = None,
                        email=form.email.data,
                        password=form.password.data,
                        fname=form.fname.data,
                        lname=form.lname.data,
                        mobile=form.mobile.data,
                        zipcode=form.zipcode.data,
                        # FIX - don't need to save this - can be assumed since required on form
                        accept_tos=True,
                        timestamp=time.time())
            db.session.add(new_user)
            db.session.commit()
            flash('Account creation successful. Please login to your account.')
            return redirect(url_for('index'))
    return render_template('create_login.html', cl_form=cl_form)

# Search shell
@app.route('/search', methods=['POST'])
def search():
    return render_template('result_shell.html')


# Ajax spinner replacement
@app.route("/search_results_partial", methods = ['POST'])
def search_results_partial():
    print 'in weather results'
    # Local neighborhood object
    neighborhoods = Location.query.all()
    print 'search neighborhood', neighborhoods

    # Search form input
    txt_query = request.form['query']
    # Captures date format yy-mm-dd as string
    date = request.form['date']

    print 'search query', txt_query

    weather = sun_functions.search_results(neighborhoods, date, txt_query)
 
    return render_template('search_results_partial.html', result=weather)
 
# FIX - working to build and pass - mostly handled with JS
@app.route('/map_details', methods = ['GET'])
def map_details():
    # generate local neighborhood object
    neighborhoods = Location.query.all()

    # print 'loc list', [nh.n_hood for nh in neighborhoods]
    # print 'coord', [(nh.lat,nh.lng) for nh in neighborhoods]

    return json.dumps({'result': {'locations': [nh.n_hood for nh in neighborhoods], 'loc_coords': [[nh.lat,nh.lng] for nh in neighborhoods] }})

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

# Search form load
@app.route('/form_index_partial', methods=['GET'])
def form_index_partial():    
    return render_template('form_index_partial.html')

@app.route('/form_top_partial', methods=['GET'])
def form_top_partial():    
    return render_template('form_top_partial.html')



# User view with favorites and ability to report on validity of sun
# @app.route('/user/<fname>')
# @login_required # Restricts page access without login
# def user(fname):
#     user = User.query.filter_by(User.fname = fname).first()

#     if user == None:
#         flash('User %(fname)s not found.', fname = fname))
#         return redirect(url_for('index'))
#     return render_template("user.html", 
#         user = user)

# @app.route('/edit', methods = ['GET', 'POST'])
# @login_required
# def edit():
#     form = EditForm(g.user.nickname)
#     if form.validate_on_submit():
#         g.user.nickname = form.fname.data
#         g.user.about_me = form.about_me.data
#         db.session.add(g.user)
#         db.session.commit()
#         flash(gettext('Your changes have been saved.'))
#         return redirect(url_for('edit'))
#     elif request.method != "POST":
#         form.nickname.data = g.user.nickname
#         form.about_me.data = g.user.about_me
#     return render_template('edit.html', form = form)