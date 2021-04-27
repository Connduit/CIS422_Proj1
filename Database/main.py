"""
Author: Connor Finch
Created on: 4/16/2021
Brief Description:
    This program calculates the closest vaccination location for 
    a given user and is able to provide its name, address, and 
    distance away from the user. 
"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sorting_system import distance, age, job, health, priority


""" Defining the databases that will be used in this program """
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_BINDS"] = {"providers": "sqlite:///providers.db"}
db = SQLAlchemy(app)


""" Class that handles the formmating of the User's database """
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    job = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    health = db.Column(db.String(50), nullable=False)


""" Class that handles the formmating of the Provider's database """
class Provider(db.Model):
    __bind_key__ = "providers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    full_address = db.Column(db.String(200), unique=True, nullable=False)


"""
This function handles the homepage of the website which can be see in 
'index.html'. It is the first page on the website that a user will see.
"""
@app.route("/")
def index():
    title = "TITLE GOES HERE"
    return render_template("index.html", title=title)


"""
This function handles the userform page of the website which can be see in 
'userform.html'. This page is where a user can fill out their information 
which is then enter into the users.db database.
"""
@app.route("/userform")
def userform():
    title = "userform"
    return render_template("userform.html",title=title)


"""
This function handles the username page of the website which can be see in 
'username.html'. This page displays the given user's username after they 
submit their information via the userform page.
"""
@app.route("/username", methods=["POST"])
def username():
    title = "username"

    """ Retrieving the information a user has entered. """
    fn = request.form.get("fname")                          # The user's first name
    ln = request.form.get("lname")                          # The user's last name
    city = request.form.get("city")                         # The city the user lives in
    state = request.form.get("state")                       # The state the user lives in
    address = request.form.get("address")                   # The user's street address
    job = request.form.get("job")                           # Is the user a healthcare worker/first responder? (y/n)
    age = request.form.get("age")                           # The user's age
    health = request.form.get("health")                     # Does the user have preexisting health conditions? (y/n)

    """
    The outter most if statement isn't necessary but gives the option add a "GET" 
    method for debugging purposes.
    """
    if request.method == "POST":
        """ Creates a new User object in order to be added and committed to the User database """
        new_user = User(first_name=fn, last_name=ln, city=city, state=state, address=address, job=job, age=age, health=health)
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("username.html", title=title, first=fn,last=ln,id=new_user.id)
        except:
            return "FAILED TO ADD USER TO DATABASE"


"""
This function handles the retrieval page of the website which can be see in 
'retrieval.html'. This page allows a user to enter their username in order to 
obtain the nearest vaccination provider and the user's vaccination priority
"""
@app.route("/retrieval")
def retrieval():
    title = "retrieval"
    return render_template("retrieval.html",title=title)


"""
This function handles the retrieval page of the website which can be see in 
'output.html'. This function calls the functions defined in sorting_system.py.
This is where the main/heavy computations are called and performed.
"""
@app.route("/output", methods=["POST"])
def output():
    title = "output"
    username = request.form.get("username")
    user_id = int(username[-1])                                                 # Obtain the user's id since it's the last character of their username
    user = User.query.get(user_id)                                              # Retrieve the given user from the User database using their user id

    """ The calls to sorting_system.py begin here """
    try:
        user_state = user.state.lower()                                         # Try/except block needed because if a user DNE then user.state will equal None
    except:
        return "INVALID USERID"

    providers = Provider.query.filter_by(state=user_state).all()                # Retrieve every vaccination location that is in the same state as the user

    """
    If there are no vaccination locations in the user's state, pull every 
    vaccination location avalible (NOT EFFICIENT AT ALL).
    """
    if len(providers) == 0:
        providers = Provider.query.order_by(Provider.id).all()

    """
    Finds the name, address, and distance away of the closest vaccination location 
    to the user.
    """
    d = distance(f"{user.address} {user.city}", providers).split(":")
    name, faddress, dist = d[0].strip(), d[1].strip(), d[2].strip()

    prio = priority(job(user.job) + age(int(user.age)) + health(user.health))   # Finds the user's vaccination priority
    return render_template("output.html", title=title, name=name, address=faddress,dist=dist, prio=prio)


""" This function builds the vaccine provider database """
def buildProviderDB(filename):
    with open(filename) as file:
        for line in file:
            name = line[:line.index("-")].strip()
            full_address = next(file).strip()
            full_list = full_address.split(",")
            street_address = f"{full_list[0]}{full_list[1]}"
            state = full_list[2].strip()
            state = state[:state.index(" ")].lower()
            new_provider = Provider(name=name, state=state, address=street_address, full_address=full_address)
            try:
                db.session.add(new_provider)
                db.session.commit()
            except:
                pass                                                            # Pass if the provider is already in the database 


if __name__ == "__main__":
    """ Add to the provider's database if there are new providers """
    newProviders = False
    filename = "vaccine_location.txt"                                           # Textfile that contains the names and locations of vaccination providers
    if newProviders:
        buildProviderDB(filename)
    app.run()