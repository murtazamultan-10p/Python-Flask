from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def indezx():
    return "Home Page"


@main.route("/profile")
def index():
    return "Profile Page"
