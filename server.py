
"""Health Tracker"""

import os, requests, hashlib, base64

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect
from flask import flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime, timedelta
from sqlalchemy import func

from model import connect_to_db, db
from model import User, UserLog, UserCondition, Condition
from model import Symptom, UserSymptom, SymptomItem
from model import ValueType, UserValueType, ValueItem
from model import CountType, UserCountType, CountItem


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['SECRET_KEY']

AIRNOW = os.environ['AIRNOW_KEY']


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

#######
#TO DO: Make homepage have logo, project info.
#######

@app.route('/')
def index():
    """Homepage - show information about project - take to login"""

    return render_template('homepage.html')

@app.route('/login', methods=['GET'])
def login_form():
    """Show login/registration form"""

    # if user is logged in, take to personal page
    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/user/{}'.format(session['userid']))

    # if not logged in, show login/register form
    return render_template('login_form.html')

@app.route('/process-login', methods=['POST'])
def login_process():
    """Process Login"""

    # process login form data, query for user in database
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # if user email exists and password matches, login
    if user:
        hashed = hashlib.sha512(password.encode() + user.salt.encode())
        hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()

        if hashed_str == user.passhash:
            session['userid']=user.user_id_pk
            flash('Log in successful')
            return redirect('/user/{}'.format(session['userid']))

    flash('Login Failed')
    return redirect('/login')

# @app.route('/register', methods=['GET'])
# def register_form():
#     """Show login/registration form"""

#     # if user is logged in, take to personal page
#     if session.get('userid'):
#         flash('Already logged in.')

#         return redirect('/user/{}'.format(session['userid']))

#     # if not logged in, go to '/login' route to login/register
#     return redirect('/login')

@app.route('/process-register', methods=['POST'])
def register_process():
    """Process user registration"""

    # process register form data, query for user in database
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # if there is a user in database that matches email redirect to '/login'    
    if user:
        flash('Account already exists. Please login.')
        return redirect('/login')

    # if email is not already in database, create salt and hashed password, 
    # create new instance of User class, add to database, 
    # login user, and take to settings page
    salt = base64.urlsafe_b64encode(os.urandom(16))
    salt_str = salt.decode()
    hashed = hashlib.sha512(password.encode() + salt)
    hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()


    new_user = User(email=email, salt=salt_str, passhash=hashed_str)
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter(User.email == email).first()
    session['userid']=user.user_id_pk

    flash('New user successfully created.')
    return redirect('/settings')

@app.route('/settings', methods=['GET'])
def user_settings():
    """Show update settings form"""

    # if user is logged in, take to settings form
    if session.get('userid'):
        user=User.query.get(session['userid'])
        return render_template("settings_form.html", user=user)

    else:
        flash('Not logged in')
        return redirect('/login')

@app.route('/process-settings', methods=['POST'])
def process_user_settings():
    """Processing user settings update"""

    user=User.query.get(session['userid'])

    email = request.form.get('email')

    # check that e-mail does not yet exist in the system
    for user_email in db.session.query(User.email).all():
        if email == user_email[0] and email != user.email:
            flash('Error - this email is already in the system')
            return redirect('/settings')

    user.email = email
    user.fname = request.form.get('fname')
    user.lname = request.form.get('lname')
    user.zipcode = request.form.get('zipcode')

    db.session.commit()

    flash('User settings updated')
######
# TO DO: change this to take back to settings, add button to return to user page
# MAKE THIS A MODAL
#######
    return redirect('/settings')

@app.route('/update-password', methods=['POST'])
def update_user_password():
    """Update user password"""

    user=User.query.get(session['userid'])

    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    new_password_2 = request.form.get('newPassword2')  

    curr_hashed = hashlib.sha512(current_password.encode() + user.salt.encode())
    curr_hash_str = base64.urlsafe_b64encode(curr_hashed.digest()).decode()

    if curr_hash_str == user.passhash:
        if new_password == new_password_2:
            salt = base64.urlsafe_b64encode(os.urandom(16))
            salt_str = salt.decode()
            hashed = hashlib.sha512(new_password.encode() + salt)
            hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()

            user.salt = salt_str
            user.passhash = hashed_str

            db.session.commit()

            return ("Password Updated")
        return ("New passwords do not match")
    return ("Current password does not match")

