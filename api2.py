from nbapy import team as nba
import pandas as pd
import json


def get_teams():
    teams = {}
    team_data = nba.constants.TEAMS
    for team in team_data:
        teams[team_data[team]['city'] + " " + team_data[team]['name']] = team_data[team]['id']
    return teams


def get_stats(teams):
    headers = []
    team_stats = {}
    for team in teams:
        id = teams[team]
        data = nba.SeasonResults(id, league_id="00",season_type="Regular Season",per_mode="PerGame")
        team_data = data.api.json["resultSets"][0]["rowSet"][len(data.api.json["resultSets"][0]["rowSet"]) - 2]
        team_data = [team_data[0]] + team_data[4:14] + team_data[15:]
        if headers == []:
            headers = data.api.json["resultSets"][0]["headers"]
            headers = [headers[0]] + headers[4:14] + headers[15:]
        team_stats[team] = team_data
    return headers, team_stats

def main():
    teams = get_teams()
    headers, team_stats = get_stats(teams)


if __name__ == "__main__":
    main()
