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
        "CREATE TABLE IF NOT EXISTS Salaries (player_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)"
    )
    conn.commit()


def add_values(cur, conn, salaries):
    salary_list = list(zip(salaries.keys(), salaries.values()))
    count = cur.execute("SELECT COALESCE(COUNT(*),0) FROM Salaries").fetchone()[0]
    index = 1
    for i in range(count, count + 25):
        if i >= len(salary_list):
            break
        try:
            id = (
                cur.execute(
                    "SELECT player_id FROM Players WHERE name = ?", ("OG Anunoby",)
                ).fetchone()[0]
                if salary_list[i][0].find("Anunoby") != -1
                else cur.execute(
                    "SELECT player_id FROM Players WHERE name = ?", (salary_list[i][0],)
                ).fetchone()[0]
            )
        except:
            id = index
            index += 1
        cur.execute(
            "INSERT OR IGNORE INTO Salaries (player_id, name, salary) VALUES (?,?,?)",
            (id, salary_list[i][0], salary_list[i][1]),
        )
    conn.commit()


def main():
    salaries = get_salaries()
    cursor, conn = set_up_database("nba.db")
    create_salary_table(cursor, conn)
    add_values(cursor, conn, salaries)

    # Execute a query to get the top 25 player salaries
    query = """
        SELECT name, salary
        FROM Salaries
        GROUP BY name
        ORDER BY salary DESC
        LIMIT 25;
    """
    cursor.execute(query)

    data = cursor.fetchall()

    names, salaries = zip(*data)

    conn.close()
    # salaries_in_millions = [salary * 10 for salary in salaries]
    # print(salaries)

    salaries_in_millions = [salary / 1_000_000 for salary in salaries]

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(names, salaries_in_millions, color="blue")
    plt.xlabel("Player Name")
    plt.ylabel("Salaries (in millions)")
    plt.title("Top 25 Player Salaries in 2023")
    plt.xticks(rotation=45, ha="right")  
    plt.tight_layout()

    line_values = range(len(names))
    plt.plot(
        line_values,
        salaries_in_millions,
        marker="o",
        linestyle="-",
        color="red",
        label="Trendline",
    )
    plt.legend()  
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