@app.route('/logout')
def logout():
    """Process user logout"""

    if session.get('userid'):    
        session.pop('userid')
        flash('Logged out.')
    
    return redirect('/login')

@app.route('/user/<userid>', defaults={'date': None})
@app.route('/user/<userid>/<date>')
def user_day_page(userid, date):
    """Show individual user day page"""

    userid=int(userid)
    today=datetime.now()

    if date:
        date=datetime.strptime(date, "%Y-%m-%d")
    else:
        date=today

    if session.get('userid'):
        if userid == session['userid']:

            user = User.query.get(session['userid'])
            info = user_tracked_info()

            return render_template('usermainpage.html',
                                   user=user,
                                   info=info, 
                                   date=date,
                                   today=today,
                                   prev_date=(date-timedelta(1)),
                                   next_date=(date+timedelta(1)))

        flash('You do not have permission to view this page.')
        return redirect('/user/{}'.format(session['userid']))

    flash('You do not have permission to view this page.')
    return redirect('/login')

@app.route('/add-tracking')
def add_tracking():
    """Add new condition/symptom/count/value items for tracking"""

    if session.get('userid'):

        user_conditions = (db.session.query(UserCondition)
                           .filter((UserCondition.user_id==session['userid']),
                                   (UserCondition.is_tracked==True))
                           .all())

        unused_conditions = user_not_tracked_conditions()
        unused_symptoms = user_not_tracked_symptoms()
        unused_values = user_not_tracked_value_types()
        unused_counts = user_not_tracked_count_types()

        return render_template('add_tracking.html', 
                               unused_conditions=unused_conditions,
                               user_conditions=user_conditions,
                               unused_symptoms=unused_symptoms,
                               unused_counts=unused_counts,
                               unused_values=unused_values)  

    flash('You do not have permission to view this page.')    
    return redirect('/login')

@app.route('/stop-tracking')
def stop_tracking():
    """Remove condition/symptom/count/value items from tracking"""

    if session.get('userid'):

        user_conditions = user_tracked_conditions()

        symptoms = []
        values = []
        counts = []

        for cond in user_conditions:
            symptoms += user_tracked_symptoms(cond)
            values += user_tracked_value_types(cond)
            counts += user_tracked_count_types(cond)

        return render_template('stop_tracking.html', 
                               user_conditions=user_conditions,
                               symptoms=symptoms,
                               counts=counts,
                               values=values)  

    flash('You do not have permission to view this page.')    
    return redirect('/login')

@app.route('/query')
def query_database():
    """Query database to find correlations between tracked items"""

    if session.get('userid'):

        user_conditions = user_tracked_conditions()

        symptoms = []
        values = []
        counts = []

        for cond in user_conditions:
            symptoms += user_tracked_symptoms(cond)
            values += user_tracked_value_types(cond)
            counts += user_tracked_count_types(cond)

        return render_template('query.html', 
                               user_conditions=user_conditions,
                               symptoms=symptoms,
                               counts=counts,
                               values=values)

    flash('You do not have permission to view this page.')
    return redirect('/login')

@app.route('/plot')
def plot_longitudinal():
    """Plot longitudinal user data"""

    if session.get('userid'):

        return render_template('plot.html')

    flash('You do not have permission to view this page.')
    return redirect('/login')

# The next 4 routes are used from plot.html and 
# associated .js files to plot longitudinal time series

@app.route('/get-plot-setup-data', methods=['GET'])
def get_plot_setup_data():
    """Get user first logged date and number of symptoms"""

    # num_symptoms = (db.session.query(func.count(UserSymptom.user_symptom_id_pk))
    #                           .join(UserCondition)
    #                           .join(SymptomItem)
    #                           .filter(UserSymptom.is_tracked==True,
    #                                   SymptomItem.symptom_present==True
    #                                   UserCondition.user_id==session['userid'])
    #                           .one())

    first_symp_date = (db.session.query(func.min(SymptomItem.symptom_date))
                              .join(UserSymptom)
                              .join(UserCondition)
                              .filter(UserSymptom.is_tracked==True,
                                      SymptomItem.symptom_present==True,
                                      UserCondition.user_id==session['userid'])
                              .first())

    first_value_date = (db.session.query(func.min(ValueItem.value_date))
                          .join(UserValueType)
                          .join(UserCondition)
                          .filter(UserValueType.is_tracked==True,
                                  ValueItem.value > 0,
                                  UserCondition.user_id==session['userid'])
                          .first())

    first_count_date = (db.session.query(func.min(CountItem.count_date))
                          .join(UserCountType)
                          .join(UserCondition)
                          .filter(UserCountType.is_tracked==True,
                                  CountItem.count > 0,
                                  UserCondition.user_id==session['userid'])
                          .first())

    first_date = min(first_symp_date[0], first_value_date[0], first_count_date[0])
    print(first_symp_date)
    print(first_date)
    print(type(first_date))
    return("hi")

