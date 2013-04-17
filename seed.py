"""
seed.py is the file to use to setup the databases

Go Live: Add this and database info to gitignore

"""
import sun_model
import csv

def load_coord(session):
	# open file as an object
	coord_file = open('data/coordinates.txt')
	# split based on space or tab into a reader object containing lists of strings for each row
	coord_obj = csv.reader(coord_file, delimiter="|")
	# pull each row and assign and store based on data labels 
	for row in coord_obj:
		store_content = sun_model.Coordinates(id=row[0], lati=row[1], longi=row[2], n_hood=row[3])
		# adds the content to the db session
		session.add(store_content)


# seeds the databased with the data
def main(session):
	load_coord(session)
	# commits changes to the db
	session.commit()

# runs if seed is loaded with python first
if __name__ == "__main__":
	session = sun_model.connect()
	main(session)
