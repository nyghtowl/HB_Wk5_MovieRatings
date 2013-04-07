# Query code for Ratings exercise - long form for query

def qMovieTitle():
	# sets var equal to query return where select * from user table -ref User object in model and pull based on id so say where id = 35 which returns an object
	user = session.query(model.User).get(35)
	# sets var to capture results from select * from rating object / ratings table where / filter_by user_id = user.id (which is hte object user and id is an attirbute) and filter for all .all() which returns a list of objects/instances
	ratings = session.query(model.Rating).filter_by(user_id=user.id).all()
	# sets an empty list
	movies = []
	for r in ratings:
		# capture query results to pull from Movie object, movies table and get for each object/instance in ratings list apply the movie_id method to get the string result
		movie = session.query(model.Movie).get(r.movie_id)
		# append results of movie into movies list
		movies.append(movie)

	# print each results in the movies list
	for m in movies:
		print m.title

# above is the long form of the query that is complex in the number of steps it runs. Joins makes this easier

# below is the query once the Rating and User objects / tables are joined with Foreign Keys and relation & backref 
def qMovieTitleShort():
	# queries the Rating table and gets a rating object at id 1
	r = session.query(Rating).get(1)
	# set a variable based on the r object with the specific user related object
	u = r.user
	#prints the age, zip attributes off the user object set to u
	print u.age
	print u.zipcode
	# prints a list of all related rating objects to that user object at that user id
	print u.ratings
	# prints the first rating object out of the list and related id
	print u.ratings[0].id
	#prints the first rating object in the list and related user & movie id
	print u.ratings[0].user_id
	print u.ratings[0].movie_id
	# r object is the same as u object from user with the first rating object in the list
	r == u.ratings[0]
