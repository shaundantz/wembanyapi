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
    query = f"CREATE TABLE IF NOT EXISTS Players (PLAYER_ID INTEGER PRIMARY KEY, NAME TEXT, TEAM_ID INTEGER, TEAM_ABBR TEXT, {''.join(params)})"
    cur.execute(query)
    last_id = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Players").fetchone()[0]
    for row in player_data:
        add = [(index + ", ") for index in headers[5:]]
        add[len(add) - 1] = add[len(add) - 1].replace(", ", "")
        row = [str(index) + ", " for index in row]
        row = [row[0], row[1], row[3], row[4]] + row[5:]
        row[len(row) - 1] = row[len(row) - 1].replace(", ", "")
        values = ["?, " for index in row]
        values[len(values) - 1] = values[len(values) - 1].replace(", ", "")
        add = "".join(add)
        values = "".join(values)
        row = "".join(row)
        query = f"INSERT OR IGNORE INTO Players (PLAYER_ID, NAME, TEAM_ID, TEAM_ABBR, {add}) VALUES ({row}))"
        print(query)
        cur.execute(query, row)
    conn.commit()


def add_values(cur, conn, headers, player_data):
    last_id = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Salaries").fetchone()[0]
    for i in range(5, len()):
        cur.execute(
            "INSERT INTO Salaries (PLAYER_ID INTEGER PRIMARY KEY, NAME TEXT, TEAM_ID INTEGER, TEAM_ABBR TEXT, ) VALUES (?,?,?)",
            (i + 1, salary_list[i][0], salary_list[i][1]),
        )
    conn.commit()


def main():
    headers, player_data = get_player_data()
    cur, conn = set_up_database("nba.db")
    create_salary_table(cur, conn, headers, player_data)


if __name__ == "__main__":
    main()