@app.route('/get-symptom-timeseries.json', methods=['GET'])
def get_symptom_timeseries():
    """Get user symptom timeseries data from database"""

    symptom_data = (db.session.query(SymptomItem)
                          .join(UserSymptom)
                          .join(UserCondition)
                          .filter(UserSymptom.is_tracked==True,
                                  SymptomItem.symptom_present==True,
                                  UserCondition.user_id==session['userid'])
                          .order_by(SymptomItem.symptom_date)
                          .order_by(UserSymptom.usercond_id)
                          .all())

    symptom_data_list = []
    for symptom_item in symptom_data:
        user_symptom_name = symptom_item.user_symptom.symptom.symptom_name
        symptom_data_list.append({"name": user_symptom_name,
                             "date": str(symptom_item.symptom_date.date()),
                             "sym_present": symptom_item.symptom_present})

    return(jsonify(symptom_data_list))

@app.route('/get-value-timeseries.json', methods=['GET'])
def get_value_timeseries():
    """Get user value timeseries data from database"""


    value_data = (db.session.query(ValueItem)
                          .join(UserValueType)
                          .join(UserCondition)
                          .filter(UserValueType.is_tracked==True,
                                  ValueItem.value > 0,
                                  UserCondition.user_id==session['userid'])
                          .order_by(ValueItem.value_date)
                          .order_by(ValueItem.user_value_id)
                          .all())

    value_data_list = []
    for value_item in value_data:
        user_value_name = value_item.user_value_type.value_type.value_name
        value_data_list.append({"name": user_value_name,
                                "date": str(value_item.value_date.date()),
                                "value": float(value_item.value)})


    return(jsonify(value_data_list))

@app.route('/get-count-timeseries.json', methods=['GET'])
def get_count_timeseries():
    """Get user count timeseries data from database"""


    count_data = (db.session.query(CountItem)
                          .join(UserCountType)
                          .join(UserCondition)
                          .filter(UserCountType.is_tracked==True,
                                  CountItem.count > 0,
                                  UserCondition.user_id==session['userid'])
                          .order_by(CountItem.count_date)
                          .order_by(CountItem.user_count_id)
                          .all())
    
    count_data_list = []
    for count_item in count_data:
        user_count_name = count_item.user_count_type.count_type.count_name
        count_data_list.append({"name": user_count_name,
                                "date": str(count_item.count_date.date()),
                                "count": count_item.count})

    return(jsonify(count_data_list))

# The next 9 routes are used from usermainpage.html and 
# associated .js files to display tracked user symptoms and 
# update values

@app.route('/get-user-symptom', methods=['GET'])
def get_user_symptom():
    """Get user symptom values from database"""

    user_symptom_id = request.args.get("user_symptom_id")
    date = request.args.get("date")

    datarecord = (SymptomItem.query
                  .filter(SymptomItem.user_symptom_id==user_symptom_id,
                          func.date(SymptomItem.symptom_date)==date)
                  .first())

    if datarecord:
        value = datarecord.symptom_present
        return str(value)

    return "False" 

@app.route('/update-user-symptom', methods=['POST'])
def update_user_symptom():
    """Process user symptoms"""

    user_symptom_id = request.form.get("user_symptom_id")
    date = request.form.get("date")
    TF = request.form.get("TF")

    datarecord = (SymptomItem.query
                  .filter(SymptomItem.user_symptom_id==user_symptom_id,
                          func.date(SymptomItem.symptom_date)==date)
                  .first())

    if datarecord:

        # This string ('true') is coming from usemainpage.js
        # UPDATE THIS STRING if JavaScript file changes!
        if TF == 'true':
            datarecord.symptom_present = True
        else:
            datarecord.symptom_present = False
        db.session.commit()
        return "Record Updated"

    new_symptom = SymptomItem(symptom_date=date, 
                symptom_present=bool(TF), 
                user_symptom_id=user_symptom_id)

    db.session.add(new_symptom)
    db.session.commit()
    return "Record Added"

