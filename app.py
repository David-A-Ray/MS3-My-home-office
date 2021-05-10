import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import date
from forms import SignupForm, WorkspaceForm
if os.path.exists("env.py"):
    import env
from typing import Optional


UPLOAD_FOLDER = '/assets/images/'
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
    form = SignupForm()
    if form.validate_on_submit():
        # check if username already exsists in db
        existing_user = mongo.db.users.find_one(
            {"username": form.username.data.lower()})

        if existing_user:
            flash("Username already taken")
            return redirect(url_for("register"))

        register = {
            "username": form.username.data.lower(),
            "email": form.email.data,
            "password": generate_password_hash(form.password.data)
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = form.username.data
        flash("You have registered")
        return redirect(url_for("my_workspace", username=session["user"]))
    return render_template("register.html", form=form, template="form_template")


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


# ----------------- DASHBOARD AND USER FUNCTIONALITY -----------------
@app.route("/add_workspace", methods=["GET", "POST"])
def add_workspace():
    form = WorkspaceForm()
    if form.validate_on_submit():  # check if POST and validate
        filename = secure_filename(form.file.data.filename)
        path_to_image = form.file.data.save(UPLOAD_FOLDER + filename)
        workspace_data = {
            "image": path_to_image, # <img src="{{ workspace.image }}"
            "description": form.description.data,
            "category_1": request.form.get("category1"),
            "product_1": request.form.get("product1"),
            "url_1": request.form.get("url1"),
            "category_2": request.form.get("category2"),
            "product_2": request.form.get("product2"),
            "url_2": request.form.get("url2"),
            "category_3": request.form.get("category3"),
            "product_3": request.form.get("product3"),
            "url_3": request.form.get("url3"),
            "user_name": session["user"],
            "upload_date": date.today().strftime("%d/%m/%Y"),
        }
        mongo.db.my_set_up.insert_one(workspace_data)
        flash("Your home office was uploaded")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
