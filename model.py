from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types 
from sqlalchemy import Column, Integer, String, Date, ForeignKey
#sessionmaker is like sqlite3 cursor - describes how to interact with database, needs to be instantiated & scope_session handle threading issues
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref 

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