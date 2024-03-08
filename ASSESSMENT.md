# Key Points:
* Google Calendar Integration: A lot of effort was put into the
smooth functioning of the calendar. Google Calendar's API was 
completely different from anything that we practiced with in 
the Book assignment as it includes additional work in setting up
a Google cloud console and handling authentication and permissions.
I'm very happy that I managed to get the application to smoothly 
interact with the API in retrieving, inserting and deleting events.
* Lesson Confirmations: I'm very happy with the way I decided to
handle pending and confirmed classes. I managed this by abstracting
an existing feature of Google Calendar; namely color ID to represent
whether a lesson was confirmed or not. By making changes, to the 
color of the event, it gave me a way to differentiate between
events.
* Datetime Formatting: Formatting datetime is a nightmare. I had
to handle different formats of datetime across Python, FullCalendar,
and Google Calendar. I managed to ensure that the datetime data being
passed around stay in/get converted to the correct format seamlessly.

# Major Decisions:
1. Database Schema: I decided on using PostgreSQL as bridge between Google Calendar
and the application because it allowed me to keep the data pulled
from the API is a structured way such that I could consistently 
make queries from the application. It also allowed me to make 
multiple queries from one API call without having to keep making 
API calls for each individual query.
2. Google Calendar Integration: My first consideration for deciding
on using Google Calendar as the backend of the calendar app 
was that many online teaching platforms have existing abilities to 
sync with Google Calendar. This meant that when it comes to keeping
lessons across multiple platforms synced, it is much simpler. My
second consideration is that I am already familiar with Google
Calendar so i believed that learning to use its API would be a bit
most straightforward.
3. E-mail System. Originally I had planned on integrating an e-mail
notification system. I was suprised to discover during the testing
of the application that Google Calendar automatically sent out e-mail
notifications so I did not have to design a system to do so myself.
If this was not the case, I would have used Gmail API to send structured
messages based on information from the database. 
4. Formatting Changes. When I originally designed the layout of the
application, I had desktop usage in mind as that is what I normally
use. In the making of the application, I tried to view the application
in mobile view and the results were not satisfactory. I therefore
adjusted the layout to be more mobile friendly; mostly by making sure 
elements stacked properly and using a more vertical layout.