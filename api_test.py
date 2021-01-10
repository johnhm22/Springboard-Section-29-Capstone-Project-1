from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# teams from league id
# url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2"

# url = "https://api-football-v1.p.rapidapi.com/leagues"

# url = "https://api-football-v1.p.rapidapi.com/leagues/season/2020"

# url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/524/last/10"

# headers = {
#     'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
#     'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers)

# print(response.text)




# url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/33/last/10"
# querystring = {"timezone":"Europe/London"}
# headers = {
#     'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
#     'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#     }
# response = requests.request("GET", url, headers=headers, params=querystring)


# last fixtures from league id
# url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/last/10"
# querystring = {"timezone":"Europe/London"}
# headers = {
#     'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
#     'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#     }
# response = requests.request("GET", url, headers=headers, params=querystring)



#seasons available
# url = "https://api-football-v1.p.rapidapi.com/v2/seasons"
# headers = {
#     'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
#     'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#     }
# response = requests.request("GET", url, headers=headers)


#last fixtures from team id
#this works. Team is MU
# url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/33/last/10"
# querystring = {"timezone":"Europe/London"}
# headers = {
#     'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
#     'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#     }
# response = requests.request("GET", url, headers=headers, params=querystring)


# search for a league in relation to a league {name}
# get("https://api-football-v1.p.rapidapi.com/v2/leagues/search/{name}");
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/search/premier_league"

# or search by country
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/search/{country}"
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/search/england"


# Get all leagues in which the {team_id} has played at least one match
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/team/{team_id}"

# active leagues in a defined season
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/season/2020"


# Allows you to search for a team in relation to a team {name} or {country}
# Spaces must be replaced by underscore for better search performance.
# EX : Real madrid => real_madrid
# url = "https://api-football-v1.p.rapidapi.com/v2/teams/search/arsenal"


# teams in england
# url = "https://api-football-v1.p.rapidapi.com/v2/teams/search/england"


# Get all leagues in which the {team_id} has played at least one match
# url = "https://api-football-v1.p.rapidapi.com/v2/leagues/team/42"


# Get all statistics for a {team_id} in a {league_id}
# url = "https://api-football-v1.p.rapidapi.com/v2/statistics/2790/42"


# Get coachs from one {team_id}
# url = "https://api-football-v1.p.rapidapi.com/v2/coachs/team/42"

# live fixture events
# url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/live"

# table standings
url = "https://api-football-v1.p.rapidapi.com/v2/leagueTable/2790"


# get teams by league id (2790 = EPL 2020 season)
# url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/2790"

headers = {
    'x-rapidapi-key': "9332caaa7amsh4b569f1db833877p1e024cjsnef540fa8e9e5",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
response = requests.request("GET", url, headers=headers)

