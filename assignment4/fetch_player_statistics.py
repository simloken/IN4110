import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin
import pandas as pd

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##
    
try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()


base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = []
    for i in teams:
        all_players.append(get_players(i['url']))


    #print(all_players)
    # get player statistics for each player,
    # using get_player_stats

    teamStats = {}
    
    for i in teams:
        playersStats = {}
        for j in all_players:
            for k in j:
                stat = get_player_stats(j[k], i)
                if stat != None:
                    playersStats[k] = stat
                    
        teamStats[i['name']] = playersStats
        
    
    # Select top 3 for each team by points:
    bestTotal = {}
    for i in ['points', 'rebounds', 'assists']:
        bestTeam = {}
        for j in teamStats:
            first, second, third = 0, 0, 0
            firstStr, secondStr, thirdStr = '', '', ''
            for k in all_players:
                for k in list(k.keys()):
                    stat = teamStats[str(j)]
                    try:
                        stat[str(k)]
                    except:
                        continue
                    else:
                        stat=stat[str(k)]
                        stat=float(stat[str(i)])
                    if stat > first:
                        third = second; thirdStr = secondStr
                        second = first; secondStr = firstStr
                        first = stat; firstStr = k
                    elif stat > second:
                        third = second; thirdStr = secondStr
                        second = stat; secondStr = k
                    elif stat > third:
                        third = stat; thirdStr = k
            
            bestTeam[j] = {firstStr: first, secondStr: second, thirdStr: third}
        bestTotal[i] = bestTeam

    for i in ['points', 'rebounds', 'assists']:
        plot_best(bestTotal[i], stat=i)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.
    """
    stats_dir = "NBA_player_statistics"
    namesAll = []
    df = pd.DataFrame(np.zeros((len(best), 3)), index=list(best.keys()), columns=['1st', '2nd', '3rd'])
    for i in best:
        names = list(best[i].keys())
        vals = ([best[i][names[0]], best[i][names[1]], best[i][names[2]]])
        df.loc[str(i)] = vals
        namesAll.append(names)        
    
    fig = df.plot.bar(rot=0, stacked=False, color=['c', 'cadetblue', 'skyblue'], figsize=(12,10))
    plt.title('Top 3 players per team for average %s per game' %(stat))
    plt.xlabel('Teams')
    plt.ylabel('Points')
    
    rects = fig.patches
    labels = [x for l in namesAll for x in l] #flatten list
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        fig.text(
            rect.get_x() + rect.get_width() / 2, height/1.2, label, ha="center", va="bottom",
        rotation=60, color='white', path_effects=[pe.withStroke(linewidth=1.5, foreground="black")], size=12)
    
    plt.savefig(stats_dir + '/' + stat + '.png')
    plt.show()


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> dict:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        players (dict) : dict with player keys
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table")
    rows = [tr.text.strip() for tr in table.find_all('tr')]
    rows = rows[3:]
    players = {}
    for i in rows:
        temp = i.split('\n')
        name = temp[4]
        player = ('{} {}'.format(name.split(', ')[1],name.split(', ')[0]))
        player = re.sub(r'\([^)]*\)', '', player) #removes parentheses terms
        name = re.sub(r'\([^)]*\)', '', name) #removes parentheses terms
        if '\xa0' in player:
            player = player.split('\xa0')[0] + player.split('\xa0')[1]
            
        if '\xa0' in name:
            tname = ''
            for i in range(len(name.split('\xa0'))):
                tname = tname + name.split('\xa0')[i]
            
            name = tname
        
        url = soup.find('a', string=re.compile(name, flags=re.S | re.I))
        players[player] = re.search(r'href=\"(.*?)\"', str(url), flags = re.S | re.I).group()[6:-1]
    

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(base_url + player_url)
    soup = BeautifulSoup(html, "html.parser")
    try:
        soup.find(id="NBA").find_next("table")
    except:
        table = soup.find(id="Regular_season").find_next("table")
    else:
        table = soup.find(id="NBA").find_next("table")
        
    rows = [tr.text.strip() for tr in table.find_all('tr')]
    rows = rows[1:]
    j = -1
    for i in rows:
        if team['name'] in i: 
            if '2021–22' in i:
                season = i
            else: #for cases where they've been on multiple teams and gathering team is the latter of the two
                if '2021–22' in rows[j]:
                    season = i
    
        j += 1
        
    try:
        season
        
        
    except:
        return
    
    else:
        season = re.sub(r'\**', season, '', flags = re.I | re.S)
        season = season.split('\n')
        
        
        stats = {}
        
        stats['points'] = re.sub(r'\*', '', season[-1])
        stats['rebounds'] = re.sub(r'\*', '', season[-5])
        stats['assists'] = re.sub(r'\*', '', season[-4])


        return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
