import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def calculate_composite_metric(ppg, games_played, field_goal_percentage, nba_fantasy_points, rebounding, assists, blocks, steals, pfd):
    # Define weights
    weights = {
        'ppg': 0.35,
        'field_goal_percentage': 0.05,
        'nba_fantasy_points': 0.20,
        'games_played': 0.15,
        'rebounding': 0.05,
        'assists': 0.05,
        'blocks': 0.05,
        'steals': 0.05,
        'pfd': 0.05,
    }

    # Calculate composite metric
    composite_metric = (
        weights['ppg'] * ppg +
        weights['field_goal_percentage'] * field_goal_percentage +
        weights['nba_fantasy_points'] * nba_fantasy_points +
        weights['games_played'] * games_played +
        weights['rebounding'] * rebounding +
        weights['assists'] * assists +
        weights['blocks'] * blocks +
        weights['steals'] * steals +
        weights['pfd'] * pfd
    )
    return composite_metric

def fetch_player_data_from_database():
    conn = sqlite3.connect('nba.db')  
    cursor = conn.cursor()

    query = """
        SELECT NAME, FG_PCT, PTS, PFD, GP, REB, AST, STL, BLK, NBA_FANTASY_PTS
        FROM Players;
    """
    cursor.execute(query)

    player_data = cursor.fetchall()

    conn.close()

    return player_data

def main():
    player_data = fetch_player_data_from_database()

    # Calculate the composite metric for each player and store in a list
    composite_metrics = []
    pts_values = []

    for player_stats in player_data:
        player_name, fg_pct, pts, pfd, gp, reb, ast, stl, blk, nba_fantasy_pts = player_stats

        # Calculate the composite metric for each player
        composite_metric = calculate_composite_metric(pts, gp, fg_pct, nba_fantasy_pts, reb, ast, blk, stl, pfd)
        composite_metrics.append(composite_metric)
        pts_values.append(pts)

    # Create bins for PTS values (inclusive at 0.0)
    max_pts = max(pts_values)
    bins = np.arange(0, max_pts + 6, 5)  # Start from 0 to include 0.0

    # If max_pts is a multiple of 5, add an extra bin for "max_pts+"
    if max_pts % 5 == 0:
        bins = np.append(bins, max_pts + 1)

    # Assign each player to a bin
    bin_indices = np.digitize(pts_values, bins, right=True)

    # Create a scatter plot with colored points for each bin
    plt.figure(figsize=(12, 8))
    for bin_index in np.unique(bin_indices):
        indices = np.where(bin_indices == bin_index)
        plt.scatter(
            [composite_metrics[i] for i in indices[0]],
            [pts_values[i] for i in indices[0]],
            label=f'PTS {bins[bin_index - 1]}-{bins[bin_index]}', alpha=0.7
        )

    z = np.polyfit(composite_metrics, pts_values, 1)
    p = np.poly1d(z)
    slope = z[0]
    plt.plot(composite_metrics, p(composite_metrics), "k--", label=f'Trendline (Slope: {slope:.2f})')

    plt.xlabel('Composite Metric')
    plt.ylabel('Points per game')
    plt.title('Players: Composite Metric vs Points per game (PPG)')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
