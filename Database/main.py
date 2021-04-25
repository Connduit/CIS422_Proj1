"""
Author: Connor Finch
Created on: 4/16/2021
Database: Takes in user input from a website and organizes it into a dictionary database


$env:FLASK_APP = "main.py"


"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sorting_system import distance, age, job, health, priority

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_BINDS"] = {"providers": "sqlite:///providers.db"}

db = SQLAlchemy(app)

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

class Provider(db.Model):
    __bind_key__ = "providers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)


@app.route("/")
def index():
    title = "TITLE GOES HERE"
    return render_template("index.html", title=title)

@app.route("/userform")
def userform():
    title = "userform"
    return render_template("userform.html",title=title)

@app.route("/username", methods=["POST"])
def username():
    title = "username"
    fn = request.form.get("fname")
    ln = request.form.get("lname")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    job = request.form.get("job")
    age = request.form.get("age")
    health = request.form.get("health")

    if request.method == "POST":
        new_user = User(first_name=fn, last_name=ln, city=city, state=state, address=address, job=job, age=age, health=health)
        try:
            db.session.add(new_user)
            db.session.commit()
            #return redirect("/")
            return render_template("username.html", title=title, first=fn,last=ln,id=new_user.id)
        except:
            return "FAILED TO ADD USER TO DATABASE"


@app.route("/retrieval")
def retrieval():
    title = "retrieval"
    return render_template("retrieval.html",title=title)



@app.route("/output", methods=["POST"])
def output():
    title = "output"
    username = request.form.get("username")
    user_id = int(username[-1])
    user = User.query.get(user_id)

    """sorting_system is called here"""
    try:
        user_state = user.state.lower()
    except:
        return "INVALID USERID"

    providers = Provider.query.filter_by(state=user_state).all()
    d = distance(user.address, providers)

    prio = priority(job(user.job) + age(int(user.age)) + health(user.health))
    return render_template("output.html", title=title, dist=d, prio=prio)



def buildProviderDB(filename):
    with open(filename) as file:
        for line in file:
            name = line.strip()
            address = next(file)
            address = address.split(",")
            state = address[2].strip()
            state = state[:state.index(" ")].lower()
            address = address[0].strip()
            new_provider = Provider(name=name, state=state, address=address)
            try:
                db.session.add(new_provider)
                db.session.commit()
            except:
                pass 




if __name__ == "__main__":
    newProviders = False
    filename = "vaccine_location.txt"
    if newProviders:
        buildProviderDB(filename)
    app.run()