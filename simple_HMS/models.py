from . import database
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class BlogPost(database.Model):
    __tablename__ = "blog_posts"
    id = database.Column(database.Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = database.Column(database.Integer, database.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
    title = database.Column(database.String(250), unique=True, nullable=False)
    subtitle = database.Column(database.String(250), nullable=False)
    date = database.Column(database.String(250), nullable=False)
    body = database.Column(database.Text, nullable=False)
    img_url = database.Column(database.String(250), nullable=False)
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_post")


# Create the User table

class User(UserMixin, database.Model):
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(100), unique=True)
    password = database.Column(database.String(100))
    name = database.Column(database.String(100))
    # This will act like a list of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    # Parent relationship: "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")


# Create the BlogPost comments table
class Comment(database.Model):
    __tablename__ = "comments"
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.Text, nullable=False)
    # Child relationship:"users.id" The users refers to the tablename of the User class.
    # "comments" refers to the comments property in the User class.
    author_id = database.Column(database.Integer, database.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child Relationship to the BlogPosts
    post_id = database.Column(database.Integer, database.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
