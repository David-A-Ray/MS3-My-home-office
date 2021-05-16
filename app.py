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
from typing import Optional


UPLOAD_FOLDER = '/workspace/MS3-My-home-office/assets/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, instance_relative_config=False)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# ----------------- HELPER FUNCTIONS -----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_logged_in() -> Optional[str]:
    """
    Returns the username if found in session, else None
    """
    return session.get("user")


# ----------------- AUTH -----------------
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
        return redirect(url_for("my_workspace", username=session["user"]))
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
                    "my_workspace", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# ----------------- DASHBOARD AND USER FUNCTIONALITY -----------------
@app.route("/")
@app.route("/home")
def home():
    setups = mongo.db.my_set_up.find()
    return render_template("home.html", setups=setups)


@app.route("/my_workspace/<username>", methods=["GET", "POST"])
def my_workspace(username):
    if is_logged_in():
        # grab the user from the DB based on username
        user = mongo.db.users.find_one({"username": session["user"]})
        return render_template("my_workspace.html", user=user)
    return redirect(url_for("login"))


# ----------------- UPLOAD USER WORKSPACE FUNCTIONALITY -----------------
@app.route("/add_workspace", methods=["GET", "POST"])
def add_workspace():
    if request.method == 'POST':
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path_to_image = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            setup = {
                "image": path_to_image,  # <img src="{{ setup.image }}"
                "description": request.form.get("description"),
                "category_1": request.form.get("category_1"),
                "product_1": request.form.get("product_1"),
                "url_1": request.form.get("url_1"),
                "category_2": request.form.get("category_2"),
                "product_2": request.form.get("product_2"),
                "url_2": request.form.get("url_2"),
                "category_3": request.form.get("category_3"),
                "product_3": request.form.get("product_3"),
                "url_3": request.form.get("url_3"),
                "user_name": session["user"],
                "upload_date": date.today().strftime("%d/%m/%Y"),
            }
            mongo.db.my_set_up.insert_one(setup)
            flash("Your home office was uploaded")
            return redirect(url_for("home"))

    return render_template("add_workspace.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
