from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/posts")
def posts_page():
    page = request.args.get("page", default=1, type=int)
    post_list = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("posts/index.html", post_list=post_list)

@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/post.html", post=post)

@posts.route("/posts/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully", category="success")
        return redirect(url_for("posts.posts_page"))
    return render_template("posts/create.html", form = form)

@posts.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully", category="success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template("posts/edit.html", form=form)

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully", category="success")

    return redirect(url_for("posts.posts_page"))