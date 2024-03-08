from flask import redirect, session
from functools import wraps
from models import User
from sqlalchemy import text


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def admin_check():
    """Check if user is an admin"""
    return User.query.get(session["user_id"]).username == "admin"

def get_username(user_id):
    """Get username of user based on ID"""
    return User.query.get(user_id).username

def get_email(user_id=None, username=None, db=None):
    "Get email of user based on either ID or username."
    if username is not None:
        return User.query.filter_by(username=username).first().email

    return db_query(db, "SELECT email FROM users WHERE id = " + str(user_id))[0][0]


def db_query(db, query):
    """Execute a database query and return the results"""
    return db.engine.execute(text(query)).all()
