"""Models and database functions for Health Tracking project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################

# Model definitions

class User(db.Model):
    """User of health tracking website."""

    __tablename__ = "users"

    user_id_pk = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(32), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id={}, email={}>".format(self.user_id_pk, self.email)


class Condition(db.Model):
    """Condition names for health tracking website"""

    __tablename__ = "conditions"

    cond_id_pk = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cond_name = db.Column(db.String(32), nullable=False)
    cond_desc = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Condition id={}, name ={}>".format(self.cond_id_pk, 
                                                    self.cond_name)


class UserCondition(db.Model):
    """Individual user conditions for health tracking website"""

    __tablename__ = "user_conditions"

    usercond_id_pk = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id_pk"), 
                        nullable=False)
    cond_id = db.Column(db.Integer, 
                        db.ForeignKey("conditions.condition_id_pk"), 
                        nullable=False)

    # Define relationships
    user = db.relationship("User", 
                           backref=("user_conditions", 
                                    order_by=usercond_id_pk))

    condition = db.relationship("Condition", 
                           backref=("user_conditions", 
                                    order_by=usercond_id_pk))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id={}, condition id={}>".format(self.user_id, 
                                                      self.cond_id)


class Symptom(db.Model):
    """Symptoms available to track"""

    __tablename__ = "symptoms"

    symptom_id_pk = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(32), nullable=False)
    symptom_desc = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Symptom id={}, name={}>".format(self.symptom_id_pk, 
                                                 self.symptom_name)


class UserSymptom(db.Model):
    """Symptom a user is tracking"""

    __tablename__ = "user_symptoms"

    user_symptom_id_pk = db.Column(db.Integer, 
                                   autoincrement=True, 
                                   primary_key=True)
    symptom_id = db.Column(db.Integer, 
                           db.ForeignKey("symptoms.symptom_id_pk"), 
                           nullable=False)
    usercond_id = db.Column(db.Integer, 
                           db.ForeignKey("user_conditions.usercond_id_pk"), 
                           nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Symptom id={}, user condition id={}>".format(self.symptom_id, 
                                                              self.usercond_id)


class ValueType(db.Model):
    """Value data available to track (e.g. test results, obtained data)"""

    __tablename__ = "value_types"

    value_type_id_pk = db.Column(db.Integer, 
                                 autoincrement=True, 
                                 primary_key=True)
    value_type_name = db.Column(db.String(32), nullable=False)
    value_type_desc = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Value type id={}, name={}>".format(self.value_type_id_pk, 
                                                    self.value_type_name)


class CountType(db.Model):
    """Count data available to track (e.g. medication)"""

    __tablename__ = "count_types"

    count_type_id_pk = db.Column(db.Integer, 
                                 autoincrement=True, 
                                 primary_key=True)
    count_type_name = db.Column(db.String(32), nullable=False)
    count_type_desc = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Count type id={}, name={}>".format(self.count_type_id_pk, 
                                                    self.count_type_name)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///health'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")