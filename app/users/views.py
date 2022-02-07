from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RegisterForm, LoginForm, UpdateAccountForm
from app.users.utils import save_avatar

users = Blueprint("users", __name__)

@users.route("/users/<string:name>")
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    page = request.args.get("page", default=1, type=int)
    post_list = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("users/user.html", user=user, post_list=post_list)

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar = avatar_file

        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated successfully", category="success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email

    img_file = url_for("static", filename=f"avatars/{current_user.avatar}")
    return render_template(
        "account.html", 
        avatar=img_file, 
        form=form
    )

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.posts_page"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account {form.name.data} created successfully", category="success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.posts_page"))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(name=form.name.data).first()
            if user and bcrypt.check_password_hash(
                user.password, 
                form.password.data
            ):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("posts.posts_page"))
            else:
                flash('Account does not exist. Please check username and password', category='danger')
    return render_template("login.html", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))