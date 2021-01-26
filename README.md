# Springboard-Section-29-Capstone-Project-1  
API used:  
https://www.api-football.com/  
Accessed via the platform:  
https://rapidapi.com/marketplace

**What does this app do?**  
It is, I hope, a fun and interesting app. It obtains data on the English Premiership (football/soccer) from the API shown above and displays it in html format. The user is requried to create a login to explore the app. The features consist of:  
* A list of upcoming games  
* The most recent games and results  
* Live games and current scores  
* The Premiership League table
* User end-of-season predictions for the top four and bottom three teams and managerial dismissals 
* The user can select their favourite team at the point of signup and see a summary of performance and next few games as the home screen upon login

The app provides key information with regard to games and performance. It provides a useful and testing exercise in web site design and full-stack development. There is scope to build on this and provide a far richer presentation and involved user participation such as a comments functionality.  

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
