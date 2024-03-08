import os
import get_calendar
import get_previous
import insert_events
import delete_events
import confirm

from flask import Flask, request, flash
from flask import render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *
from models import *

from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Initialize database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route('/')
def index():
    """Render the welcome page"""

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        user = User.query.filter_by(
            username=request.form.get("username")).first()

        if user is None or not check_password_hash(user.hash, request.form.get(
                "password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = user.id

        # Remember log in status
        session['logged_in'] = True

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Log user out"""

    # Forget any user_id and login status
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Check student key
        if request.form.get("studentkey") != 'test_key':
            flash("Invalid Student Key!")
            render_template("register.html")
        # Check for password confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords entered do not match!")
            return render_template("register.html")

        username = request.form.get("username")

        # Check if username is already in database
        if User.query.filter_by(
                username=request.form.get("username")).first() is not None:
            flash("Username has been taken!")
            return render_template("register.html")

        email = request.form.get("email")

        # Check if email is already in database
        if User.query.filter_by(
                email=request.form.get("email")).first() is not None:
            flash("E-mail has been registered!")
            return render_template("register.html")

        # Generate password hash and add new user to database
        pass_hash = generate_password_hash(request.form.get("password"),
                                           method='pbkdf2:sha256',
                                           salt_length=8)
        new_user = User(username=username, email=email, hash=pass_hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration Successful!")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route('/calendar', methods=["GET", "POST"])
@login_required
def calendar():
    """Render the calendar page and handle lesson bookings"""

    # Retrieve calendar from Google API and load to database
    get_calendar.main()

    # Set current date and date in three months
    today = date.today()
    three_months = date.today() + relativedelta(months=+3)

    # Retrieve all events from database
    events = db_query(db, "SELECT * FROM events")

    # Retrieve username of logged-in user
    username = get_username(session["user_id"])

    # Handle lesson bookings
    if request.method == "POST":

        # Retrieve date and time from forms and parses to match Google format
        lesson_date = request.form.get("date")
        start_time = request.form.get("start_hour") + request.form.get(
            "start_minute")
        start_parsed = parser.parse(start_time)
        start_time = str(start_parsed)[11:16]  # Index only the time
        duration = int(request.form.get("duration"))
        end_time = str(start_parsed + relativedelta(minutes=+duration))[
                   11:16]  # Index only the time
        start_datetime = lesson_date + 'T' + str(start_time) + ':00+02:00'
        end_datetime = lesson_date + 'T' + str(end_time) + ':00+02:00'

        # Check for conflict with existing lessons
        conflict_check = db_query(db,
                                  "SELECT * FROM events "
                                  "WHERE date = " + "'" + lesson_date + "'")

        # First check against date, then time of existing lessons
        if len(conflict_check) != 0:
            for lessons in conflict_check:
                existing_start = parser.parse(lessons[6])
                existing_end = parser.parse(lessons[8])
                new_start = parser.parse(str(start_datetime))
                new_end = parser.parse(end_datetime)
                if existing_start <= new_start < existing_end or \
                        existing_start < new_end <= existing_end:
                    flash("Booking failed: Timeslot is not available!")
                    return redirect("/calendar")

        # Retrieve e-mail of logged-in user
        email = get_email(user_id=session["user_id"], db=db)

        # Add new lesson to the database
        new_booking = Calendar(user_id=session["user_id"], summary=username,
                               attendees=email, date=lesson_date,
                               start=str(start_time) + ':00+02:00',
                               datetime_start=start_datetime,
                               end=end_time + ':00+02:00',
                               datetime_end=end_datetime, confirmed=False)
        db.session.add(new_booking)

        # Commit the changes and insert event into the Google calendar
        db.session.commit()
        insert_events.main(username, start_datetime, end_datetime, email)
        return redirect("/calendar")

    return render_template("calendar.html", today=today,
                           three_months=three_months, events=events,
                           username=username)


@app.route('/profile_redir')
@login_required
def profile_redir():
    """Redirect to the profile page of the logged-in user"""

    url = "/profile/" + str(get_username(session["user_id"]))
    return redirect(url)


@app.route('/profile/<username>', methods=["GET", "POST"])
@login_required
def profile(username):
    """Render the profile page for the given user"""

    # Check if the user is either admin or owner of profile
    username_check = get_username(session["user_id"])
    is_admin = admin_check()

    if username_check == username or is_admin:
        pass
    else:
        return redirect("/calendar")

    # Retrieve email of the user
    email = get_email(username=username)

    # Update the lessons database
    get_calendar.main()

    # Retrieve upcoming lessons for the requested user
    upcoming_lessons = db_query(db,
                                "SELECT * FROM events "
                                "JOIN users ON events.user_id=users.id "
                                "WHERE username=" + "'" + username + "'")

    # Update the previous lessons database
    get_previous.main()

    # Retrieve previous lessons for the requested user
    previous_lessons = db_query(db,
                                "SELECT * FROM previous "
                                "JOIN users ON previous.prev_user_id=users.id "
                                "WHERE username=" + "'" + username + "'")
    len_upcoming = len(upcoming_lessons)
    len_previous = len(previous_lessons)

    # Handle confirming or canceling lessons
    if request.method == "POST":
        redir_url = "/profile/" + username
        if request.form.get("confirm") is not None:
            event_id = request.form.get("confirm")
            confirm.main(event_id)
            flash("Lesson Confirmed!")
        elif request.form.get("cancel") is not None:
            event_id = request.form.get("cancel")
            delete_events.main(event_id)
            flash("Lesson successfully cancelled!")

        # Handle loading all upcoming and previous lessons
        elif request.form.get("view_upcoming") is not None:
            return render_template("profile.html", name=username, email=email,
                                   upcoming_lessons=upcoming_lessons,
                                   previous_lessons=previous_lessons,
                                   len_upcoming=len_upcoming,
                                   len_previous=len_previous, admin=is_admin,
                                   view_all_upcoming=True)

        elif request.form.get("view_prev") is not None:
            return render_template("profile.html", name=username, email=email,
                                   upcoming_lessons=upcoming_lessons,
                                   previous_lessons=previous_lessons,
                                   len_upcoming=len_upcoming,
                                   len_previous=len_previous, admin=is_admin,
                                   view_all_previous=True)

        return redirect(redir_url)

    return render_template("profile.html", name=username, email=email,
                           upcoming_lessons=upcoming_lessons,
                           previous_lessons=previous_lessons,
                           len_upcoming=len_upcoming,
                           len_previous=len_previous, admin=is_admin)


@app.route('/students', methods=["GET"])
@login_required
def student_list():
    """Render the student list page"""

    # Check if admin
    if not admin_check():
        return redirect("/calendar")

    # Retrieve list of students from the database
    students = db_query(db,
                        "SELECT username, email FROM users "
                        "WHERE NOT username = 'admin' ORDER BY username ASC")
    n_students = len(students)

    return render_template("students.html", students=students,
                           n_students=n_students)
