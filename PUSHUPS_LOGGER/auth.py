from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)


@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    print(list(request.form.values()))
    return redirect(url_for("auth.signin"))

@auth.route("/signin")
def signin():
    return render_template("signin.html")

@auth.route("/signin", methods=["POST"])
def signin_post():
    print(list(request.form.values()))
    return redirect(url_for("main.profile"))

@auth.route("/signout")
def signout():
    return "signout successfully"
