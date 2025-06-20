import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import json
import os
import csv

# Load JSON data
with open("2020s_wpa_analysis.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Convert to list of dicts for sorting
data = []
for team_name, team_info in raw_data.items():
    data.append({
        "team": team_name,
        "team_id": team_info["team_id"],
        "games_played": team_info["games_played"],
        "total_wpa": team_info["total_wpa"],
        "avg_wpa": team_info["average_wpa_per_game"]
    })

# Sort data by average WPA
data.sort(key=lambda x: x["avg_wpa"])

# Extract sorted teams, WPAs, and team IDs
teams = [team["team"] for team in data]
avg_wpa = [team["avg_wpa"] for team in data]
team_ids = [team["team_id"] for team in data]

# Plot bar chart
fig, ax = plt.subplots(figsize=(10, 10))
bars = ax.barh(teams, avg_wpa, color='skyblue')

# Function to load and return the logo as an image object
def get_logo_image(team_id):
    path = f"Logos/{team_id}.png"
    if os.path.exists(path):
        img = mpimg.imread(path)
        return OffsetImage(img, zoom=0.01, interpolation='hanning')  # Adjust zoom as needed
    return None

# Add each logo to the corresponding bar
for bar, team_id in zip(bars, team_ids):
    x = bar.get_width() - (max(avg_wpa) * 0.001)
    y = bar.get_y() + bar.get_height() / 2
    imagebox = get_logo_image(team_id)
    if imagebox:
        ab = AnnotationBbox(imagebox, (x, y), frameon=False, box_alignment=(1, 0.5))
        ax.add_artist(ab)

# Final plot adjustments
plt.xlabel("Average win percentage change per game")
plt.ylabel("Teams")
plt.title("Average win percentage change per game (most \"chaotic\" games) by team in the 2020s")
plt.xlim(min(avg_wpa) * 0.99, max(avg_wpa) * 1.01)
plt.tight_layout()
plt.savefig('2020s_wpa_analysis.png', dpi=300)
plt.show()

# Output to terminal
print("\nAverage WPA per game by team (sorted):")
print("{:<25} {:>10} {:>15} {:>15}".format("Team", "Games", "Total WPA", "Avg WPA/Game"))
for team in data:
    print("{:<25} {:>10} {:>15.5f} {:>15.5f}".format(
        team["team"], team["games_played"], team["total_wpa"], team["avg_wpa"]
    ))

# Save to CSV
with open("2020s_wpa_analysis.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Team", "Team ID", "Games Played", "Total WPA", "Average WPA per Game"])
    for team in data:
        writer.writerow([
            team["team"], team["team_id"], team["games_played"],
            round(team["total_wpa"], 5), round(team["avg_wpa"], 5)
        ])

print("\nWPA data saved to 2020s_wpa_analysis.csv")