@app.route('/get-user-value-item', methods=['GET'])
def get_user_valueitem():
    """Get user value items from database"""

    user_value_id = request.args.get("user_value_id")
    date = request.args.get("date")

    datarecord = (ValueItem.query
                  .filter(ValueItem.user_value_id==user_value_id,
                          func.date(ValueItem.value_date)==date)
                  .first())

    if datarecord:
        value = datarecord.value
        return str(value)

    return "False" 

@app.route('/update-user-value-item', methods=['POST'])
def update_user_value_item():
    """Process user value items"""

    user_value_id = request.form.get("user_value_id")
    date = request.form.get("date")
    value = request.form.get("value")

    return(update_value_item_db(user_value_id, date, value))

@app.route('/update-airnow-item', methods=['POST'])
def update_aqi_data():
    """Update database with AirNOW API data"""

    distance = 200

    user_value_id = request.form.get("user_value_id")
    date = request.form.get("date")
    zipcode = request.form.get("zipcode")

    if not zipcode:
        user = User.query.get(session['userid'])
        zipcode = user.zipcode

    value = airnow_api(date, zipcode, distance)

    if value:
        db_status = update_value_item_db(user_value_id, date, value)
    else:
        db_status = "Failed to create AQI record"

    return jsonify([value, db_status])

@app.route('/get-user-count-item', methods=['GET'])
def get_user_countitem():
    """Get user count items from database"""

    user_count_id = request.args.get("user_count_id")
    date = request.args.get("date")

    datarecord = (CountItem.query
                           .filter(CountItem.user_count_id==user_count_id,
                                   func.date(CountItem.count_date)==date)
                           .first())

    if datarecord:
        count = datarecord.count
        return str(count)

    return "False" 

@app.route('/update-user-count-item', methods=['POST'])
def update_user_count_item():
    """Process user count items"""

    user_count_id = request.form.get("user_count_id")
    date = request.form.get("date")
    count = request.form.get("count")

    if count=="":
        count = None

    datarecord = (CountItem.query
                           .filter(CountItem.user_count_id==user_count_id,
                                   func.date(CountItem.count_date)==date)
                           .first())   
                    
    if datarecord: 
        datarecord.count = count
        db.session.commit()
        return "Record Updated"

    new_count = CountItem(count_date=date,
                          count=count,
                          user_count_id=user_count_id)

    db.session.add(new_count)
    db.session.commit()
    return "Record Added"

@app.route('/get-user-log', methods=['GET'])
def get_user_log():
    """Get user daily log from database"""

    date = request.args.get("date")

    datarecord = (UserLog.query.filter(func.date(UserLog.log_date)==date,
                                       UserLog.user_id==session['userid'])
                               .first())

    if datarecord:
        log_text = datarecord.log_text
        return log_text

    return "False"

@app.route('/update-user-log', methods=['POST'])
def update_user_log():
    """Process user count items"""

    date = request.form.get("date")
    text = request.form.get("text")

    datarecord = (UserLog.query.filter(func.date(UserLog.log_date)==date,
                                       UserLog.user_id==session['userid'])
                               .first())   
                    
    if datarecord: 
        datarecord.log_text = text
        db.session.commit()
        return "Record Updated"

    new_log = UserLog(log_date=date,
                      log_text=text,
                      user_id=session['userid'])

    db.session.add(new_log)
    db.session.commit()
    return "Record Added"

# The next 8 routes are used from add_tracking.html
# and associated .js files to display and add new tracking

@app.route('/get-condition-desc', methods=['GET'])
def get_condition_description():
    """Get description of condition from database"""

    cond_id = request.args.get("cond_id")

    if cond_id:
        cond_record = (Condition.query
                                .filter(Condition.cond_id_pk==cond_id)
                                .first())

        if cond_record.cond_desc:
            return cond_record.cond_desc

    return ("n/a")

