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

    query = """
        SELECT Players.NAME, Players.FG_PCT, Players.PTS, Players.PFD, Players.GP, Players.REB, Players.AST, Players.STL, Players.BLK, Players.NBA_FANTASY_PTS, Salaries.salary
        FROM Players JOIN Salaries ON Players.PLAYER_ID = Salaries.player_id;
    """
    cursor.execute(query)

    player_data = cursor.fetchall()

    conn.close()

    return player_data

def main():
    player_data = fetch_player_data_from_database()

    composite_metrics = []
    salaries = []
    player_names = []

    for player_stats in player_data:
        player_name, fg_pct, pts, pfd, gp, reb, ast, stl, blk, nba_fantasy_pts, salary = player_stats

        composite_metric = calculate_composite_metric(pts, gp, fg_pct, nba_fantasy_pts, reb, ast, blk, stl, pfd)
        composite_metrics.append(composite_metric)
        
        salary_in_millions = salary / 1000000.0
        salaries.append(salary_in_millions)
        player_names.append(player_name)

    sorted_players = sorted(zip(player_names, composite_metrics, salaries), key=lambda x: x[1], reverse=True)
    
    # Extract the top 10 players and their details
    top_10_players = sorted_players[:10]
    top_10_names, top_10_metrics, top_10_salaries = zip(*top_10_players)

    # Create a scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(composite_metrics, salaries, color='orange', alpha=0.7)

    for i, name in enumerate(top_10_names):
        rotation_angle = 45 if name == 'Giannis Antetokounmpo' or name == 'Damian Lillard' else 0
        plt.text(top_10_metrics[i], top_10_salaries[i], name, fontsize=8, ha='right', va='bottom', rotation=rotation_angle)

    plt.xlabel('Composite Metric')
    plt.ylabel('Salary (Millions)')
    plt.title('Players: Composite Metric vs Salary')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
