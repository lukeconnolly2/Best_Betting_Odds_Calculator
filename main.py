import json
from fractions import Fraction

import requests as r
import secrets

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



sports_endpoint = f"https://api.the-odds-api.com/v4/sports?apiKey={secrets.api_key}"


def main():
    dict_of_sports = get_sports()
    sport = choose_sport(dict_of_sports)

    region = "uk"
    markets = "h2h"
    odds_endpoint = f"https://api.the-odds-api.com/v4/sports/{sport}" \
                    f"/odds/?" \
                    f"apiKey={secrets.api_key}" \
                    f"&regions={region}" \
                    f"&markets={markets}"

    for match in r.get(odds_endpoint).json():
        try:
            print(f"\n{bcolors.HEADER}{match['home_team']} vs {match['away_team']} at {match['commence_time']}{bcolors.ENDC}")
            #print(json.dumps(match, indent=4))
            for bookie in match["bookmakers"]:
                print(f"\n{bcolors.OKCYAN}{bookie['title']}{bcolors.ENDC}")
                for market in bookie['markets']:
                    print(f"{bcolors.OKBLUE}\n{market['key']}{bcolors.ENDC}")
                    print_outcomes(market['outcomes'])
            print(f"{bcolors.WARNING}\nBest h2h odds{bcolors.ENDC}")
            get_best_odds(match)
        except:
            print(match)


def print_outcomes(outcomes):
    for outcome in outcomes:
        print(f"{outcome['name']} - {outcome['price']}")


def get_sports():
    list_of_sports = []
    for i, sport in enumerate(r.get(sports_endpoint).json()):
        if sport['description'] != "":
            print(f"{i}. {sport['description']}")
            list_of_sports.append(sport['key'])
    return list_of_sports


def choose_sport(list_of_sports):
    while True:
        choice = int(input("Enter the number of the sport you want to view odds from: "))
        if choice in range(0, len(list_of_sports)):
            break
        print("Choice isn't in list, Try again")
    return list_of_sports[choice]


def get_best_odds(match):
    home_team = match['home_team']
    away_team = match['away_team']
    best_home_odds = 0
    best_home_odds_bookie = ""
    best_away_odds = 0
    best_away_odds_bookie = ""
    best_draw_odds = 0
    best_draw_bookie = ""
    bookmakers = match['bookmakers']
    arbs = []
    for bookie in bookmakers:
        for prices in bookie['markets'][0]['outcomes']:
            if prices['name'] == home_team and prices['price'] > best_home_odds:
                best_home_odds = prices['price']
                best_home_odds_bookie = bookie['title']
            if prices['name'] == away_team and prices['price'] > best_away_odds:
                best_away_odds = prices['price']
                best_away_odds_bookie = bookie['title']
            if prices['name'] == "Draw" and prices['price'] > best_draw_odds:
                best_draw_odds = prices['price']
                best_draw_bookie = bookie['title']

    print(f"Best {home_team} odds: {best_home_odds} on {best_home_odds_bookie}")
    print(f"Best {away_team} odds: {best_away_odds} on {best_away_odds_bookie}")
    if best_draw_odds != 0:
        print(f"Best Draw odds: {best_draw_odds} on {best_draw_bookie}")

    if best_home_odds != 0 and best_away_odds != 0:
        if best_draw_odds == 0:
            arb = ((1 / best_home_odds) * 100 + (1 / best_away_odds) * 100)
        else:
            arb = ((1 / best_home_odds) * 100 + (1 / best_away_odds) * 100) + ((1/ best_draw_odds) * 100)

        if arb < 100:
            print(f"{bcolors.FAIL}Theres an arb of {round(100 - arb, 5)}%{bcolors.ENDC}")


if __name__ == '__main__':
    main()
