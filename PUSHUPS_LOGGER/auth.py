from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/signup")
def signup():
    return "signup page"


@auth.route("/signin")
def signup():
    return "signin page"


@auth.route("/signout")
def signup():
    return "signout successfully"
