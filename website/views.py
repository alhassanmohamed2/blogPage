from flask import Blueprint, render_template, request, redirect,url_for
from flask.helpers import flash
from flask_login import login_required, current_user
from .models import Post,User
from . import db
views = Blueprint("views", __name__)



@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html",user=current_user,posts=posts)




@views.route("/create-post",methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash("post cannot be empty")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created")
    return render_template("create_posts.html",user=current_user)

@views.route("/delete-post/<id>")
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("post did exisit",category='error')
    elif current_user.id != post.id:
        flash("not can't")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted")
    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)
