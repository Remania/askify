from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "samplesecret"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///askify.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://saoacykbmyuojp:3f8bc32fb66e3457b9f7be3e68bf452b31f64ba9a57457b559b3a4665f7fac8a@ec2-54-204-56-171.compute-1.amazonaws.com:5432/deanfmhvm4tn1f"

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.main.views import main
    from app.users.views import users
    from app.posts.views import posts
    from app.errors.handlers import errors


    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app