
"""Utility file to seed health data for fictitious user"""

from model import connect_to_db, db
from model import User, UserLog, UserCondition, Condition
from model import Symptom, UserSymptom, SymptomItem
from model import ValueType, UserValueType, ValueItem
from model import CountType, UserCountType, CountItem

from datetime import datetime

from server import app


def example_data():
    """Create some sample data."""

    users = [
        User(email="hi@gmail.com", 
             password="123456", 
             fname="Bob", 
             lname="Bee", 
             zipcode="94030",
             is_superuser=True),
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

    db.session.add_all(users)
    db.session.commit()

    conditions = [
        Condition(cond_name="Asthma", 
                  cond_desc="Condition with swollen and narrowed airways"),
        Condition(cond_name="Migraines", 
                  cond_desc="Severe headaches"),
        Condition(cond_name="Diabetes", 
                  cond_desc="Diseases affecting how body uses insulin")
    ]

    db.session.add_all(conditions)
    db.session.commit() 

    user_conditions = [
        UserCondition(user_id=users[0].user_id_pk, cond_id=conditions[0].cond_id_pk),
        UserCondition(user_id=users[0].user_id_pk, cond_id=conditions[1].cond_id_pk),
        UserCondition(user_id=users[1].user_id_pk, cond_id=conditions[0].cond_id_pk),
        UserCondition(user_id=users[2].user_id_pk, cond_id=conditions[0].cond_id_pk)
    ]

    db.session.add_all(user_conditions)
    db.session.commit()

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

    db.session.add_all(symptoms)
    db.session.commit()

    user_symptoms = [
        UserSymptom(usercond_id=user_conditions[0].usercond_id_pk, symptom_id=symptoms[0].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[0].usercond_id_pk, symptom_id=symptoms[1].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[0].usercond_id_pk, symptom_id=symptoms[2].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[1].usercond_id_pk, symptom_id=symptoms[3].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[1].usercond_id_pk, symptom_id=symptoms[4].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[1].usercond_id_pk, symptom_id=symptoms[6].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[1].usercond_id_pk, symptom_id=symptoms[7].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[1].usercond_id_pk, symptom_id=symptoms[9].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[2].usercond_id_pk, symptom_id=symptoms[0].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[2].usercond_id_pk, symptom_id=symptoms[1].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[2].usercond_id_pk, symptom_id=symptoms[2].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[3].usercond_id_pk, symptom_id=symptoms[0].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[3].usercond_id_pk, symptom_id=symptoms[1].symptom_id_pk),
        UserSymptom(usercond_id=user_conditions[3].usercond_id_pk, symptom_id=symptoms[2].symptom_id_pk)
    ]

    db.session.add_all(user_symptoms)
    db.session.commit()

    symptom_items = [
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[0].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[1].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[2].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[3].user_symptom_id_pk),       
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[4].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[5].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[6].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[7].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[8].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[9].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[10].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[11].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=True, 
                    user_symptom_id=user_symptoms[12].user_symptom_id_pk),
        SymptomItem(symptom_date=datetime(2018, 10, 7, 0, 0, 0), 
                    symptom_present=False, 
                    user_symptom_id=user_symptoms[13].user_symptom_id_pk)
    ]

    db.session.add_all(symptom_items)
    db.session.commit()

    value_types = [
        ValueType(value_name="AQI", value_desc="Air Quality Index"),
        ValueType(value_name="Hemoglobin Level"),
    ]

    db.session.add_all(value_types)
    db.session.commit()

    user_value_types = [
        UserValueType(usercond_id=user_conditions[0].usercond_id_pk, value_id=value_types[0].value_id_pk),
        UserValueType(usercond_id=user_conditions[2].usercond_id_pk, value_id=value_types[0].value_id_pk),
        UserValueType(usercond_id=user_conditions[3].usercond_id_pk, value_id=value_types[0].value_id_pk),
    ]

    db.session.add_all(user_value_types)
    db.session.commit()

    value_items = [
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=80, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=60, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=45, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=40, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=70, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=110, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=180, 
                  user_value_id=user_value_types[0].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=30, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=60, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=90, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=110, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=60, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=30, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=80, 
                  user_value_id=user_value_types[1].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 1, 0, 0, 0), 
                  value=70, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 2, 0, 0, 0), 
                  value=110, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 3, 0, 0, 0), 
                  value=160, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 4, 0, 0, 0), 
                  value=170, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 5, 0, 0, 0), 
                  value=100, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 6, 0, 0, 0), 
                  value=60, 
                  user_value_id=user_value_types[2].user_value_id_pk),
        ValueItem(value_date=datetime(2018, 10, 7, 0, 0, 0), 
                  value=30, 
                  user_value_id=user_value_types[2].user_value_id_pk)        
    ]

    db.session.add_all(value_items)
    db.session.commit()

    count_types = [
        CountType(count_name="Ventolin", count_desc="Rescue Inhaler"),
        CountType(count_name="QVAR", count_desc="Steroid Inhaler"),
        CountType(count_name="Tylenol", count_desc="Acetaminophen"),
        CountType(count_name="Advil", count_desc="Ibuprofen"),
        CountType(count_name="Caffeine")
    ]

    db.session.add_all(count_types)
    db.session.commit()

    user_count_types = [
        UserCountType(usercond_id=user_conditions[0].usercond_id_pk, count_id=count_types[0].count_id_pk),
        UserCountType(usercond_id=user_conditions[0].usercond_id_pk, count_id=count_types[1].count_id_pk),
        UserCountType(usercond_id=user_conditions[2].usercond_id_pk, count_id=count_types[0].count_id_pk),
        UserCountType(usercond_id=user_conditions[2].usercond_id_pk, count_id=count_types[1].count_id_pk),
        UserCountType(usercond_id=user_conditions[3].usercond_id_pk, count_id=count_types[0].count_id_pk),
        UserCountType(usercond_id=user_conditions[3].usercond_id_pk, count_id=count_types[1].count_id_pk)
    ]

    db.session.add_all(user_count_types)
    db.session.commit()

    count_items = [
        CountItem(count_date=datetime(2018, 10, 7, 8, 30, 0), 
                  count=1, 
                  user_count_id=user_count_types[0].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 8, 21, 30, 0), 
                  count=1, 
                  user_count_id=user_count_types[0].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 7, 12, 30, 0), 
                  count=2, 
                  user_count_id=user_count_types[1].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 7, 7, 30, 0), 
                  count=1, 
                  user_count_id=user_count_types[2].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 8, 22, 30, 0), 
                  count=1, 
                  user_count_id=user_count_types[2].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 7, 8, 30, 0), 
                  count=2, 
                  user_count_id=user_count_types[3].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 7, 9, 1, 0), 
                  count=1, 
                  user_count_id=user_count_types[4].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 8, 22, 15, 0), 
                  count=1, 
                  user_count_id=user_count_types[4].user_count_id_pk),
        CountItem(count_date=datetime(2018, 10, 7, 14, 30, 0), 
                  count=2, 
                  user_count_id=user_count_types[5].user_count_id_pk),
    ]

    db.session.add_all(count_items)
    db.session.commit()

    user_logs = [
        UserLog(log_date=datetime(2018, 10, 7, 0, 0, 0), 
                log_text="I'm feeling great today!",
                user_id=users[0].user_id_pk),
        UserLog(log_date=datetime(2018, 10, 6, 0, 0, 0), 
                log_text="Last night sleep was TERRIBLE.",
                user_id=users[0].user_id_pk),
        UserLog(log_date=datetime(2018, 10, 7, 0, 0, 0), 
                log_text="Need to cut back on the coffee",
                user_id=users[1].user_id_pk),
        UserLog(log_date=datetime(2018, 10, 7, 0, 0, 0), 
                log_text="Wildfire smoke today",
                user_id=users[2].user_id_pk)                                        
    ]


    db.session.add_all(user_logs)
    db.session.commit()

    # import pdb; pdb.set_trace()


##############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # drop tables first
    db.drop_all()

    # In case tables haven't been created, create them
    db.create_all()

    # Import test data
    example_data()
