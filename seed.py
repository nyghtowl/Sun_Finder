"""
seed.py is the file to use to setup the databases

Go Live: Add this and database info to gitignore

"""
import sun_model
import csv

def load_location(session):
	# open file as an object
	loc_file = open('data/location.txt')
	# split based on space or tab into a reader object containing lists of strings for each row
	loc_obj = csv.reader(loc_file, delimiter="|")
	# pull each row and assign and store based on data labels 
	for row in loc_obj:
		store_content = sun_model.Location(id=row[0], lati=row[1], longi=row[2], n_hood=row[3])
		# adds the content to the db session
		session.add(store_content)


# seeds the databased with the data
def main(session):
	load_location(session)
	# commits changes to the db
	session.commit()

# runs if seed is loaded with python first
if __name__ == "__main__":
	session = sun_model.connect()
	main(session)
