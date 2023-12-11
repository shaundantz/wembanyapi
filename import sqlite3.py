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

import sqlite3
import matplotlib.pyplot as plt

def fetch_player_data_from_database():
    conn = sqlite3.connect('nba.db')  # Replace with your database name
    cursor = conn.cursor()
    """
        ALTER TABLE Players
        ADD COLUMN SALARY FLOAT;

        UPDATE Players
        SET Players.SALARY = Salaries.SALARY
        FROM Salaries
        WHERE Players.PLAYER_ID = Salaries.PLAYER_ID;
    """

    # Execute a query to fetch player data from the Players table, including salary
    query = """
        SELECT p.NAME, p.FG_PCT, p.PTS, p.PFD, p.GP, p.REB, p.AST, p.STL, p.BLK, p.NBA_FANTASY_PTS, s.SALARY
        FROM Players p
        INNER JOIN Salaries s ON p.PLAYER_ID = s.PLAYER_ID;
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
    salaries = []
    for player_stats in player_data:
        player_name, fg_pct, pts, pfd, gp, reb, ast, stl, blk, nba_fantasy_pts, salary = player_stats

        # Calculate the composite metric for each player
    composite_metric = calculate_composite_metric(
        pts, gp, fg_pct, nba_fantasy_pts, reb, ast, blk, stl, pfd
    )
    composite_metrics.append(composite_metric)
    salaries.append(salary)

    # Create a scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(salaries, composite_metrics, color='green', alpha=0.7)
    plt.xlabel('Salary')
    plt.ylabel('Composite Metric')
    plt.title('Players: Salary vs Composite Metric')
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
