import matplotlib.pyplot as plt
import pandas as pd
import requests
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_TOKEN')
url1 = "https://api.football-data.org/v2/competitions/PL/matches?season=2021"
url2 = "https://api.football-data.org/v2/competitions/PL/teams?season=2021"
headers = {"X-Auth-Token": api_key}

response1 = requests.get(url1, headers=headers)
response2 = requests.get(url2, headers=headers)

data1 = json.loads(response1.text)
data2 = json.loads(response2.text)

matches = pd.DataFrame(data1["matches"])
teams = pd.DataFrame(data2["teams"])

# Get initial points and rankings for each team
points = pd.DataFrame({
    "team_id": teams["id"],
    "team_name": teams["name"],
    "points": 0,
    "position": 0
})


with open("./data/21-22PL_RankAftermatch.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    
    writer.writerow(["ID", "Position", "Team Name", "Points"])
    
# Calculate points and rankings for each match
    for _, match in matches.iterrows():
        home_team_id = match["homeTeam"]["id"]
        away_team_id = match["awayTeam"]["id"]
        home_team_name = match["homeTeam"]["name"]
        away_team_name = match["awayTeam"]["name"]
        home_score = match["score"]["fullTime"]["homeTeam"]
        away_score = match["score"]["fullTime"]["awayTeam"]
        
        home_score = home_score if home_score is not None else 0
        away_score = away_score if away_score is not None else 0
        
        # Calculate points
        if int(home_score) > int(away_score):
            points.loc[points["team_id"] == home_team_id, "points"] += 3
        elif home_score < away_score:
            points.loc[points["team_id"] == away_team_id, "points"] += 3
        else:
            points.loc[points["team_id"] == home_team_id, "points"] += 1
            points.loc[points["team_id"] == away_team_id, "points"] += 1

        # Calculate rankings
        points = points.sort_values(
            by=["points", "team_id"], ascending=[False, True])
        points["position"] = points["points"].rank(method="dense", ascending=False)

        writer.writerow("")
        writer.writerow([f"{home_team_name} {home_score} - {away_score} {away_team_name}"])
        writer.writerow([points[["position", "team_id", "team_name", "points"]]])
        