@app.route('/get-tracked-condition-desc', methods=['GET'])
def get_tracked_condition_description():
    """Get description of condition from database"""

    usercond_id = request.args.get("usercond_id")

    if usercond_id:
        usercond_record = (UserCondition.query
                           .filter(UserCondition.usercond_id_pk==usercond_id)
                           .first())

        if usercond_record.condition.cond_desc:
            return usercond_record.condition.cond_desc

    return ("n/a")    

@app.route('/add-user-condition', methods=['POST'])
def add_user_condition():
    """Add new condition to database for user to track"""

    cond_id = request.form.get("cond_id")

    user_condition = (UserCondition.query
                       .filter(UserCondition.user_id==session['userid'],
                               UserCondition.cond_id==int(cond_id))
                       .first())

    if user_condition:
        if user_condition.is_tracked==False:
            user_condition.is_tracked = True
            db.session.commit()
            return "Condition is now tracked again"
        return "Add condition failed"

    new_condition = UserCondition(user_id=session['userid'],
                                  cond_id=cond_id)

    db.session.add(new_condition)
    db.session.commit()
    return "Condition Added"

@app.route('/get-symptom-desc', methods=['GET'])
def get_symptom_description():
    """Get description of symptom from database"""

    symptom_id = request.args.get("symptom_id")

    if symptom_id:
        symptom_record = (Symptom.query
                                 .filter(Symptom.symptom_id_pk==symptom_id)
                                 .first())

        if symptom_record.symptom_desc:
            return symptom_record.symptom_desc

    return ("n/a")    

