# The purpose of this file is to create the database only

from flinterest import app, database
from flinterest.models import Post, User

with app.app_context():
    database.create_all()
