
"""Health Tracker"""

# from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
from model import User, UserCondition, Condition
from model import Symptom, UserSymptom, SymptomItem
from model import ValueType, UserValueType, ValueItem
from model import CountType, UserCountType, CountItem


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'THISISSECRETHERE'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    if session.get('userid'):
        return redirect('/{}'.format(session['userid']))

    return redirect('/login')

@app.route('/login', methods=["GET"])
def show_login_form():
    """Show login/registration form"""

    if session.get('userid'):
        flash('Already logged in.')

        return redirect('/{}'.format(session['userid']))

    return render_template('login_form.html')

@app.route('/login', methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter(User.email == email).first()

    if user:
        if password == user.password:
            session['userid']=user.user_id_pk
            flash('Log in successful')
            return redirect('/{}'.format(session['userid']))

    flash("Login Failed")
    return redirect('/login')


# pulling in favicon.ico instead of userid.  FIGURE THIS OUT!!!
@app.route('/<userid>')
def user_main_page(userid):
    """Show individual user main page"""
    userid=int(userid)

    if session.get('userid'):
        if userid == session['userid']:   
            user = User.query.get(userid)
            return render_template('usermainpage.html', user=user)

        flash("You don't have permission to view this page.")
        return redirect('/{}'.format(session['userid']))

    flash("You don't have permission to view this page.")
    return redirect('/login')





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