from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types #need types for datetime
from sqlalchemy import Column, Integer, String
import datetime #have to import datetime for timestamp column in ratings
from sqlalchemy.orm import sessionmaker #like sqlite3 cursor - describes how to interact with database, needs to be instantiated

ENGINE = None #sets a variable that will be a method to connect to ratings.db
Session = None # set a variable that will be used by sessionmaker to help interact with ratings.db

# the variable connecting to the declarative_base function of sqlalchemy
Base = declarative_base()

### Class declarations go here

class User(Base):
	#informs sqlalchemy that an instance of this class will be stored in user table
	__tablename__ = "users"

	id = Column(Integer, primary_key = True) # primary key written and unique 
	email = Column(String(64), nullable=True) #nullable=True means this attribute is optional
	password = Column(String(64), nullable=True)
	age = Column(Integer, nullable=True)
	zipcode = Column(String(15), nullable=True)


class Movies(Base):
	#informs sqlalchemy that an instance of this class will be stored in "movies" table
	__tablename__ = "movies"

	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	release_at = Column(types.DateTime()) # imported from sqlalchemy (notes above)
	imdb_url = Column(String(64))


class Ratings(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	movie_id = Column(Integer)
	rating = Column(Integer)




	# sqlalchemy writes the init function - if we write it then it overwrites and gets odd results
	# use named parameters email = ... 

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

def connect(): #function that connects engine to database, creates our session & interacts with database; see above comments at "ENGINE" & "Session" variables
	global ENGINE
	global Session

	ENGINE = create_engine("sqlite:///ratings.db", echo=True)
	Session = sessionmaker(bind=ENGINE)

	return Session() # this instantiates our session