# HealthTracker

HealthTracker is a tool that allows users to take charge of their health conditions by logging personalized daily information.  Users can then use the accumulated daily data to identify personal triggers to avoid or know when extra medication may be necessary.  Features include daily item logging, custom item trackers, manual data review, query of logged items to find common occurrences, and graphical presentation of longitudinal data.

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [About Me](#aboutme)

## <a name="tech-stack"></a>Tech Stack

__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy <br/>
__Frontend:__ JavaScript, jQuery, AJAX, Jinja2, D3, Bootstrap, HTML5, CSS3 <br/>
__API:__ AirNOW <br/>

## <a name="features"></a>Features

Features include daily item logging, custom item trackers, manual data review, query of logged items to find common occurrences, and graphical presentation of longitudinal data.

## <a name="installation"></a>Setup/Installation

#### Requirements:

- PostgreSQL
- Python 3.6
- AirNOW API key

To have this app running on your local computer, please follow the below steps:

Install PostgreSQL

Clone or fork this repository:
```
$ git clone https://github.com/lenaireland/healthapp.git
```

Create a virtual environment inside your healthapp directory:
```
$ virtualenv env
```

Activate the virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip install -r requirements.txt
```

Sign up to use the [AirNOW API](https://docs.airnowapi.org/account/request/) and obtain an API key. Save it to a file `secrets.sh`, along with a secret key you choose for the app. Your file should look something like this:
```
export SECRET_KEY = 'xyz'
export AIRNOW_KEY= = 'abc'
```

Source your keys from your `secrets.sh` file into your virtual environment:
```
$ source secrets.sh
```

Create database 'health'.
```
$ createdb health
```

Create your database tables and seed example data.
```
$ python3 model.py
$ python3 seed.py
```

If you want to use SQLAlchemy to query the database, you can run the model in interactive mode
```
$ python3 -i model.py
```

Run the app from the command line.
```
$ python3 server.py
```

You can now navigate to 'localhost:5000/' to access HealthTracker.

## <a name="aboutme"></a>About Me
Lena Ireland is a Software Engineer in the Bay Area; this is her first project.
Visit her on [LinkedIn](http://www.linkedin.com/in/lenaireland).