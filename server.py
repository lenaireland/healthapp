
"""Health Tracker"""

# from jinja2 import StrictUndefined

from flask import Flask



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "THISISSECRETHERE"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
# app.jinja_env.undefined = StrictUndefined