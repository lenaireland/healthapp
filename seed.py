
"""Utility file to seed health data for fictitious user"""

from sqlalchemy import func

from model import User
from model import UserCondition
from model import Condition

from model import Symptom
from model import UserSymptom
from model import SymptomItem

from model import ValueType
from model import UserValueType
from model import ValueItem

from model import CountType
from model import UserCountType
from model import CountItem

from datetime import datetime

from model import connect_to_db, db
#from server import app




def example_data():
    """Create some sample data."""

    users = [
        User(email="hi@gmail.com", 
             password="123456", 
             fname="Bob", 
             lname="Bee", 
             zipcode=94030),
        User(email="hello@gmail.com", 
             password="123456", 
             fname="Patty", 
             lname="Pi", 
             zipcode=02738),
        User(email="howdy@gmail.com",
             password="123456",
             fname="Al",
             lname="Aboard",
             zipcode=63038)
    ]

    conditions = [
        Condition(cond_name="Asthma", 
                  cond_desc="Condition with swollen and narrowed airways"),
        Condition(cond_name="Migraines", 
                  cond_desc="Severe headaches"),
        Condition(cond_name="Diabetes", 
                  cond_desc="Diseases affecting how body uses insulin")
    ]

    ded = Department(
        dept_code='ed', dept='Education', phone='555-1000')
    dad = Department(
        dept_code='admin', dept='Administration', phone='555-2222')
    dpt = Department(
        dept_code='pt', dept='Part-Time', phone='555-9999')
    dot = Department(
        dept_code='oth', dept='Other', phone='555-3333')

    employees = [
        Employee(name='Joel Burton', dept=ded, fav_color='orange'),
        Employee(name='Cynthia Dueltgen', dept=ded, fav_color='purple'),
        Employee(name='Rachel Thomas', dept=ded),
        Employee(name='Katie Lefevre', dept=ded, fav_color='rainbow'),
        Employee(name='Meggie Mahnken', dept=ded, fav_color='black'),
        Employee(name='Ahmad Alawad', dept=ded, fav_color='blue'),
        Employee(name='Heather Bryant', dept=ded, fav_color='purple'),
        Employee(name='Meg Bishop', dept=ded, fav_color='blue'),
        Employee(name='Katie Byers', dept=ded, fav_color='red'),
        Employee(name='Henry Chen', dept=ded, fav_color='green'),
        Employee(name='Kara DeWalt', dept=ded, fav_color='cyan'),
        Employee(name='Lavinia Karl', dept=ded, fav_color='orange'),
        Employee(name='David Phillips', dept=dad),
        Employee(name='Angie Chang', dept=dad),
        Employee(name='Stefan Gomez', dept=dad),
        Employee(name='Laura Gillen', dept=dad),
        Employee(name='Paria Rajai', dept=dad),
        Employee(name='Wendy Saccuzzo', dept=dot),
        Employee(name='Dori Grant', dept=dot),
        Employee(name='Kari Burge', dept=dot, fav_color='purple'),
        Employee(name='Rachel Walker', dept=dpt),
        Employee(name='Balloonicorn', fav_color='rainbow')
    ]
    db.session.add_all(employees)
    db.session.commit()

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