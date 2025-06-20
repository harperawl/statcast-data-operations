import os
import json
from collections import defaultdict

DESTINATION = "B:/MLB"
SPORT_ID = 1

teams = {
    "Los Angeles Angels": 108,
    "Arizona Diamondbacks": 109,
    "Baltimore Orioles": 110,
    "Boston Red Sox": 111,
    "Chicago Cubs": 112,
    "Cincinnati Reds": 113,
    "Cleveland Guardians": 114,
    "Colorado Rockies": 115,
    "Detroit Tigers": 116,
    "Houston Astros": 117,
    "Kansas City Royals": 118,
    "Los Angeles Dodgers": 119,
    "Washington Nationals": 120,
    "New York Mets": 121,
    "Oakland Athletics": 133,
    "Pittsburgh Pirates": 134,
    "San Diego Padres": 135,
    "Seattle Mariners": 136,
    "San Francisco Giants": 137,
    "St. Louis Cardinals": 138,
    "Tampa Bay Rays": 139,
    "Texas Rangers": 140,
    "Toronto Blue Jays": 141,
    "Minnesota Twins": 142,
    "Philadelphia Phillies": 143,
    "Atlanta Braves": 144,
    "Chicago White Sox": 145,
    "Miami Marlins": 146,
    "New York Yankees": 147,
    "Milwaukee Brewers": 158,
}

# Create reverse mapping: team_id -> team_name
team_ids = {v: k for k, v in teams.items()}

# Track WPA and games played
team_wpa = defaultdict(float)
team_games = defaultdict(int)

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
files = []
for year in years:
    path = os.path.join(DESTINATION, year)
    if os.path.exists(path):
        files += [f"{year}/{file}" for file in os.listdir(path) if file.endswith(".json")]

for file in files:
    with open(f"{DESTINATION}/{file}", "r", encoding="utf-8") as f:
        try:
            game = json.load(f)
            game_total = 0
            for at_bat in game["scoreboard"]["stats"]["wpa"]["gameWpa"]:
                game_total += abs(at_bat["homeTeamWinProbabilityAdded"])
            if game_total > 0:
                home_id = game["scoreboard"]["teams"]["home"]["id"]
                away_id = game["scoreboard"]["teams"]["away"]["id"]
                team_wpa[home_id] += game_total
                team_wpa[away_id] += game_total
                team_games[home_id] += 1
                team_games[away_id] += 1
        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Compute average WPA per game
results = {}
for team_id in team_wpa:
    team_name = team_ids.get(team_id, f"Unknown ({team_id})")
    games = team_games[team_id]
    avg_wpa = team_wpa[team_id] / games if games > 0 else 0
    results[team_name] = {
        "team_id": team_id,
        "games_played": games,
        "total_wpa": round(team_wpa[team_id], 5),
        "average_wpa_per_game": round(avg_wpa, 5)
    }

with open("2020s_wpa_analysis.json", "w+", encoding="utf-8") as out_file:
    json.dump(results, out_file, indent=4)
    print("WPA analysis saved to 2020s_wpa_analysis.json")