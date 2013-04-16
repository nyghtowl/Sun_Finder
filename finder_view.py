"""
finder_view.py -- A flask based sun search tool

TO DO: 
	Go Live: 
		change secret key 
		turn off debug

QUESITONS:


"""

from flask import Flask, render_template, request, redirect, url_for, session, flash

# import data_model // when it is built

# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
app.secret_key = 'key'

# app.config.from_object(__name__) - allows for setting all caps var as global var
# eg: SECRET_KEY = "bbbb"

@app.route('/')
def index():
	return render_template('index.html')

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
	return render_template('search.html')

# create actual search function to enter the name of the location
@app.route('/search', methods=['POST'])
def search():
	# capture the query request from the form into a variable
	question = request.form['query']
	print question
	# confirm the infromation captured matches model; otherwise throw error and ask to search again - do through javasript
	# submit the query to the data model file to match lat & long to the name of location and then pull from app to determine weather information
	# return the results template
	return redirect(url_for('fast_result'))

# create view that will show simple sun result from search
@app.route('/fast_result')
def fast_result():
	return render_template('fast_result.html')


# create an extend result view with weather details and map view
# create map view
# create login view
# create profile page view with favorites and ability report on validty of sun

# runs app
if __name__ == "__main__":
	app.run(debug=True)