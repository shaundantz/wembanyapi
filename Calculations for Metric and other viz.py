import sqlite3
import matplotlib.pyplot as plt

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

    # Execute a query to fetch player data from the Players table
    query = """
        SELECT Players.NAME, Players.FG_PCT, Players.PTS, Players.PFD, Players.GP, Players.REB, Players.AST, Players.STL, Players.BLK, Players.NBA_FANTASY_PTS, Salaries.salary
        FROM Players JOIN Salaries ON Players.PLAYER_ID = Salaries.player_id;
    """
    cursor.execute(query)

    # Fetch the data
    player_data = cursor.fetchall()

    # Close the database connection 
    conn.close()

    return player_data

def main():
    player_data = fetch_player_data_from_database()

    # Calculate the composite metric for each player and store in a list
    composite_metrics = []
    for player_stats in player_data:
        player_name, fg_pct, pts, pfd, gp, reb, ast, stl, blk, nba_fantasy_pts, salary = player_stats

        # Calculate the composite metric for each player
        composite_metric = calculate_composite_metric(pts, gp, fg_pct, nba_fantasy_pts, reb, ast, blk, stl, pfd)
        composite_metrics.append((player_name, composite_metric, salary))

    composite_metrics.sort(key=lambda x: x[1], reverse=True)

    # Extract the top 50 players and their composite metrics for plotting
    top_50_players = composite_metrics[:50]
    player_names, composite_metrics_values, salaries = zip(*top_50_players)

    # Create a bar graph
    plt.figure(figsize=(12, 8))
    plt.barh(player_names, composite_metrics_values, color='blue')
    plt.xlabel('Composite Metric')
    plt.ylabel('Player Name')
    plt.title('Top 50 Players by Composite Metric')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
