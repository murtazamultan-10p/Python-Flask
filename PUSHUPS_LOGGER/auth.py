from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/signup")
def signup():
    return "signup page"


@auth.route("/signin")
def signin():
    return "signin page"


@auth.route("/signout")
def signout():
    return "signout successfully"
