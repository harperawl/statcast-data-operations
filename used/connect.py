import os
import json

player_id = 519184

files = ["2010/" + file for file in os.listdir("B:/MLB/2010")] + ["2011/" + file for file in os.listdir("B:/MLB/2011")] + ["2012/" + file for file in os.listdir("B:/MLB/2012")] + ["2013/" + file for file in os.listdir("B:/MLB/2013")]

for file in files:
    with open(f"B:/MLB/{file}", "r", encoding="utf-8") as f:
        game = json.loads(f.read())
        if f"ID{player_id}" in game["boxscore"]["teams"]["away"]["players"]:
            team = "away"
        elif f"ID{player_id}" in game["boxscore"]["teams"]["home"]["players"]:
            team = "home"
        else:
            continue
        if game["boxscore"]["teams"][team]["players"][f"ID{player_id}"]["position"]["abbreviation"] == "CF":
            for at_bat in (game["team_home"] + game["team_away"]):
                if at_bat["balls"] == 3 and at_bat["strikes"] == 1 and at_bat["result"] == "Home Run" and at_bat["call"] == "X" and at_bat["team_fielding"] == game["scoreboard"]["teams"][team]["abbreviation"]:
                    if "center field" in at_bat["des"]:
                        print(f"Found 3-1 CF homer with Revere in the outfield in {file} with at bat number {at_bat['ab_number']}!")
                        if at_bat["team_batting"] == "TOR":
                            print("This was a Blue Jays game!")
                