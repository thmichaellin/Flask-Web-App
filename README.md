# Project Title:<br> Meacham Lesson Management App
## Name: Michael Lin
# Screenshots:<br>
<img src="C:\Users\thmic\OneDrive\Documents\GitHub\project-thmichaellin\static\images\Screenshot1.png" width="250"/>
<img src="C:\Users\thmic\OneDrive\Documents\GitHub\project-thmichaellin\static\images\Screenshot2.png" width="250"/><br>
<img src="C:\Users\thmic\OneDrive\Documents\GitHub\project-thmichaellin\static\images\Screenshot3.png" width="250"/>
<img src="C:\Users\thmic\OneDrive\Documents\GitHub\project-thmichaellin\static\images\Screenshot4.png" width="250"/>

# Description:
This project is a Flask application that allows users to view a
calendar, book lessons through Google Calendar API integration
and view a profile of past and future lessons. 
It also allows admins the ability to confirm and cancel
lessons as well as view the profile of all users.

The application solves the problem of scheduling and managing
lessons across multiple platforms by using Google Calendar as
a hub. Events that are inserted into Google Calendar, regardless
of origin will be retrieved and populate the calendar.

The intended users for this application is the owner of Meacham
and her students.

# Prerequisites:
### Install required modules
`pip install -r requirements.txt`
### Start postgres psql
`sudo service postgresql start`
### Create calendar db
`sudo -u postgres psql`
`\c`
'CREATE DATABASE calendar;'
### Set up db
`python3 create.py`
### Run Flask app
`bash start_script.sh` or `bash start_script_debug.sh`

# Data Sources and Dependencies:
[FullCalendar](https://fullcalendar.io/): Used for rendering the calendar in the application<br>
[Google Calendar API](https://developers.google.com/calendar/api): Used for retrieving and updating user calendar data<br>
[Flask](https://flask.palletsprojects.com/en/): A web framework for developing the application<br>
[Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/): An extension of Flask for database integration <br>
[Werkzeug](https://werkzeug.palletsprojects.com/en/): Used to generate password hash <br>
[Bootstrap](https://getbootstrap.com/): Used for front-end design of application.

Other dependencies are listed in the 'requirements.txt' file.<br>
The background image used in this project is sourced from [freepik.com](https://www.freepik.com/free-vector/green-nebula_13216451.htm#query=green%20background&position=2&from_view=keyword&track=ais) and is <br>
licensed under a Free license which allows for free use, 2023. 


