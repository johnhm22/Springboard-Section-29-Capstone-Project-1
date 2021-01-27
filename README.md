# Springboard-Section-29-Capstone-Project-1  

**What does this app do?**  
It is, I hope, a fun and interesting app. It obtains data on the English Premiership (football/soccer) from an API and displays it in html format. The user is requried to create a login to explore the app. The features consist of:  
* A list of upcoming games  
* The most recent games and results  
* Live games and current scores  
* The Premiership League table
* User end-of-season predictions for the top four and bottom three teams and managerial dismissals 
* The user can select their favourite team at the point of signup and see a summary of performance and next few games as the home screen upon login

The app provides key information with regard to games and performance. It provides a useful and testing exercise in web site design and full-stack development. There is scope to build on this and provide a far richer presentation and involved user participation such as a comments functionality.  

**API used**  
The API used is: https://www.api-football.com/  It is a freemium model. Thus there is a charge for a number of calls above a defined threshold.  
The API has been accessed via the platform:  https://rapidapi.com/marketplace

**Website design**  
Access to all website pages is via a navbar. The menus across the top left are the portals to the functionality described above. The menus on the right are for signup, login/logout. Once logged in the username is displayed, clicking it will present a brief summary of the user's profile. It is a simple, intuitive layout.  

**Technology**  
The stack runs from HTML for the front end through to Python and a PostgreSQL database at the backend.  
Flask-SQLAlchemy is deployed as a web framework; it "glues" everything together by connecting the URL routes to the code in the app.py file and the backend database. Along with Jinja, it enables customised HTML pages.  
A small javascript file using jQuery has also been used in order to manipulate match dates provided by the API into a more user-friendly format.  

Bootstrap 4 has been used to design the HTML pages and unsplash.com and fontawseome.com for photos and icons, where not provided by the API.

**API and database**  
As recommended by the API authors, some of the less dynamic data has been stored in the backend database. The database will be accessed by the app rather than making unnecessary direct API calls for information which does not change frequently. An example is the table for team name and team id or the table containing league name, league id and season.  

Some of the data can change frequently and users will be looking for regular updates; this is the case with live games. However, conscious of the freeium nature of the API, a function decorator called ratelimit has been added to a number of the routes to restrict the API calls to a defined maximum during a set period of time.  

The choice between a direct API call or to the database is less clear for some of the data. This is the case with the league table. Sometimes this doesn't change for a period of days, but when games are reaching fulltime, users will want to see the most up-to-date version of the league table. As a compromise, the function which calls the API for this league table and populates the database is called each time the app is used. Thus everytime the user opens the app, the database is updated with the latest league data.

For the "static" data mentioned earlier, no automated update of the database has been set up.  


**Testing**  
Four testing scripts have been written.  
* test_app.py
* test_models.py
* test_user_models.py
* test_populate_scripts.py  

The Python built-in unit testing framework unittest is used to test the application. It is part of the standard Python library and so doesn't need to be downloaded or installed. TestCase is a base class containing testing methods. It is imported from unittest and is used to test the response of a defined test to a series of inputs.  

One or more test classes are created in each test file. These test classes inherit from TestCase which provides them with access to the testing methods of TestCase such as assert methods.

The tests are structured with setUp and tearDown functions which are run before and after each test respectively. The setUp function will ensure a clean database and enter test data prior to the test. The tearDown function will remove the data at the end of the test.  

test_user_models.py is aimed at testing signup and authentication
test_models.py checks that data can be correctly entered into the database tables
test_app.py is more extensive and tests the routes defined in app.py
test_populate_scripts.py is not in itself a test file, but is populates the test database by using the API and is called by test_app.py when first exectuted  



