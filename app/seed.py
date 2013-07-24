"""
seed.py is the file to use to setup the databases

Go Live: Add this and database info to gitignore

"""
from app import db
from app import models
import csv

def load_location():
	# open file as an object
	loc_file = open('data/location.txt')

	# split based on space or tab into a reader object containing lists of strings for each row
	loc_obj = csv.reader(loc_file, delimiter="|")
	# pull each row and assign and store based on data labels 
	for row in loc_obj:
		store_content = models.Location(id=row[0], lat=row[1], lng=row[2], rad=row[3], n_hood=row[4])
		# adds the content to the db db_session
		db.session.add(store_content)


# seeds the databased with the data
def main():
	load_location()
	# commits changes to the db
	db.session.commit()

# runs if seed is loaded with python first
if __name__ == "__main__":
	main()
