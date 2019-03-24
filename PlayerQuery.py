import pandas as pd
import matplotlib as plt

def teamSearch(teamName):
    teams = pd.read_html("https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations", header=0)
    team_names = pd.DataFrame(columns=["Abbreviation/Acronym", "Franchise"])
    team_names = team_names.append(teams)

    for row in team_names.itertuples(index=False, name="Pandas"):
        if row[1] == teamName:
            teamName = row[0]
            break

    return teamName

# def main():
#     stats = pd.read_csv("https://rotogrinders.com/projected-stats/nba-player.csv?site=fanduel", delimiter=",", header=None, names=["Name", "Salary", "Team", "Position", "Opposing", "Ceiling", "Floor", "Points"])
#
#     for row in stats.itertuples(index = False, name = "Pandas"):
#         row[0].strip().title()
#
#     searchType = input("Search by team name or player name? (team/player) ").title()
#     if searchType == "Player":
#         player = input("Which player? ").strip()
#         for row in stats.itertuples(index = False, name = "Pandas"):
#             if row[0] == player:
#                 print(row)
#                 break
#     elif searchType == "Team":
#         team = input("Which team? ")
#         team = teamSearch(team)
#         for row in stats.itertuples(index = False, name = "Pandas"):
#             if row[2] == team:
#                 print(row)

def main():
    stats = pd.read_csv("https://rotogrinders.com/projected-stats/nba-player.csv?site=fanduel", delimiter=",", header = None, names = ["Name", "Salary", "Team", "Position", "Opposing", "Ceiling", "Floor", "Points"])
    for row in stats.itertuples(index=False, name="Pandas"):
        row[0].strip().title()
    stats.plot(x = "Floor", y = "Ceiling")
    print("plotted")

main()