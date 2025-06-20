import os
import json

files = os.listdir("B:/MLB/2025")
highestWPA = 0
lowestWPA = 100
for file in files:
    with open(f"B:/MLB/2025/{file}", "r", encoding="utf-8") as f:
        content = f.read()
        game = json.loads(content)
        WPA = 0
        for at_bat in game["scoreboard"]["stats"]["wpa"]["gameWpa"]:
            WPA += abs(at_bat["homeTeamWinProbabilityAdded"])

        if WPA > highestWPA:
            highestWPA = WPA
            print(f"Highest WPA found on {game['gameDate']} between {game['scoreboard']['teams']['away']['name']} and {game['scoreboard']['teams']['home']['name']}: {highestWPA:.2f}")
        if WPA < lowestWPA and WPA > 0:
            lowestWPA = WPA
            print(f"Lowest WPA found on {game['gameDate']} between {game['scoreboard']['teams']['away']['name']} and {game['scoreboard']['teams']['home']['name']}: {lowestWPA:.2f}")