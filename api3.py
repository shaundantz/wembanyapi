from bs4 import BeautifulSoup
import requests
import json
from nba_api.stats.endpoints import leaguedashplayerstats
import os
import sqlite3


def get_player_data():
    advanced_stats = json.loads(
        leaguedashplayerstats.LeagueDashPlayerStats(
            per_mode_detailed="PerGame", season="2022-23"
        ).get_json()
    )
    player_data = advanced_stats["resultSets"][0]["rowSet"]
    headers = advanced_stats["resultSets"][0]["headers"]
    return headers, player_data


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def create_salary_table(cur, conn, headers, player_data):
    params = [(index + " FLOAT, ") for index in headers[5:]]
    params[len(params) - 1] = params[len(params) - 1].replace(", ", "")
    query = f"CREATE TABLE IF NOT EXISTS Players (PLAYER_ID INTEGER PRIMARY KEY, NAME TEXT, TEAM_ID INTEGER, {''.join(params)})"
    cur.execute(query)
    count = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Players").fetchone()[0]
    for i in range(count, count + 25):
        if i >= len(player_data):
            break
        row = player_data[i]
        if row[1].find("'"):
            row[1] = row[1].replace("'", "'")
        row[1] = '"' + row[1] + '"'
        row = [str(index) + ", " for index in row]
        row = [row[0], row[1], row[3]] + row[5:]
        row[len(row) - 1] = row[len(row) - 1].replace(", ", "")
        query = f'INSERT OR IGNORE INTO Players VALUES ({"".join(row)})'
        cur.execute(query)
    conn.commit()


def main():
    headers, player_data = get_player_data()
    cur, conn = set_up_database("nba.db")
    create_salary_table(cur, conn, headers, player_data)


if __name__ == "__main__":
    main()
