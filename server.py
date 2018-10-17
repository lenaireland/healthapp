
"""Health Tracker"""

import os
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


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

#######
#TO DO: Make homepage have logo, project info.  Login/Register on own pages.
#######

@app.route('/')
def index():
    """Homepage - show login/register form"""

    # if user is already logged in, take to personal page
    if session.get('userid'):
        return redirect('/user/{}'.format(session['userid']))

    # if not logged in, show login/register form
    return render_template('login_form.html')

@app.route('/login', methods=['GET'])
def login_form():
    """Show login/registration form"""

    # if user is logged in, take to personal page
    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/user/{}'.format(session['userid']))

    # if not logged in, go to '/' route to login/register
    return redirect('/') 

@app.route('/process-login', methods=['POST'])
def login_process():
    """Process Login"""

    # process login form data, query for user in database
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # if user email exists and password matches, login
    if user:
        if password == user.password:
            session['userid']=user.user_id_pk
            flash('Log in successful')
            return redirect('/user/{}'.format(session['userid']))

    flash('Login Failed')
    return redirect('/')

@app.route('/register', methods=['GET'])
def register_form():
    """Show login/registration form"""

    # if user is logged in, take to personal page
    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/user/{}'.format(session['userid']))

    # if not logged in, go to '/' route to login/register
    return redirect('/')

@app.route('/process-register', methods=['POST'])
def register_process():
    """Process user registration"""

    # process register form data, query for user in database
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # if there is a user in database that matches email redirect to '/'    
    if user:
        flash('Account already exists. Please login.')
        return redirect('/')

    # if email is not already in database, create new instance of User
    # class, add to database, login user, and take to settings page
    new_user = User(email=email, password=password)
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
        return redirect('/')

@app.route('/process-settings', methods=['POST'])
def process_user_settings():
    """Processing user settings update"""

    user=User.query.get(session['userid'])

    email = request.form.get('email')

    # check that e-mail does not yet exist in the system
    for user_email in db.session.query(User.email).all():
        if email == user_email[0]:
            flash('Error - this email is already in the system')
            return redirect('/settings')

    user.email = email
    user.password = request.form.get('password')
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

@app.route('/logout')
def logout():
    """Process user logout"""

    if session.get('userid'):    
        session.pop('userid')
        flash('Logged out.')
    
    return redirect('/')

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
    return redirect('/')

@app.route('/add-tracking')
def add_tracking():
    """Add new condition/symptom/count/value items for tracking"""

    if session.get('userid'):

        symptoms = Symptom.query.all()
        values = ValueType.query.all()
        counts = CountType.query.all()

        all_conditions = Condition.query.all()
        user_conditions = (db.session.query(Condition)
                            .join(UserCondition)
                            .filter(UserCondition.user_id==session['userid'])
                            .all())

        unused_conditions = []
        for condition in all_conditions:
            if condition not in user_conditions:
                unused_conditions.append(condition)

        return render_template('add_tracking.html', 
                               unused_conditions=unused_conditions,
                               user_conditions=user_conditions,
                               symptoms=symptoms,
                               counts=counts,
                               values=values)  
    
    return redirect('/')

@app.route('/stop-tracking')
def stop_tracking():
    """Remove condition/symptom/count/value items from tracking"""

    if session.get('userid'):

        user_conditions = user_tracked_conditions()

        symptoms = []
        values = []
        counts = []

        for cond in user_tracked_conditions():
            symptoms += user_tracked_symptoms(cond)
            values += user_tracked_value_types(cond)
            counts += user_tracked_count_types(cond)

        return render_template('stop_tracking.html', 
                               user_conditions=user_conditions,
                               symptoms=symptoms,
                               counts=counts,
                               values=values)  
    
    return redirect('/')

# The next 8 routes are used from usermainpage.html and 
# associated .js files to display tracked user symptoms and 
# update values

@app.route('/get-user-symptom', methods=['GET'])
def get_user_symptom():
    """Get user symptom values from database"""

    symptom_id = request.args.get("symptom_id")
    date = request.args.get("date")

    datarecord = SymptomItem.query.filter(
                    SymptomItem.user_symptom_id==symptom_id,
                    func.date(SymptomItem.symptom_date)==date).first()

    if datarecord:
        value = datarecord.symptom_present
        return str(value)

    return "False" 

@app.route('/update-user-symptom', methods=['POST'])
def update_user_symptom():
    """Process user symptoms"""

    symptom_id = request.form.get("symptom_id")
    date = request.form.get("date")
    TF = request.form.get("TF")

    datarecord = SymptomItem.query.filter(
                    SymptomItem.user_symptom_id==symptom_id,
                    func.date(SymptomItem.symptom_date)==date).first()

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
                user_symptom_id=symptom_id)

    db.session.add(new_symptom)
    db.session.commit()
    return "Record Added"

@app.route('/get-user-value-item', methods=['GET'])
def get_user_valueitem():
    """Get user value items from database"""

    value_id = request.args.get("value_id")
    date = request.args.get("date")

    datarecord = ValueItem.query.filter(
                    ValueItem.user_value_id==value_id,
                    func.date(ValueItem.value_date)==date).first()

    if datarecord:
        value = datarecord.value
        return str(value)

    return "False" 

