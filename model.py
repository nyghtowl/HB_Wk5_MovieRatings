from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types 
from sqlalchemy import Column, Integer, String, Date, ForeignKey
#sessionmaker is like sqlite3 cursor - describes how to interact with database, needs to be instantiated & scope_session handle threading issues
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref 
import correlation

# ENGINE = None 
# Session = None 

#sets a variable that will be a method to connect to ratings.db
# echo = True shows what is being written for sqlalchemy
engine = create_engine("sqlite:///ratings.db", echo=False)
# set a variable that will be used by sessionmaker to help interact with ratings.db - instead of instatiating a session class, its replaced by a session object that is always connected and safe to use directly without explicitly connecting to db
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


# the variable connecting to the declarative_base function of sqlalchemy
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here

class User(Base):
	#informs sqlalchemy that an instance of this class will be stored in user table
	__tablename__ = "users"

	id = Column(Integer, primary_key = True) # primary key written and unique 
	email = Column(String(64), nullable=True) #nullable=True means this attribute is optional
	password = Column(String(64), nullable=True)
	age = Column(Integer, nullable=True)
	zipcode = Column(String(15), nullable=True)

	# setup pearson correlation analysis
	def similarity(self, other):
		#set an empty dict and list
		u_ratings = {}
		paired_ratings = []
		# for each rating for self, place in dict under index of movie id
		for r in self.ratings:
			u_ratings[r.movie_id] = r

		# for each rating for 2nd user, get the rating for that movie id out of dict 
		for r in other.ratings:
			u_r = u_ratings.get(r.movie_id)
			# if there is a rating append it to the list as a pair of self and 2nd user ratings
			if u_r:
				paired_ratings.append( (u_r.rating, r.rating) )

		# if there is info in paired_rating list then run the pearson correlation function
		if paired_ratings:
			return correlation.pearson(paired_ratings)
		# else return 0
		else:
			return 0.0

	# setup a prediction method that takes in a user object and a movie object
	def predict_rating(self,movie):
		# set rating variable to capture the ratings from user
		ratings = self.ratings
		# set variable to all rating objects that relate to movie
		other_ratings = movie.ratings
		# create list of each user object pulling from those that rated the movie leveraging a list comprehension for loop
		other_users = [r.user for r in other_ratings]
		# run a similarity method on each user pulled from other users list and compare to the initial user. Create a tuple of the other user object and the compared pearson rating. This looks at similarity coefficient of user instance.
		similarities = [(self.similarity(other_user), other_user) for other_user in other_users]
		# sort the list of tuples with the highest value at the top
		similarities.sort(reverse = True)
		# assign the first tuple element in the list to top user
		top_user = similarities[0]

		# pull each rating out of movie rating list
		matched_rating = None
		for rating in other_ratings:
			# if the user_id maches the top_user.user_id (object in the 2nd position of the index)
			if rating.user_id == top_user[1].id:
				# set the current rating object to matched_rating
				matched_rating = rating
				break
		# return the rating out of the matched_rating object and multiply wtih top_user - this is the prediction
		return matched_rating.rating * top_user[0]

	# better prediction by blending users and make tuple composed of similarity coefficient and rating
	def predict(self, movie):
		ratings = self.ratings
		other_ratings = movie.ratings
		# creates coefficient tuple coupled with rating
		similarities = [(self.similarity(r.user), r) for r in other_ratings]
		similarities.sort(reverse = True)
		
		'''
		# this uses the r mapped to coefficient but the answer is still the same
		top_user = similarities[0]
		# no additional loop since ratings are already mapped by user
		# returns the rating object out of the tope user times the matched rating
		return top_user[1].rating * top_user[0]
		'''
		'''
		# alternative to blend results and get weighted average with weighted mean
		# instead of summing all the ratings and dividing by number of ratings, this gives more weight to users that are similar
		# r is the rating object and similarity the related coefficient
		numer = sum([r.rating * similarity for similarity, r in similarities]) 
		denom = sum([similarity[0] for similarity in similarities])
		return numer/denom
		'''

		# additional alternative to help account and remove negative numbers
		similarities = [sim for sim in similarities if sim[0] > 0]
		if not similarities:
			return None
		num = sum([r.rating * similarity for similarity, r in similarities])
		den = sum([similarity[0] for similarity in similarities])
		return num/den

class Movie(Base):
	#connect to the table named movies and put information in that table
	__tablename__ = "movies"

	id = Column(Integer, primary_key=True)
	title = Column(String(255))
	release_at = Column(Date, nullable=True) # importing release date as a string & converting to datetime
	imdb = Column(String(64))

	# will print out the movie information to see if it works
	def __repr__(self):
		return u"<Movie: %d %s>"%(self.id, unicode(self.name))


class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key=True)
	#ForeignKey sets relationship and references a with the other tables - table.column_name
	user_id = Column(Integer, ForeignKey("users.id"))
	movie_id = Column(Integer, ForeignKey("movies.id"))
	rating = Column(Integer)

	# establishes relationshiop between Rating and User objects along with backref - only need to do it once to connect both
	user = relationship("User", backref=backref("ratings", order_by=id))
	movie = relationship("Movie", backref=backref("ratings", order_by=id))

	# sqlalchemy writes the init function - if we write it then it overwrites and gets odd results
	# use named parameters email = ... 



### End class declarations

def main():
    """In case we need this for something"""
    # creates the database
    engine = create_engine("sqlite:///ratings.db", echo=True)
    # Base is a class that all the objects inherit from, metadata is table schema, create_all makes the table
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()

# removing the connect function because have applied sessionmaker above
# def connect(): #function that connects engine to database, creates our session & interacts with database; see above comments at "ENGINE" & "Session" variables
# 	# global ENGINE # global says it wants to access the var outside
# 	# global Session
# 	# session = sessionmaker(bind=engine)
# 	return session() # this instantiates our session