
"""Utility file to seed health data for fictitious user"""

from sqlalchemy import func
from model import User
from model import Condition
from model import UserCondition

from datetime import datetime

from model import connect_to_db, db
#from server import app



##############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    # load_movies()
    # load_ratings()
    # set_val_user_id()