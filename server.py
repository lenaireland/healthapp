
"""Health Tracker"""

import os
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect
from flask import flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime, timedelta

from model import connect_to_db, db
from model import User, UserCondition, Condition
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

    date=datetime.now().date().strftime("%Y-%m-%d")

    # if user is already logged in, take to personal page
    if session.get('userid'):
        return redirect('/user/{}/{}'.format(session['userid'], date))

    # if not logged in, show login/register form
    return render_template('login_form.html')

@app.route('/login', methods=['GET'])
def login_form():
    """Show login/registration form"""

    date=datetime.now().date().strftime("%Y-%m-%d")

    # if user is logged in, take to personal page
    # if not logged in, go to '/' route to login/register
    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/user/{}/{}'.format(session['userid'], date))

    return redirect('/') 

@app.route('/process-login', methods=['POST'])
def login_process():
    """Process Login"""

    date=datetime.now().date().strftime("%Y-%m-%d")

    # process login form data, query for user in database
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

    # if user email exists and password matches, login
    if user:
        if password == user.password:
            session['userid']=user.user_id_pk
            flash('Log in successful')
            return redirect('/user/{}/{}'.format(session['userid'], date))

    flash('Login Failed')
    return redirect('/')

@app.route('/register', methods=['GET'])
def register_form():
    """Show login/registration form"""

    date=datetime.now().date().strftime("%Y-%m-%d")
    # date=datetime.strftime()

    # if user is logged in, take to personal page
    # if not logged in, go to '/' route to login/register
    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/user/{}/{}'.format(session['userid'], date))

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

@app.route('/user/<userid>/<date>')
def user_day_page(userid, date):
    """Show individual user day pages"""

    userid=int(userid)
    date=datetime.strptime(date, "%Y-%m-%d").date()
    today=datetime.now().date()

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
        return redirect('/user/{}/{}'.format(session['userid'], date))

    flash('You do not have permission to view this page.')
    return redirect('/')


def user_tracked_info():
    """Query database for information user is tracking"""

    user = User.query.get(session['userid'])
    # conds = {}
    # for cond in user.user_conditions:
    #     name = cond.condition.cond_name
    #     conds[name]={}
    #     conds[name]['symptoms'] = []
    #     conds[name]['value_types'] = []
    #     conds[name]['count_types'] = []
    #     for usymptom in cond.user_symptoms:
    #         conds[name]['symptoms'].append(usymptom.symptom.symptom_name)
    #     for uvalue_type in cond.user_value_types:
    #         conds[name]['value_types'].append(uvalue_type.value_type.value_name)
    #     for ucount_type in cond.user_count_types:
    #         conds[name]['count_types'].append(ucount_type.count_type.count_name)

    # print(conds)
    # return conds

    conds = {}

    for cond in user.user_conditions:

        name = cond.condition.cond_name
        conds[name]={}

        symptoms = (db.session.query(UserCondition.user_id, 
                                     Symptom.symptom_name,
                                     UserSymptom.usercond_id, 
                                     UserSymptom.user_symptom_id_pk, 
                                     UserSymptom.symptom_id)
                    .join(UserSymptom)
                    .join(Symptom)
                    .filter(UserCondition.usercond_id_pk==cond.usercond_id_pk)
                    .all())

        value_types = (db.session.query(UserCondition.user_id, 
                                        ValueType.value_name,
                                        UserValueType.usercond_id, 
                                        UserValueType.user_value_id_pk, 
                                        UserValueType.value_id)
                       .join(UserValueType)
                       .join(ValueType)
                       .filter(UserCondition.usercond_id_pk==cond.usercond_id_pk)
                       .all())

        count_types = (db.session.query(UserCondition.user_id, 
                                        CountType.count_name,
                                        UserCountType.usercond_id, 
                                        UserCountType.user_count_id_pk, 
                                        UserCountType.count_id)
                       .join(UserCountType)
                       .join(CountType)
                       .filter(UserCondition.usercond_id_pk==cond.usercond_id_pk)
                       .all())

        conds[name]['symptoms'] = symptoms
        conds[name]['value_types'] = value_types
        conds[name]['count_types'] = count_types

    return conds


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