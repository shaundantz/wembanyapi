# Purpose: To test ESPN requests and scrape salary data
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import matplotlib.pyplot as plt


def get_salaries():
    salaries = {}
    url = "https://www.espn.com/nba/salaries/_/year/2023/page/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    for i in range(15):
        response = requests.get(
            url + str(i),
            headers=header,
        )
        if response.status_code == 200:
            html = response.text
        else:
            print("The web page you requested failed to respond")
        soup = BeautifulSoup(html, "html.parser")
        salary_data = []
        table = soup.find("table", class_="tablehead")
        salary_data = table.find_all("tr", {"class": ["oddrow", "evenrow"]})
        for player in salary_data:
            name = player.find("a").text
            salary = player.find_all("td")[3].text.strip("$").replace(",", "")
            salaries[name] = salary
    return salaries


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def create_salary_table(cur, conn):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Salaries (player_id INTEGER PRIMARY KEY, salary INTEGER)"
    )
    conn.commit()


def add_values(cur, conn, salaries):
    salary_list = list(zip(salaries.keys(), salaries.values()))
    count = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Salaries").fetchone()[0]
    index = cur.execute("SELECT COALESCE(MAX(player_id),0) FROM Salaries WHERE player_id < 2544").fetchone()[0] + 1
    for i in range(count, count + 25):
        if i >= len(salary_list):
            break
        try:
            id = (
                cur.execute(
                    "SELECT player_id FROM Players WHERE NAME = ?", ("OG Anunoby",)
                ).fetchone()[0]
                if salary_list[i][0].find("Anunoby") != -1
                else cur.execute(
                    "SELECT player_id FROM Players WHERE NAME = ?", (salary_list[i][0],)
                ).fetchone()[0]
            )
        except:
            id = index
            index += 1
        cur.execute(
            "INSERT OR IGNORE INTO Salaries (player_id, salary) VALUES (?,?)",
            (id, salary_list[i][1]),
        )
    conn.commit()


def main():
    salaries = get_salaries()
    cursor, conn = set_up_database("nba.db")
    create_salary_table(cursor, conn)
    for i in range(22):
        add_values(cursor, conn, salaries)

if __name__ == "__main__":
    main()