@app.route('/add-user-symptom', methods=['POST'])
def add_user_symptom():
    """Add new symptom to database for user to track"""

    symptom_id = request.form.get("symptom_id")
    usercond_id = request.form.get("usercond_id")

    # Check if symptom is tracked (for any condition)
    user_symptoms = (db.session
                       .query(UserSymptom)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_symptom in user_symptoms:
        if int(symptom_id) == user_symptom.symptom_id:

            # if sympotom was previously tracked, change back to track again 
            # and make sure associated with correct condition
            if user_symptom.is_tracked==False:
                user_symptom.is_tracked = True
                user_symptom.usercond_id = usercond_id
                db.session.commit()
                return "Symptom is now tracked again"

            return "Add symptom failed - this symptom is already tracked"

    new_symptom = UserSymptom(symptom_id=symptom_id,
                              usercond_id=usercond_id)

    db.session.add(new_symptom)
    db.session.commit()
    return "Symptom Added"

@app.route('/get-value-desc', methods=['GET'])
def get_value_description():
    """Get description of value item from database"""

    value_id = request.args.get("value_id")

    if value_id:
        value_record = (ValueType.query
                                 .filter(ValueType.value_id_pk==value_id)
                                 .first())

        if value_record.value_desc:
            return value_record.value_desc

    return ("n/a")    

@app.route('/add-user-value', methods=['POST'])
def add_user_value():
    """Add new value to database for user to track"""

    value_id = request.form.get("value_id")
    usercond_id = request.form.get("usercond_id")

    user_values = (db.session
                       .query(UserValueType)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_value in user_values:
        if int(value_id) == user_value.value_id:

            if user_value.is_tracked==False:
                user_value.is_tracked = True
                user_value.usercond_id = usercond_id
                db.session.commit()
                return "Value item is now tracked again"

            return "Add value item failed - this value item is already tracked"

    new_value = UserValueType(value_id=value_id,
                              usercond_id=usercond_id)

    db.session.add(new_value)
    db.session.commit()
    return "Value Item Added"

@app.route('/get-count-desc', methods=['GET'])
def get_count_description():
    """Get description of count item from database"""

    count_id = request.args.get("count_id")

    if count_id:
        count_record = (CountType.query
                                 .filter(CountType.count_id_pk==count_id)
                                 .first())

        if count_record.count_desc:
            return count_record.count_desc

    return ("n/a")    

@app.route('/add-user-count', methods=['POST'])
def add_user_count():
    """Add new count to database for user to track"""

    count_id = request.form.get("count_id")
    usercond_id = request.form.get("usercond_id")

    user_counts = (db.session
                       .query(UserCountType)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_count in user_counts:
        if int(count_id) == user_count.count_id:

            if user_count.is_tracked==False:
                user_count.is_tracked = True
                user_count.usercond_id = usercond_id
                db.session.commit()
                return "Count item is now tracked again"

            return "Add count item failed - this count item is already tracked"

    new_count = UserCountType(count_id=count_id,
                              usercond_id=usercond_id)

    db.session.add(new_count)
    db.session.commit()
    return "Count Item Added"

# The next 4 routes are used from stop_tracking.html
# and associated .js files to stop tracking items

@app.route('/stop-user-condition', methods=['POST'])
def stop_tracking_user_condition():
    """Stop tracking condition and associated data in database"""

    cond_id = request.form.get("cond_id")

    user_conditions = (UserCondition.query
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_condition in user_conditions:
        if (int(cond_id) == user_condition.cond_id and 
        user_condition.is_tracked == True):
            user_condition.is_tracked = False

            user_symptoms = (db.session.query(UserSymptom)
                             .join(UserCondition)
                             .filter((UserCondition.user_id==session['userid']), 
                                     (UserCondition.cond_id==cond_id))
                             .all())
            user_values = (db.session.query(UserValueType)
                             .join(UserCondition)
                             .filter((UserCondition.user_id==session['userid']), 
                                     (UserCondition.cond_id==cond_id))
                             .all())
            user_counts = (db.session.query(UserCountType)
                             .join(UserCondition)
                             .filter((UserCondition.user_id==session['userid']), 
                                     (UserCondition.cond_id==cond_id))
                             .all())

            for user_symptom in user_symptoms:
                user_symptom.is_tracked = False
            for user_value in user_values:
                user_value.is_tracked = False
            for user_count in user_counts:
                user_count.is_tracked = False

            db.session.commit()
            return "Condition (and sub data) are no longer tracked"

    return "Condition was not tracked - no change"

@app.route('/stop-user-symptom', methods=['POST'])
def stop_tracking_user_symptom():
    """Stop tracking symptoms in database"""

    symptom_id = request.form.get("symptom_id")

    user_symptoms = (db.session
                       .query(UserSymptom)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_symptom in user_symptoms:
        if (int(symptom_id) == user_symptom.symptom_id and
        user_symptom.is_tracked == True):
            user_symptom.is_tracked = False
            db.session.commit()
            return "Symptom is no longer tracked"

    return "Symptom was not tracked - no change"

@app.route('/stop-user-value', methods=['POST'])
def stop_tracking_user_value():
    """Stop tracking value items in database"""

    value_id = request.form.get("value_id")

    user_values = (db.session
                       .query(UserValueType)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_value in user_values:
        if (int(value_id) == user_value.value_id and
        user_value.is_tracked == True):
            user_value.is_tracked = False
            db.session.commit()
            return "Value item is no longer tracked"

    return "Value item was not tracked - no change"

@app.route('/stop-user-count', methods=['POST'])
def stop_tracking_user_count():
    """Stop tracking count items in database"""

    count_id = request.form.get("count_id")

    user_counts = (db.session
                       .query(UserCountType)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_count in user_counts:
        if (int(count_id) == user_count.count_id and
        user_count.is_tracked == True):
            user_count.is_tracked = False
            db.session.commit()
            return "Count item is no longer tracked"

    return "Count item was not tracked - no change"

# The next 3 routes are used by query.html and associated js files
# to query data and find correlations

@app.route('/query-user-symptom.json', methods=['GET'])
def query_user_symptom():
    """Query database for correlations with symptom data items"""

    symptom_id = request.args.get("symptom_id")

    user_symptom_logs = (db.session.query(SymptomItem)
                                  .join(UserSymptom)
                                  .join(UserCondition)
                                  .filter(UserSymptom.symptom_id==symptom_id, 
                                          SymptomItem.symptom_present==True,
                                          UserCondition.user_id==session['userid'])
                                  .all())
    dates = set()

    for entry in user_symptom_logs:
        dates.add(entry.symptom_date.date())

    query_result = query_dates(dates)

    sorted_result = []
    for item in sorted(query_result, key=query_result.get, reverse=True):
        sorted_result.append((item, query_result[item]))

    return jsonify(sorted_result)

@app.route('/query-user-value.json', methods=['GET'])
def query_user_value():
    """Query database for correlations with value type data items"""

    value_id = request.args.get("value_id")

    user_value_logs = (db.session.query(ValueItem)
                                  .join(UserValueType)
                                  .join(UserCondition)
                                  .filter(UserValueType.value_id==value_id, 
                                          ValueItem.value > 0,
                                          UserCondition.user_id==session['userid'])
                                  .all())
    dates = set()

    for entry in user_value_logs:
        dates.add(entry.value_date.date())

    query_result = query_dates(dates)

    sorted_result = []
    for item in sorted(query_result, key=query_result.get, reverse=True):
        sorted_result.append((item, query_result[item]))

    return jsonify(sorted_result)

@app.route('/query-user-count.json', methods=['GET'])
def query_user_count():
    """Query database for correlations with count type data items"""

    count_id = request.args.get("count_id")

    user_count_logs = (db.session.query(CountItem)
                                  .join(UserCountType)
                                  .join(UserCondition)
                                  .filter(UserCountType.count_id==count_id, 
                                          CountItem.count > 0,
                                          UserCondition.user_id==session['userid'])
                                  .all())
    dates = set()

    for entry in user_count_logs:
        dates.add(entry.count_date.date())

    query_result = query_dates(dates)

    sorted_result = []
    for item in sorted(query_result, key=query_result.get, reverse=True):
        sorted_result.append((item, query_result[item]))

    return jsonify(sorted_result)


# Helper functions

def update_value_item_db(user_value_id, date, value):
    """Update database with new/updated value item"""

    if value=="":
        value = None

    datarecord = (ValueItem.query
                           .filter(ValueItem.user_value_id==user_value_id,
                                   func.date(ValueItem.value_date)==date)
                           .first())   

    if datarecord: 
        datarecord.value = value
        db.session.commit()
        return "Record Updated"

    new_value = ValueItem(value_date=date,
                          value=value,
                          user_value_id=user_value_id)

    db.session.add(new_value)
    db.session.commit()

    return "Record Added"


def airnow_api(date, zipcode, distance):
    """Process data to send to AirNOW API"""
    
    value = None
    today=datetime.now().date()

    if date == str(today):
        payload = {'format': "application/json",
                   'zipCode': zipcode,
                   'distance': distance,
                   'API_KEY': AIRNOW
                  }
        url = 'http://www.airnowapi.org/aq/observation/zipCode/current'
   
    else:
        # date=datetime.strptime(date, "%Y-%m-%d")
        payload = {'format': "application/json",
                   'zipCode': zipcode,
                   'date': date+"T00-0000",
                   'distance': distance,
                   'API_KEY': AIRNOW
                   }

        url = 'http://www.airnowapi.org/aq/observation/zipCode/historical'

    data = get_airnow_data(url, payload)

    for item in data:
        if (item['ParameterName'] == 'O3' or 
            item['ParameterName'] == 'OZONE'):
            value = item['AQI']

    return value


def get_airnow_data(url, payload):
    """Call to AirNOW API to get air quality data"""

    response = requests.get(url,payload)
    return response.json()


def query_dates(dates):
    """Query database for events that happened on given dates"""

    user_symptoms = (db.session.query(UserSymptom)
                     .join(UserCondition)
                     .filter((UserCondition.user_id==session['userid']), 
                             (UserSymptom.is_tracked==True))
                     .all())
    user_values = (db.session.query(UserValueType)
                     .join(UserCondition)
                     .filter((UserCondition.user_id==session['userid']), 
                             (UserValueType.is_tracked==True))
                     .all())
    user_counts = (db.session.query(UserCountType)
                     .join(UserCondition)
                     .filter((UserCondition.user_id==session['userid']), 
                             (UserCountType.is_tracked==True))
                     .all())

    query_result = {}

    for symptom in user_symptoms:
        name = symptom.symptom.symptom_name
        query_result[name] = 0
        for item in symptom.symptom_items:
            if (
                item.symptom_date.date() in dates and 
                item.symptom_present == True
                ):
                query_result[name] += 1

    for value in user_values:
        name = value.value_type.value_name
        query_result[name] = 0
        for item in value.value_items:
            if (
                item.value_date.date() in dates and 
                item.value > 0
                ):
                query_result[name] += 1    

    for count in user_counts:
        name = count.count_type.count_name
        query_result[name] = 0
        for item in count.count_items:
            if (
                item.count_date.date() in dates and 
                item.count > 0
                ):
                query_result[name] += 1

    return query_result


def user_tracked_info():
    """Query database for information user is tracking"""

    conds = {}

    for cond in user_tracked_conditions():

        name = cond.condition.cond_name
        conds[name]={}

        conds[name]['symptoms']=user_tracked_symptoms(cond)
        conds[name]['value_types']=user_tracked_value_types(cond)
        conds[name]['count_types']=user_tracked_count_types(cond)            

    return conds


def user_tracked_conditions():
    """Query database for UserConditions user is tracking"""

    user_conditions = (db.session.query(UserCondition)
              .filter(UserCondition.user_id==session['userid'])
              .all())

    cond_list = []

    for cond in user_conditions:
        if cond.is_tracked:
            cond_list.append(cond)

    return cond_list


def user_tracked_symptoms(cond):
    """Query database for symptoms user is tracking for given condition"""

    symptoms = (db.session.query(UserSymptom, Symptom)
                  .join(Symptom)
                  .filter(UserSymptom.usercond_id==cond.usercond_id_pk)
                  .all())

    symptom_list = []

    for symptom in symptoms:
        if symptom.UserSymptom.is_tracked:
            symptom_list.append(symptom)

    return symptom_list


def user_tracked_value_types(cond):
    """Query database for value types user is tracking for given condition"""

    value_types = (db.session.query(UserValueType, ValueType)
                   .join(ValueType)
                   .filter(UserValueType.usercond_id==cond.usercond_id_pk)
                   .all())

    value_list = []

    for value in value_types:
        if value.UserValueType.is_tracked:
            value_list.append(value)

    return value_list


def user_tracked_count_types(cond):
    """Query database for count types user is tracking for given condition"""

    count_types = (db.session.query(UserCountType, CountType)
                   .join(CountType)
                   .filter(UserCountType.usercond_id==cond.usercond_id_pk)
                   .all())

    count_list = []

    for count in count_types:
        if count.UserCountType.is_tracked:
            count_list.append(count)

    return count_list


def user_tracked_conditions_name():
    """Condition objects user is tracking"""

    user_conditions = (db.session.query(Condition)
                         .join(UserCondition)
                         .filter((UserCondition.user_id==session['userid']),
                                 (UserCondition.is_tracked==True))
                         .all())

    return user_conditions  


def user_not_tracked_conditions():
    """Conditions user is not tracking"""

    unused_conditions = []

    all_conditions = Condition.query.all()
    user_conditions = user_tracked_conditions_name()

    for condition in all_conditions:
        if condition not in user_conditions:
            unused_conditions.append(condition)

    return unused_conditions     


def user_not_tracked_symptoms():
    """Symptoms user is not tracking"""

    unused_symptoms = []
    all_symptoms = Symptom.query.all()
    user_symptoms = (db.session.query(Symptom)
                       .join(UserSymptom)
                       .join(UserCondition)
                       .filter((UserSymptom.is_tracked==True),
                               (UserCondition.user_id==session['userid']))
                       .all())

    for symptom in all_symptoms:
        if symptom not in user_symptoms:
            unused_symptoms.append(symptom)

    return unused_symptoms


def user_not_tracked_value_types():
    """Value types user is not tracking"""

    unused_values = []
    all_values = ValueType.query.all()
    user_values = (db.session.query(ValueType)
                     .join(UserValueType)
                     .join(UserCondition)
                     .filter((UserValueType.is_tracked==True),
                             (UserCondition.user_id==session['userid']))
                     .all())

    for value in all_values:
        if value not in user_values:
            unused_values.append(value)    

    return unused_values


def user_not_tracked_count_types():
    """Count types user is not tracking"""

    unused_counts = []
    all_counts = CountType.query.all()
    user_counts = (db.session.query(CountType)
                     .join(UserCountType)
                     .join(UserCondition)
                     .filter((UserCountType.is_tracked==True),
                             (UserCondition.user_id==session['userid']))
                     .all())

    for count in all_counts:
        if count not in user_counts:
            unused_counts.append(count)

    return unused_counts


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
    # app.run(debug=True)