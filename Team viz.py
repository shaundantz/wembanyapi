import sqlite3
import matplotlib.pyplot as plt

def fetch_team_data():
    conn = sqlite3.connect("nba.db")
    cursor = conn.cursor()

    cursor.execute("SELECT WINS, FG_PCT, PTS, BLK, STL, FG3_PCT, NAME FROM Teams")
    team_data = cursor.fetchall()

    conn.close()

    return team_data

def calculate_team_composite_metric(wins, fg_pct, pts, blk, stl, fg3_pct):
    weights = {'WINS': 0.4, 'FG_PCT': 0.05, 'PTS': 0.25, 'BLK': 0.1, 'STL': 0.05, 'FG3_PCT': 0.15}
    
    composite_metric = wins * weights['WINS'] + fg_pct * weights['FG_PCT'] + pts * weights['PTS'] + blk * weights['BLK'] + stl * weights['STL'] + fg3_pct * weights['FG3_PCT']
    
    return composite_metric

def plot_scatter(team_data):
    wins = [row[0] for row in team_data]
    fg_pct = [row[1] for row in team_data]
    pts = [row[2] for row in team_data]
    blk = [row[3] for row in team_data]
    stl = [row[4] for row in team_data]
    fg3_pct = [row[5] for row in team_data]
    team_names = [row[6] for row in team_data]

    composite_metrics = [calculate_team_composite_metric(w, fg, p, b, s, f3) for w, fg, p, b, s, f3 in zip(wins, fg_pct, pts, blk, stl, fg3_pct)]

    sorted_teams = sorted(zip(team_names, composite_metrics, wins), key=lambda x: x[1])

    # Extract top 5 and bottom 5 teams
    top_5_teams = sorted_teams[-5:]
    bottom_5_teams = sorted_teams[:5]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(composite_metrics, wins, marker='o', color='b')
    
    for team in top_5_teams:
        plt.annotate(team[0], (team[1], team[2]), textcoords="offset points", xytext=(0, 5), ha='center', rotation=0)

    for team in bottom_5_teams:
        plt.annotate(team[0], (team[1], team[2]), textcoords="offset points", xytext=(0, 5), ha='center', rotation=45)

    plt.title('NBA Team Composite Metric vs. Wins (2022-23 Season)')
    plt.xlabel('Team Composite Metric')
    plt.ylabel('Wins')
    plt.tight_layout()

    plt.show()

def main():
    team_data = fetch_team_data()
    plot_scatter(team_data)

if __name__ == "__main__":
    main()
