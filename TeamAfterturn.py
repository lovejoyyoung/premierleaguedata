import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_TOKEN')
url = "https://api.football-data.org/v2/competitions/PL/matches?season=2021"
headers = {"X-Auth-Token": api_key}

response = requests.get(url, headers=headers)
data = response.json()

team_points = {}
team_games_played = {}

tot_fc_points = 0
tot_fc_rank = 0

# Save the data list
data_list = []

for match in data["matches"]:
    # Get match data
    home_team = match["homeTeam"]["name"]
    away_team = match["awayTeam"]["name"]
    home_score = match["score"]["fullTime"]["homeTeam"]
    away_score = match["score"]["fullTime"]["awayTeam"]

    home_score = home_score if home_score is not None else 0
    away_score = away_score if away_score is not None else 0

    # Calculate Scores
    if home_score > away_score:
        home_points = 3
        away_points = 0
    elif home_score == away_score:
        home_points = 1
        away_points = 1
    else:
        home_points = 0
        away_points = 3

    # Calculate Home/Away team points and game played
    if home_team not in team_points:
        team_points[home_team] = 0
        team_games_played[home_team] = 0
    if away_team not in team_points:
        team_points[away_team] = 0
        team_games_played[away_team] = 0

    team_points[home_team] += home_points
    team_points[away_team] += away_points
    team_games_played[home_team] += 1
    team_games_played[away_team] += 1

    # if fav team finished match then update data
    if "Tottenham Hotspur FC" in [home_team, away_team]:
        tot_fc_points = team_points["Tottenham Hotspur FC"]
        tot_fc_rank = sorted(team_points.items(), key=lambda x: x[1], reverse=True).index(
            ("Tottenham Hotspur FC", tot_fc_points)) + 1

    # add data into list
    data_list.append([match['matchday'], tot_fc_rank, tot_fc_points])

# Write data into csv files
with open('./data/ToT_FC_RankAfterturn.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Round', 'Rank', 'Points'])
    for row in data_list:
        writer.writerow(row)
