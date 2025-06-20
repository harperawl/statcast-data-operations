import requests
import os

DESTINATION = "B:/MLB/2023"
SPORT_ID = 1
STARTING_DATE = "2023-01-01"
ENDING_DATE = "2023-12-31"

schedule_request = requests.get(f"https://statsapi.mlb.com/api/v1/schedule?sportId={SPORT_ID}&startDate={STARTING_DATE}&endDate={ENDING_DATE}&gameType=R&fields=dates,date,games,gamePk")
schedule_json = schedule_request.json()

gamePks = []

for date in schedule_json["dates"]:
    for gamePk in date["games"]:
        gamePks.append(gamePk["gamePk"])

print(f"Downloading games from {STARTING_DATE} to {ENDING_DATE}...")

while True:
    if input(f"This contains {len(gamePks)} games. Are you sure you want to continue? (y/n) ") == 'y':
        break

for gamePk in gamePks:
    if os.path.exists(f"{DESTINATION}/game_{gamePk}.json"):
        print(f"Game {gamePk} already exists, skipping download.")
        continue
    game_request = requests.get(f"https://baseballsavant.mlb.com/gf?game_pk={gamePk}")
    with open(f"{DESTINATION}/game_{gamePk}.json", "w+", encoding="utf-8") as file:
        file.write(game_request.text)
        print(f"Downloaded game {gamePk}.")
        file.close() 

print(f"Downloaded {len(gamePks)} games from {STARTING_DATE} to {ENDING_DATE}.")