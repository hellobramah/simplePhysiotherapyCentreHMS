from functools import wraps

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import BlogPost, Comment
from .forms import CreateBlogPostForm, CommentForm
from datetime import date

from . import database

views = Blueprint('views', __name__)

# Create a decorator function that allows only the administrator
def admin_only(function_to_be_passed):
    @wraps(function_to_be_passed)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return function_to_be_passed(*args, **kwargs)

    return decorated_function


# home route
@views.route('/')
def get_all_posts():
    result = database.session.execute(database.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Add a POST method to be able to post comments
@views.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = database.get_or_404(BlogPost, post_id)
    # Add the CommentForm to the route
    comment_form = CommentForm()
    # Only allow logged-in users to comment on posts
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        database.session.add(new_comment)
        database.session.commit()
    return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)


# Use a decorator so only an admin user can create new posts
@views.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    create_blog_post_form = CreateBlogPostForm()
    if create_blog_post_form.validate_on_submit():
        new_post = BlogPost(
            title=create_blog_post_form.title.data,
            subtitle=create_blog_post_form.subtitle.data,
            body=create_blog_post_form.body.data,
            img_url=create_blog_post_form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        database.session.add(new_post)
        database.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=create_blog_post_form, current_user=current_user)


# Use a decorator so only an admin user can edit a post
@views.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = database.get_or_404(BlogPost, post_id)
    edit_form = CreateBlogPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        database.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


# Use a decorator so only an admin user can delete a post
@views.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = database.get_or_404(BlogPost, post_id)
    database.session.delete(post_to_delete)
    database.session.commit()
    return redirect(url_for('get_all_posts'))


# route to How we treat page
@views.route("/how_we_treat")
def how_we_treat():
    return render_template("how_we_treat.html", current_user=current_user)
# route to What we treat page
@views.route("/what_we_treat")
def what_we_treat():
    return render_template("what_we_treat.html", current_user=current_user)
# route to about page
@views.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


# route to contact page
@views.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html", current_user=current_user)
