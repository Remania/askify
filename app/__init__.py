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
    app.config["SECRET_KEY"] = "4f3f4a82050ddbdae70ed6c54758df80"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///askify.db"

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