from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Calendar(db.Model):
    """Model class for events table in database"""

    __tablename__ = "events"
    key = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    summary = db.Column(db.String, nullable=False)
    attendees = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    start = db.Column(db.String, nullable=False)
    datetime_start = db.Column(db.String, nullable=False)
    end = db.Column(db.String, nullable=False)
    datetime_end = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, default=True)
    calendar_id = db.Column(db.String, nullable=True)


class User(db.Model):
    """Model class for users table in database"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)


class Previous(db.Model):
    """Model class for previous lessons table in database"""

    __tablename__ = "previous"
    prev_key = db.Column(db.Integer, primary_key=True)
    prev_user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                             nullable=False)
    prev_summary = db.Column(db.String, nullable=False)
    prev_attendees = db.Column(db.String, nullable=False)
    prev_date = db.Column(db.String, nullable=False)
    prev_start = db.Column(db.String, nullable=False)
    prev_datetime_start = db.Column(db.String, nullable=False)
    prev_end = db.Column(db.String, nullable=False)
    prev_datetime_end = db.Column(db.String, nullable=False)
    prev_confirmed = db.Column(db.Boolean, default=True)