@app.route('/update-user-value-item', methods=['POST'])
def update_user_value_item():
    """Process user value items"""

    value_id = request.form.get("value_id")
    date = request.form.get("date")
    value = request.form.get("value")

    if value=="":
        value = None

    datarecord = ValueItem.query.filter(
                    ValueItem.user_value_id==value_id,
                    func.date(ValueItem.value_date)==date).first()   

    if datarecord: 
        datarecord.value = value
        db.session.commit()
        return "Record Updated"

    new_value = ValueItem(value_date=date,
                          value=value,
                          user_value_id=value_id)

    db.session.add(new_value)
    db.session.commit()
    return "Record Added"

@app.route('/get-user-count-item', methods=['GET'])
def get_user_countitem():
    """Get user count items from database"""

    count_id = request.args.get("count_id")
    date = request.args.get("date")

    datarecord = CountItem.query.filter(
                    CountItem.user_count_id==count_id,
                    func.date(CountItem.count_date)==date).first()

    if datarecord:
        count = datarecord.count
        return str(count)

    return "False" 

@app.route('/update-user-count-item', methods=['POST'])
def update_user_count_item():
    """Process user count items"""

    count_id = request.form.get("count_id")
    date = request.form.get("date")
    count = request.form.get("count")

    if count=="":
        count = None

    datarecord = CountItem.query.filter(
                    CountItem.user_count_id==count_id,
                    func.date(CountItem.count_date)==date).first()   
                    
    if datarecord: 
        datarecord.count = count
        db.session.commit()
        return "Record Updated"

    new_count = CountItem(count_date=date,
                          count=count,
                          user_count_id=count_id)

    db.session.add(new_count)
    db.session.commit()
    return "Record Added"

@app.route('/get-user-log', methods=['GET'])
def get_user_log():
    """Get user daily log from database"""

    date = request.args.get("date")

    datarecord = UserLog.query.filter(func.date(UserLog.log_date)==date).first()

    if datarecord:
        log_text = datarecord.log_text
        return log_text

    return "False"

@app.route('/update-user-log', methods=['POST'])
def update_user_log():
    """Process user count items"""

    date = request.form.get("date")
    text = request.form.get("text")

    datarecord = UserLog.query.filter(func.date(UserLog.log_date)==date).first()   
                    
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

@app.route('/add-user-condition', methods=['POST'])
def add_user_condition():
    """Add new condition to database for user to track"""

    cond_id = request.form.get("cond_id")

    user_conditions = (UserCondition.query
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_condition in user_conditions:
        if int(cond_id) == user_condition.cond_id:

            if user_condition.UserCondition.is_tracked==False:
                user_condition.UserCondition.is_tracked = True
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

    user_symptoms = (db.session
                       .query(UserSymptom)
                       .join(UserCondition)
                       .filter(UserCondition.user_id==session['userid'])
                       .all())

    for user_symptom in user_symptoms:
        if int(symptom_id) == user_symptom.symptom_id:

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
                user_value.UserValueType.usercond_id = usercond_id
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
        if int(cond_id) == user_condition.cond_id:
            user_condition.UserCondition.is_tracked = False

            user_symptoms = (db.session.query(UserSymptom)
                               .join(UserCondition)
                               .filter((UserCondition.user_id==1), 
                                       (UserSymptom.usercond_id==1))
                               .all())
            user_values = (db.session.query(UserValueType)
                             .join(UserCondition)
                             .filter((UserCondition.user_id==1), 
                                     (UserValueType.usercond_id==1))
                             .all())
            user_counts = (db.session.query(UserCountType)
                             .join(UserCondition)
                             .filter((UserCondition.user_id==1), 
                                     (UserCountType.usercond_id==1))
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
        if int(symptom_id) == user_symptom.symptom_id:
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
        if int(value_id) == user_value.value_id:
            user_value.is_tracked = False
            db.session.commit()
            return "Value item is no longer tracked"

    return "Value was not tracked - no change"

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
        if int(count_id) == user_count.count_id:
            user_count.is_tracked = False
            db.session.commit()
            return "Symptom is no longer tracked"

    return "Symptom was not tracked - no change"


# helper functions

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
    """Query database for conditions user is tracking"""

    user_conditions = (db.session.query(UserCondition)
              .filter(UserCondition.user_id==session['userid'])
              .all())

    cond_list = []

    for cond in user_conditions:
        if cond.is_tracked:
            cond_list.append(cond)

    return cond_list


def user_tracked_symptoms(cond):
    """Query database for symptoms user is tracking"""

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
    """Query database for value types user is tracking"""

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
    """Query database for count types user is tracking"""

    count_types = (db.session.query(UserCountType, CountType)
                   .join(CountType)
                   .filter(UserCountType.usercond_id==cond.usercond_id_pk)
                   .all())

    count_list = []

    for count in count_types:
        if count.UserCountType.is_tracked:
            count_list.append(count)

    return count_list


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