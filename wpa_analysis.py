import os
import json

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

results = []

for team, team_id in teams.items():
    print(f"Analyzing {team} ({team_id})...")

    running_total = 0
    num_games = 0
    files = ["2020/" + file for file in os.listdir("B:/MLB/2020")] + ["2021/" + file for file in os.listdir("B:/MLB/2021")] + ["2022/" + file for file in os.listdir("B:/MLB/2022")] + ["2023/" + file for file in os.listdir("B:/MLB/2023")] + ["2024/" + file for file in os.listdir("B:/MLB/2024")] + ["2025/" + file for file in os.listdir("B:/MLB/2025")]

    for file in files:
        with open(f"{DESTINATION}/{file}", "r", encoding="utf-8") as f:
            game = json.loads(f.read())
            game_total = 0
            if game["scoreboard"]["teams"]["home"]["id"] == team_id or game["scoreboard"]["teams"]["away"]["id"] == team_id:
                for at_bat in game["scoreboard"]["stats"]["wpa"]["gameWpa"]:
                    game_total += abs(at_bat["homeTeamWinProbabilityAdded"])
            if game_total > 0:
                running_total += game_total
                num_games += 1
                print(f"Processed {game['gameDate']}: {game_total:.2f} WPA")

    print(f"Average WPA for {team}: {running_total / num_games:.2f}")
    results.append({
        "team": team,
        "team_id": team_id,
        "avg_wpa": running_total / num_games
    })

with open(f"2020s_wpa_analysis.json", "w+", encoding="utf-8") as file:
    json.dump(results, file, indent=4)
    print("WPA analysis saved to 2020s_wpa_analysis.json")
