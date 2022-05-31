from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/favicon.ico")
def favicon():
    return ""

@main.route("/")
@main.route("/home")
def home_page():
    return render_template("index.html")