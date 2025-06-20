import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import json
import os

# Load JSON data
with open("2020s_wpa_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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
    x = bar.get_width() - (max(avg_wpa) * 0.001)  # position inside the bar
    y = bar.get_y() + bar.get_height() / 2
    imagebox = get_logo_image(team_id)
    if imagebox:
        ab = AnnotationBbox(imagebox, (x, y), frameon=False, box_alignment=(1, 0.5))
        ax.add_artist(ab)

# Final plot adjustments
plt.xlabel("Average win percentage change per game")
plt.ylabel("Teams")
plt.title("Average win percentage change per game (most \"chaotic\" games) by team in the 2020s")
plt.xlim(min(avg_wpa) * 0.95, max(avg_wpa) * 1.01)  # Add space for clarity
plt.tight_layout()
plt.savefig('2020s_wpa_analysis.png', dpi=300)  # Save the figure
plt.show()
