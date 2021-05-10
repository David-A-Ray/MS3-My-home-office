import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import date
if os.path.exists("env.py"):
    import env


today = date.today()
d1 = today.strftime("%d/%m/%Y")
UPLOAD_FOLDER = '/assets/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/show_setups")
def show_setups():
    setups = mongo.db.my_set_up.find()
    return render_template("index.html", setups=setups)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already taken")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have registered")
        return redirect(url_for("my_work_space", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exsists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_work_space", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/my_work_space/<username>", methods=["GET", "POST"])
def my_work_space(username):
    # grab the session user's name from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("my_work_space.html", username=username)
    
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_my_work_space", methods=["GET", "POST"])
def add_my_work_space():
    if request.method == 'POST':
        setup = {
            "image": request.form.get("image"),
            "description": request.form.get("description"),
            "category1": request.form.get("category1"),
            "product1": request.form.get("product1"),
            "url1": request.form.get("url1"),
            "category2": request.form.get("category2"),
            "product2": request.form.get("product2"),
            "url2": request.form.get("url2"),
            "category3": request.form.get("category3"),
            "product3": request.form.get("product3"),
            "url3": request.form.get("url3"),
            "user_name": session["user"],
            "upload_date": d1,
        }
        mongo.db.my_set_up.insert_one(setup)
        flash("Your home office was uploaded")
        return redirect(url_for("show_setups"))

    return render_template("add_my_work_space.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
