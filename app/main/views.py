from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/home")
@main.route("/")
def home_page():
    return render_template("index.html")