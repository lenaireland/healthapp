"""Tests for Health Tracking Flask app."""

from unittest import TestCase
from server import app
from model import connect_to_db, db
from seed import example_data
from flask import session

class LoggedOutTests(TestCase):
    """Tests for when no one is logged in."""

class FlaskTestsDatabase(TestCase):
    """Tests for when user is logged in."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Drop all tables first
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()



if __name__ == "__main__":
    unittest.main()