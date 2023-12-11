# Purpose: To test ESPN requests and scrape salary data
import requests
from bs4 import BeautifulSoup
import sqlite3
import os

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
    cur.execute("CREATE TABLE IF NOT EXISTS Salaries (player_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)")
    conn.commit()

def add_values(cur, conn, salaries):
    salary_list = list(zip(salaries.keys(), salaries.values()))
    last_id = cur.execute("SELECT COALESCE(MAX(player_id),0) FROM Salaries").fetchone()[0]
    for i in range(last_id,last_id+25):
        cur.execute("INSERT INTO Salaries (player_id, name, salary) VALUES (?,?,?)", (i+1, salary_list[i][0], salary_list[i][1]))
    conn.commit()

def main():
    salaries = get_salaries()
    cur, conn = set_up_database("nba.db")
    create_salary_table(cur, conn)
    add_values(cur, conn, salaries)

if __name__ == "__main__":
    main()
