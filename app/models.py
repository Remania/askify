from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    avatar = db.Column(db.String(20), default="default.png", nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship('Comment', backref='author', lazy="dynamic")

    def __repr__(self):
        return f"User ('{self.name}', '{self.email}', '{self.avatar}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship('Comment', backref='post',
    cascade='all, delete, delete-orphan', lazy=True)

    def __repr__(self):
        return f"Post ('{self.title}', '{self.content}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)