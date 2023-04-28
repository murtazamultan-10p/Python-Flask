from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User
from . import sql_db

auth = Blueprint("auth", __name__)


@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    name, email, password = list(request.form.values())
    user = User.query.filter_by(email=email).first()

    if not user:
        hash_password = generate_password_hash(password=password)
        user = User(name=name, email=email, password=hash_password)
        sql_db.session.add(user)
        sql_db.session.commit()
        flash("User created successfully")
        return redirect(url_for("auth.signin"))
    
    flash("User already exists")
    return redirect(url_for("auth.signup"))

@auth.route("/signin")
def signin():
    return render_template("signin.html")

@auth.route("/signin", methods=["POST"])
def signin_post():
    email, password = list(request.form.values())
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid email or password")
        return redirect(url_for("auth.signin"))

    flash("Login successful")
    return redirect(url_for("main.profile"))

@auth.route("/signout")
def signout():
    return flash("signout successfully")
