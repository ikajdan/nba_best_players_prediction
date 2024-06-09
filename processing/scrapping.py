import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def fetch_players_stats(year):
    """
    Fetches all players stats for a given year

    Args:
    year (int): the year to fetch the stats for

    Returns:
    DataFrame: the season stats for the given year
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        table = soup.find("table", {"id": "advanced_stats"})

        headers = [th.getText() for th in table.thead.find_all("th")]
        headers = headers[1:]
        rows = table.tbody.find_all("tr")

        player_stats = []
        for row in rows:
            if row.find("td"):
                player_data = [td.getText() for td in row.find_all("td")]
                if len(player_data) == len(headers):
                    player_stats.append(player_data)

        df = pd.DataFrame(player_stats, columns=headers)
        return df
    return []


def fetch_all_nba_teams(year):
    """
    Fetches the All-NBA teams for a given year

    Args:
    year (int): the year to fetch the All-NBA teams for

    Returns:
    list: the players in the All-NBA teams for the given year
    """
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        all_nba_players = []
        tables = soup.find_all("table")
        for table in tables:
            if "All-NBA" in table.text:
                rows = table.find_all("tr")[1:]
                for row in rows:
                    player_cell = row.find("td", {"data-stat": "player"})
                    if player_cell and player_cell.a:
                        player = player_cell.a.get_text()
                        all_nba_players.append(player)
        return all_nba_players[:15]
    return []


def fetch_rookies(year):
    """
    Fetches the rookies for a given year

    Args:
    year (int): the year to fetch the rookies for

    Returns:
    DataFrame: the rookies for the given year
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_rookies.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        table = soup.find("table")

        headers = [th.getText() for th in table.thead.find_all("th")]

        rows = table.tbody.find_all("tr")
        rookies = []
        for row in rows:
            if row.find("td"):
                rookie_data = {
                    headers[i + 5]: td.getText()
                    for i, td in enumerate(row.find_all("td"))
                }
                rookies.append(rookie_data)

        df = pd.DataFrame(rookies)
        return df
    return []


def fetch_rookie_teams(year):
    """
    Fetches the All-Rookie teams for a given year

    Args:
    year (int): the year to fetch the All-Rookie teams for

    Returns:
    list: the players in the All-Rookie teams for the given year
    """
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        all_rookie_players = []
        table = soup.find("table", {"id": "leading_all_rookie"})
        if table:
            rows = table.find_all("tr")[1:]
            for row in rows:
                player_cell = row.find("td", {"data-stat": "player"})
                if player_cell and player_cell.a:
                    player = player_cell.a.get_text()
                    all_rookie_players.append(player)
        return all_rookie_players[:10]
    return []


def process_data(raw_data):
    """
    Processes the raw data by dropping NaN values, converting columns to numeric, and removing duplicate players

    Args:
    raw_data (DataFrame): the raw data to process

    Returns:
    DataFrame: the processed data
    """
    raw_data = raw_data.dropna()
    raw_data = raw_data.apply(pd.to_numeric, errors="ignore")
    tot_rows = raw_data[raw_data["Tm"] == "TOT"]
    unique_players = raw_data[~raw_data["Player"].duplicated(keep=False)]
    raw_data = pd.concat([tot_rows, unique_players])
    return raw_data


def get_data(year_from, year_to):
    """
    Fetches the data for the given range of years

    Args:
    year_from (int): the starting year
    year_to (int): the ending year

    Returns:
    DataFrame: the combined data for the given range of years
    """
    data = []

    for year in range(year_from, year_to):
        stats = fetch_players_stats(year)
        processed_stats = process_data(stats)
        all_nba_players = fetch_all_nba_teams(year)
        rookies = fetch_rookies(year)
        all_rookies = fetch_rookie_teams(year)

        rookie_names = rookies["Player"].tolist() if not rookies.empty else []

        processed_stats["ANBA"] = processed_stats["Player"].apply(
            lambda x: 1 if x in all_nba_players else 0
        )

        processed_stats["RK"] = processed_stats["Player"].apply(
            lambda x: 1 if x in rookie_names else 0
        )

        processed_stats["ANBARK"] = processed_stats["Player"].apply(
            lambda x: 1 if x in all_rookies else 0
        )
        processed_stats["Year"] = year
        data.append(processed_stats)

    concatenated_data = pd.concat(data, ignore_index=True)
    concatenated_data = concatenated_data.dropna(axis=1)

    return concatenated_data


print("Fetching data...")
nba_data = get_data(2018, 2024)
print(nba_data.head())
print(nba_data.shape)
nba_data.to_csv("./data/nba_data.csv", index=False)

nba_data = get_data(2024, 2025)
print(nba_data.head())
print(nba_data.shape)
nba_data.to_csv("./data/nba_data_2024.csv", index=False)
