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
    zipcode = db.Column(db.String(5), nullable=True)

    #Define relationships
    # user_conditions=db.relationship("UserCondition")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id={}, email={}>".format(self.user_id_pk, self.email)


class Condition(db.Model):
    """Condition names for health tracking website"""

    __tablename__ = "conditions"

    cond_id_pk = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cond_name = db.Column(db.String(32), nullable=False)
    cond_desc = db.Column(db.String(200), nullable=True)

    #Define relationships
    # user_conditions=db.relationship("UserCondition")

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
                        db.ForeignKey("conditions.cond_id_pk"), 
                        nullable=False)

    # Define relationships
    user = db.relationship("User", backref="user_conditions")
    condition = db.relationship("Condition", backref="user_conditions")
    user_symptoms = db.relationship("UserSymptom")
    user_value_types = db.relationship("UserValueType")
    user_count_types = db.relationship("UserCountType")

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

    # Define relationships
    user_symptoms = db.relationship("UserSymptom")

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

    # Define relationships
    user_condition = db.relationship("UserCondition")
    symptom = db.relationship("Symptom")
    symptom_items = db.relationship("SymptomItem")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Symptom id={}, user condition id={}>".format(self.symptom_id, 
                                                              self.usercond_id)


class SymptomItem(db.Model):
    """Symptom occurrence logged by user"""

    __tablename__ = "symptom_items"

    symptom_item_id = db.Column(db.Integer, 
                                autoincrement=True, 
                                primary_key=True)
    symptom_date = db.Column(db.DateTime, nullable=False)
    symptom_present = db.Column(db.Boolean, nullable=False)
    user_symptom_id = db.Column(db.Integer, 
                            db.ForeignKey("user_symptoms.user_symptom_id_pk"), 
                            nullable=False)

    # Define relationships
    user_symptom = db.relationship("UserSymptom")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<ID: {},
                   DateTime: {},
                   present? {},  
                   user symp id={}>""".format(self.symptom_item_id,
                                                 self.symptom_date,
                                                 self.symptom_present, 
                                                 self.user_symptom_id)


class ValueType(db.Model):
    """Value data available to track (e.g. test results, obtained data)"""

    __tablename__ = "value_types"

    value_id_pk = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    value_name = db.Column(db.String(32), nullable=False)
    value_desc = db.Column(db.String(200), nullable=True)

    # Define relationships
    user_value_types = db.relationship("UserValueType")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Value type id={}, name={}>".format(self.value_id_pk, 
                                                    self.value_name)


class UserValueType(db.Model):
    """Value item a user is tracking"""

    __tablename__ = "user_value_types"

    user_value_id_pk = db.Column(db.Integer, 
                                   autoincrement=True, 
                                   primary_key=True)
    value_id = db.Column(db.Integer, 
                         db.ForeignKey("value_types.value_id_pk"), 
                         nullable=False)
    usercond_id = db.Column(db.Integer, 
                            db.ForeignKey("user_conditions.usercond_id_pk"), 
                            nullable=False)

    # Define relationships
    user_condition = db.relationship("UserCondition")
    value_type = db.relationship("ValueType")
    value_items = db.relationship("ValueItem")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Value type id={}, 
                  user condition id={}>""".format(self.value_id, 
                                                  self.usercond_id)


class ValueItem(db.Model):
    """Symptom occurrence logged by user"""

    __tablename__ = "value_items"

    value_item_id = db.Column(db.Integer, 
                                autoincrement=True, 
                                primary_key=True)
    value_date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Numeric, nullable=False)
    user_value_id = db.Column(db.Integer, 
                              db.ForeignKey("user_value_types.user_value_id_pk"), 
                              nullable=False)

    # Define relationships
    user_value_item = db.relationship("UserValueType")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<ID: {},
                   DateTime:{}, 
                   value= {}, 
                   user value id={}>""".format(self.value_item_id,
                                               self.value_date,
                                               self.value, 
                                               self.user_value_id)


class CountType(db.Model):
    """Count data available to track (e.g. medication)"""

    __tablename__ = "count_types"

    count_id_pk = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    count_name = db.Column(db.String(32), nullable=False)
    count_desc = db.Column(db.String(200), nullable=True)

    # Define relationships
    user_count_types = db.relationship("UserCountType")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Count type id={}, name={}>".format(self.count_id_pk, 
                                                    self.count_name)


class UserCountType(db.Model):
    """Count item a user is tracking"""

    __tablename__ = "user_count_types"

    user_count_id_pk = db.Column(db.Integer, 
                                 autoincrement=True, 
                                 primary_key=True)
    count_id = db.Column(db.Integer, 
                         db.ForeignKey("count_types.count_id_pk"), 
                         nullable=False)
    usercond_id = db.Column(db.Integer, 
                            db.ForeignKey("user_conditions.usercond_id_pk"), 
                            nullable=False)

    # Define relationships
    user_condition = db.relationship("UserCondition")
    count_type = db.relationship("CountType")
    count_items = db.relationship("CountItem")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Count type id={}, 
                  user condition id={}>""".format(self.count_id, 
                                                  self.usercond_id)


class CountItem(db.Model):
    """Symptom occurrence logged by user"""

    __tablename__ = "count_items"

    count_item_id = db.Column(db.Integer, 
                                autoincrement=True, 
                                primary_key=True)
    count_date = db.Column(db.DateTime, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    user_count_id = db.Column(db.Integer, 
                            db.ForeignKey("user_count_types.user_count_id_pk"), 
                            nullable=False)

    # Define relationships
    user_count_type = db.relationship("UserCountType")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<ID: {},
                   DateTime: {}, 
                   count= {}, 
                   user value id={}>""".format(self.count_item_id,
                                               self.count_date,
                                               self.count, 
                                               self.user_value_id)


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