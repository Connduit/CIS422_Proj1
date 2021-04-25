"""
Author: Connor Finch
Created on: 4/16/2021
Database: Takes in user input from a website and organizes it into a dictionary database


$env:FLASK_APP = "main.py"


"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sorting_system import distance

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

    def __repr__(self):
        return f"first name = {self.first_name}, last name = {self.last_name}, city = {self.city}, state = {self.state}, address = {self.address}, job = {self.job}, age = {self.age}, id = {self.id}"
        #return f"Your username is {self.first_name}{self.last_name}{self.id}"

class Provider(db.Model):
    __bind_key__ = "providers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.name},{self.address}"


@app.route("/")
def index():
    title = "TITLE GOES HERE"
    return render_template("index.html", title=title)

@app.route("/userform")
def userform():
    title = "userform"
    return render_template("userform.html",title=title)

@app.route("/database", methods=["POST","GET"])
def database():
    title = "database"
    fn = request.form.get("fname")
    ln = request.form.get("lname")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    job = request.form.get("job")
    age = request.form.get("age")


    if request.method == "POST":
        new_user = User(first_name=fn, last_name=ln, city=city, state=state, address=address, job=job, age=age)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/database")
        except:
            return "FAILED TO ADD USER TO DATABASE"
    else:
        all_users = User.query.order_by(User.id)
        return render_template("database.html",title=title, users=all_users)


@app.route("/delete/<int:id>")
def delete(id):
    user_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect("/database")
    except:
        return "FAILED TO DELETE USER FROM DATABASE"

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
    user_state = user.state.lower()
    providers = Provider.query.filter_by(state=user_state).all()
    d = distance(user.address, providers)

    return render_template("output.html", title=title, out=d)

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