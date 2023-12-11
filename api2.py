from nbapy import team as nba
import pandas as pd
import os
import sqlite3
import json


def get_teams():
    teams = {}
    team_data = nba.constants.TEAMS
    for team in team_data:
        teams[team_data[team]["city"] + " " + team_data[team]["name"]] = team_data[
            team
        ]["id"]
    return teams


def get_stats(teams):
    headers = []
    team_stats = {}
    for team in teams:
        id = teams[team]
        data = nba.SeasonResults(
            id, league_id="00", season_type="Regular Season", per_mode="PerGame"
        )
        team_data = data.api.json["resultSets"][0]["rowSet"][
            len(data.api.json["resultSets"][0]["rowSet"]) - 2
        ]
        team_data = [team_data[0]] + team_data[4:14] + team_data[15:]
        if headers == []:
            headers = data.api.json["resultSets"][0]["headers"]
            headers = [headers[0]] + headers[4:14] + headers[15:]
        team_stats[team] = team_data
    write_json(team_stats)
    write_headers(headers)
    return headers, team_stats


def write_json(data, filename="data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def write_headers(headers, filename="headers.json"):
    with open(filename, "w") as f:
        json.dump(headers, f, indent=4)


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def create_table(cur, conn, headers, team_data):
    params = ["TEAM_ID INTEGER PRIMARY KEY, ", "NAME TEXT, "] + [
        (index + " FLOAT, ") for index in headers[1:]
    ]
    params[len(params) - 1] = params[len(params) - 1].replace(", ", "")
    query = f'CREATE TABLE IF NOT EXISTS Teams ({"".join(params)})'
    cur.execute(query)
    count = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Teams").fetchone()[0]
    team_list = list(zip(team_data.keys(), team_data.values()))
    for i in range(count, count + 25):
        if i >= len(team_list):
            break
        row = team_list[i]
        values = [str(index) + ", " for index in row[1]]
        values.insert(1, "'" + str(row[0]) + "', ")
        values[len(values) - 1] = values[len(values) - 1].replace(", ", "")
        query = f'INSERT OR IGNORE INTO Teams VALUES ({"".join(values)})'
        cur.execute(query)
    conn.commit()


def main():
    teams = get_teams()
    if os.path.exists("data.json") and os.path.exists("headers.json"):
        with open("data.json") as f:
            team_stats = json.load(f)
        with open("headers.json") as f:
            headers = json.load(f)
    else:
        headers, team_stats = get_stats(teams)
    cur, conn = set_up_database("nba.db")
    create_table(cur, conn, headers, team_stats)


if __name__ == "__main__":
    main()
