
"""Utility file to seed health data for fictitious user"""

from model import connect_to_db, db
from model import User, UserCondition, Condition
from model import Symptom, UserSymptom, SymptomItem
from model import ValueType, UserValueType, ValueItem
from model import CountType, UserCountType, CountItem

from datetime import datetime

from server import app


def example_data():
    """Create some sample data."""

    # Delete all rows in all tables so if we need to run this a second time,
    # we won't be trying to add duplicate data

    # User.query.delete()
    # Condition.query.delete()
    # UserCondition.query.delete()
    # Symptom.query.delete()
    # UserSymptom.query.delete()
    # SymptomItem.query.delete()
    # ValueType.query.delete()
    # UserValueType.query.delete()
    # ValueItem.query.delete()
    # CountType.query.delete()
    # UserCountType.query.delete()
    # CountItem.query.delete()


    users = [
        User(email="hi@gmail.com", 
             password="123456", 
             fname="Bob", 
             lname="Bee", 
             zipcode="94030"),
        User(email="hello@gmail.com", 
             password="123456", 
             fname="Patty", 
             lname="Pi", 
             zipcode="02738"),
        User(email="howdy@gmail.com",
             password="123456",
             fname="Al",
             lname="Aboard",
             zipcode="63038")
    ]

    conditions = [
        Condition(cond_name="Asthma", 
                  cond_desc="Condition with swollen and narrowed airways"),
        Condition(cond_name="Migraines", 
                  cond_desc="Severe headaches"),
        Condition(cond_name="Diabetes", 
                  cond_desc="Diseases affecting how body uses insulin")
    ]

    user_conditions = [
        UserCondition(user_id=1, cond_id=1),
        UserCondition(user_id=1, cond_id=2),
        UserCondition(user_id=2, cond_id=1),
        UserCondition(user_id=3, cond_id=1)
    ]

    symptoms = [
        Symptom(symptom_name="Wheezing", symptom_desc="Whistling with breath"),
        Symptom(symptom_name="Difficulty Breathing"),
        Symptom(symptom_name="Backache", symptom_desc="Muscle pain in back"),
        Symptom(symptom_name="Headache"),
        Symptom(symptom_name="Sleep-deprived"),
        Symptom(symptom_name="Fatigued"),
        Symptom(symptom_name="Stressed"),
        Symptom(symptom_name="Peanuts"),
        Symptom(symptom_name="Chocolate"),
        Symptom(symptom_name="Hormones"),
        Symptom(symptom_name="Bright Lights"),
        Symptom(symptom_name="Dehydrated")
    ]

    user_symptoms = [
        UserSymptom(usercond_id=1, symptom_id=1),
        UserSymptom(usercond_id=1, symptom_id=2),
        UserSymptom(usercond_id=1, symptom_id=3),
        UserSymptom(usercond_id=2, symptom_id=4),
        UserSymptom(usercond_id=2, symptom_id=5),
        UserSymptom(usercond_id=2, symptom_id=7),
        UserSymptom(usercond_id=2, symptom_id=8),
        UserSymptom(usercond_id=2, symptom_id=10),
        UserSymptom(usercond_id=3, symptom_id=1),
        UserSymptom(usercond_id=3, symptom_id=2),
        UserSymptom(usercond_id=3, symptom_id=3),
        UserSymptom(usercond_id=4, symptom_id=1),
        UserSymptom(usercond_id=4, symptom_id=2),
        UserSymptom(usercond_id=4, symptom_id=3),
    ]

    symptom_items = [
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=1),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=2),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=3),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=4),       
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=5),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=6),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=7),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=8),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=9),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=10),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=11),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=12),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=13),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=14)
    ]

    value_types = [
        ValueType(value_name="AQI", value_desc="Air Quality Index"),
        ValueType(value_name="Hemoglobin Level"),
    ]

    user_value_types = [
        UserValueType(usercond_id=1, value_id=1),
        UserValueType(usercond_id=3, value_id=1),
        UserValueType(usercond_id=4, value_id=1),
    ]

    value_items = [
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=80, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=60, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=45, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=40, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=70, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=110, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=180, 
                  user_value_id=1),
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=30, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=60, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=90, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=110, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=60, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=30, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=80, 
                  user_value_id=2),
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=70, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=110, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=160, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=170, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=100, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=60, 
                  user_value_id=3),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=30, 
                  user_value_id=3)        
    ]

    count_types = [
        CountType(count_name="Ventolin", count_desc="Rescue Inhaler"),
        CountType(count_name="QVAR", count_desc="Steroid Inhaler"),
        CountType(count_name="Tylenol", count_desc="Acetaminophen"),
        CountType(count_name="Advil", count_desc="Ibuprofen"),
        CountType(count_name="Caffeine")
    ]

    user_count_types = [
        UserCountType(usercond_id=1, count_id=1),
        UserCountType(usercond_id=1, count_id=2),
        UserCountType(usercond_id=3, count_id=1),
        UserCountType(usercond_id=3, count_id=2),
        UserCountType(usercond_id=4, count_id=1),
        UserCountType(usercond_id=4, count_id=2)
    ]

    count_items = [
        CountItem(count_date=datetime(2018, 10, 7, 8, 30, 0), 
                  count=1, 
                  user_count_id=1),
        CountItem(count_date=datetime(2018, 10, 7, 21, 30, 0), 
                  count=1, 
                  user_count_id=1),
        CountItem(count_date=datetime(2018, 10, 7, 12, 30, 0), 
                  count=2, 
                  user_count_id=2),
        CountItem(count_date=datetime(2018, 10, 7, 7, 30, 0), 
                  count=1, 
                  user_count_id=3),
        CountItem(count_date=datetime(2018, 10, 7, 22, 30, 0), 
                  count=1, 
                  user_count_id=3),
        CountItem(count_date=datetime(2018, 10, 7, 8, 30, 0), 
                  count=2, 
                  user_count_id=4),
        CountItem(count_date=datetime(2018, 10, 7, 9, 1, 0), 
                  count=1, 
                  user_count_id=5),
        CountItem(count_date=datetime(2018, 10, 7, 22, 15, 0), 
                  count=1, 
                  user_count_id=5),
        CountItem(count_date=datetime(2018, 10, 7, 14, 30, 0), 
                  count=2, 
                  user_count_id=6),
    ]

    db.session.add_all(users)
    db.session.add_all(conditions) 
    db.session.add_all(user_conditions)
    db.session.add_all(symptoms)
    db.session.add_all(user_symptoms)
    db.session.add_all(symptom_items)
    db.session.add_all(value_types)
    db.session.add_all(user_value_types)
    db.session.add_all(value_items)
    db.session.add_all(count_types)
    db.session.add_all(user_count_types)
    db.session.add_all(count_items)

    db.session.commit()

##############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import test data
    example_data()
