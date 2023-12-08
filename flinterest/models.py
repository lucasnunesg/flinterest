# Create the database structure
from datetime import datetime

from flask_login import UserMixin

from flinterest import database, login_manager


# Required function to retrieve an user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship("Post", backref="user", lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    picture = database.Column(database.String, default="default.png")
    created_date = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow()
    )
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )
