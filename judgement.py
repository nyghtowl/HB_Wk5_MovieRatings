"""
judgement.py -- A flask-based ratings list
"""

#Added session, url_for, escape for username login and g for global variables
# adding request is accessing the request object and same for redirect
from flask import Flask, render_template, request, redirect, url_for, session, flash
# connect to model
import model

#initializes program to be a Flask application
app = Flask(__name__)
# in order to use session, a secret key is needed to keep client side session secure
app.secret_key = "key"
# initialize application with config and from_object will import the object if its a string
app.config.from_object(__name__)

@app.route("/index")
def index():
	# pull the user_id from the session
	user_id = session.get("user_id", None)
	# generate random list of users template
	return redirect(url_for("list_users"))

# generate the create_user page to capture user information (email, password, age, zipcode)
@app.route("/create_user")
def create_user():
	return render_template("create_user.html")

# save information entered on create_user form
@app.route("/save_user", methods=["POST"])
def save_user():
	# query to see if the user is in the db

	# capture the input from the form
	new_email = request.form['email']
	new_password = request.form['password']
	new_age = request.form['age']
	new_zip = request.form['zipcode']

	# apply the content of the form to model.User
	new_user = model.User(email = new_email, password = new_password, age = new_age, zipcode = new_zip)
	# add the object to a session
	model.session.add(new_user)
	# commit/save the information into db session.commit
	model.session.commit()

	return redirect(url_for("index"))

# We should be able to log in as a user
@app.route("/login", methods=['GET'])
def login():
	return render_template("login.html")

# create view called authenticate
@app.route("/authenticate", methods=["POST"])
def authenticate():
	user_email = request.form['email']
	user_password = request.form['password']
	
	#check model-db for user information and create an object of that information
	user_info = model.session.query(model.User).filter_by(email = user_email, password = user_password).first()
	
	# validate that the info exists otherwise send back to login
	if user_info:
		#capture the email from the form and apply to session - alternative request.form['email']
		session['email'] = user_info.email
		#capture id out of the user_info object and assign to session
		session['user_id'] = user_info.id
		flash('Logged in as:' + user_email)
		# ratings = user_info.ratings
		# ratings = model.session.query(model.Rating).filter_by(user_id=user_info.id).all()
		return redirect(url_for('user_ratings', id=user_info.id))
	else:
		#post message on screen if username or password are incorret
		flash('Invalid username or password', 'error')
		return redirect(url_for('login'))

	# after getting the session variable back, you have to point it to a page
	# return redirect(url_for("index"))

# logout a user
@app.route("/logout")
def logout():
	#del session['user_id']
	session.pop('email',None)
	session.pop('user_id',None)
	return redirect(url_for('index'))

# We should be able to view a list of all users
# Note you can pass id through view and funciton or through calling the session
@app.route("/list_users")
def list_users():
	#capture user email if it exists in a session
	user_email = session.get('email', None)
	#user_email = session.get("email", None)
	user_list = model.session.query(model.User).limit(5).all()

	#user_list = model.session.query(model.User).all()
	return render_template("list_users.html", user_list = user_list, user_email = user_email)
	

# We should be able to click on a user and view the list of movies they've rated, as well as ratings
# generate a ratings page based on users id
@app.route("/user_ratings/<int:id>")
# id = None in case there is no id
def user_ratings(id=None):
	user_email = session.get('email', None)
	if user_email:
		flash('Click movie link to review ratings.', 'message')
	else:
		flash('Login to update ratings.', 'warning')
	# sets sql query to pull ratings based on user id
	user = model.session.query(model.User).get(id)
	# ratings = model.session.query(model.Rating).filter_by(user_id=id).all()
	# return a page of the user ratings by passing the queried information in user object
	return render_template("user_ratings.html", user=user)

# View all ratings for a specific movie & note the int:id confirms id is type int
@app.route("/movie_ratings/<int:id>")
# id = None in case there is no id
def movie_ratings(id=None):
	user_id = session.get('user_id', None)
	# query for the object of whether the user rated this movie
	user_rating_query = model.session.query(model.Rating).filter_by(user_id=user_id,movie_id=id).first()
	# sets sql query to pull ratings based on movie id
	movie = model.session.query(model.Movie).get(id)
	
	if user_rating_query:
		flash('You\'ve rated this movie as follows:' + user_rating_query.rating)
		# return a page of the user ratings by passing the queried information in movie object
		return render_template("movie_ratings.html", movie = movie, rating = user_rating_query)
	else:
		flash('Do you want to rate this movie?', 'message')
		# return a page of the user ratings by passing the queried information in movie object
		return render_template("movie_ratings.html", movie = movie)

# We should be able to, when logged in and viewing a record for a movie, either add or update a personal rating for that movie
#@app.route("/add_rating")

@app.route('/rate_movie/<int:id>', methods=['POST'])
def rate_movie(id):
	user_id = session['user_id']
	rating_submitted = int(request.form['rating_select'])

	log_rating = model.Rating(user_id = user_id, movie_id = id, rating = rating_submitted)
	model.session.add(log_rating)
	model.session.commit()


	return redirect(url_for('user_ratings', id = user_id))


if __name__ == "__main__":
	# turn on Flask debug mode- browser does a traceback in browser
	# never leave this on when on a production system because allows users to execute code on server
	app.run(debug=True)