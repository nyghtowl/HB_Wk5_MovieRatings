"""
judgement.py -- A flask-based ratings list
"""

#Added session, url_for, escape for username login and g for global variables
# adding request is accessing the request object and same for redirect
from flask import Flask, render_template, request, redirect, url_for, session
# connect to model
import model

#initializes program to be a Flask application
app = Flask(__name__)
# in order to use session, a secret key is needed
app.secret_key = "key"

@app.route("/index")
def index():
	# pull the user_id from the session
	user_id = session.get("user_id", None)
	return redirect(url_for("list_users", id = user_id))

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
	# need to validate that the info exists otherwise send back to login

	#capture the email from the form and apply to session
	session['email'] = request.form['email']
	#capture id out of the user_info object and assign to session
	session['user_id'] = user_info.id

	# after getting the session variable back, you have to point it to a page
	return redirect("/index")

# logout a user
@app.route("/logout")
def logout():
	#del session['user_id']
	session.pop('email',None)
	session.pop('user_id',None)
	return redirect(url_for('login'))

# We should be able to click on a user and view the list of movies they've rated, as well as ratings
# generate a ratings page based on users id
@app.route("/view_ratings/<id>")
# id = None in case there is no id
def view_ratings(id=None):
	# sets sql query to pull ratings based on user id
	user_ratings = model.session.query(model.Rating).filter_by(user_id=id).limit(5).all()
	# return a page of the user ratings by passing the queried information in user_ratings object
	return render_template("view_ratings.html", ratings = user_ratings)


# We should be able to view a list of all users
# Note you can pass id through view and funciton or through calling the session
@app.route("/list_users/<id>")
def list_users(id=None):
	user_email = session.get("email", None)
	user_list = model.session.query(model.User).limit(5).all()
	#user_list = model.session.query(model.User).all()
	return render_template("user_list.html", user_list = user_list, user_email = user_email)

# We should be able to, when logged in and viewing a record for a movie, either add or update a personal rating for that movie
#@app.route("/add_rating")

if __name__ == "__main__":
	# turn on Flask debug mode- browser does a traceback in browser
	app.run(debug=True)