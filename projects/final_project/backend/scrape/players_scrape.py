import argparse
import csv
import os
import time
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests_html import HTMLSession

from exceptions import NeedATagException
""" Using players_scrape.py :

    python players_scrape.py -l [fetches data for latest season]
    python players_scrape.py -p [fetches data for previous season]
    python players_scrape.py -lp[fetches data for both latest and previous
    season]
    ALSO, python players_scrape.py -pl [fetches data for both latest
      and previous season]

"""


def fetch_all_team_url_links(LATEST_SEASON: int) -> Dict[str, str]:
    """
    Fetch link leads to the page with different tables of different team
    standings
    Href links inside each tr of any table leads to that college's
    player stats
    Idea : Get all the links in the tables to get links to all
    college's player stats

    Return : a dict with college name and link to that college's
    all player stats

    """
    team_link_dict = {}
    fetch_link = "https://rollrivers.com/stats.aspx"
    params_dict = {'path': 'msoc', 'year': LATEST_SEASON}
    session = HTMLSession()
    r = session.get(fetch_link, params=params_dict)
    soup = BeautifulSoup(r.content, 'lxml')
    all_a_tags = soup.find('table').find_all('a')

    for a_tag in all_a_tags:
        team_link_dict[a_tag.text] = MAIN_URL + a_tag['href']

    return team_link_dict


def fetch_all_players(all_url_links_dict: Dict[str, str],
                      year: int) -> Tuple[List[str]]:

    session = HTMLSession()
    all_players_info = []
    all_goalkeepers_info = []
    for college in all_url_links_dict:

        # only get conference data
        r = session.get(all_url_links_dict[college] + '&conf=true')

        # render the page
        r.html.render()
        # r.html.html is the path where the renedered code is under
        soup = BeautifulSoup(r.html.html, 'lxml')
        player_tr_elements = soup.find("section", {'id': "player"})\
            .find('tbody').find_all('tr')

        # Fetch goalkeeper stats
        for player_tr_element in player_tr_elements:

            player_info = []
            name = player_tr_element.find('th').text

            player_info.append(college)
            player_info.append(year)
            player_info.append(name)

            for td_element in player_tr_element.find_all('td'):
                player_info.append(td_element.text)

            all_players_info.append(player_info)

        # Fetch goalkeeper stats
        goalkeeper_tr_elements = soup.find("section", {'id': "goalie"})\
            .find('tbody').find_all('tr')

        for goalkeeper_tr_element in goalkeeper_tr_elements:

            goalkeeper_info = []
            name = goalkeeper_tr_element.find('th').text

            goalkeeper_info.append(college)
            goalkeeper_info.append(year)
            goalkeeper_info.append(name)

            for td_element in goalkeeper_tr_element.find_all('td'):
                goalkeeper_info.append(td_element.text)

            all_goalkeepers_info.append(goalkeeper_info)

    headers = ['College', 'Year']
    goalie_headers = headers[:]

    header_elements = soup.find("section", {'id': "player"})\
        .find('thead').find_all('th')
    goalie_header_elements = soup.find("section", {'id': 'goalie'})\
        .find('thead').find_all('th')
    for header_element in header_elements:
        headers.append(header_element.text)

    for goalie_header_element in goalie_header_elements:
        goalie_headers.append(goalie_header_element.text)

    return all_players_info, all_goalkeepers_info, headers, goalie_headers


def create_csv_file(file_name: str, directory_location: str,
                    csv_data_list: List[List[str]], fieldnames: List[str]):

    file_path = os.path.join(directory_location, file_name)
    with open(file_path, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(fieldnames)
        writer.writerows(csv_data_list)


def main(list_of_season_types_to_scrape):
    # Get the current season data and also the previous season data
    # only fetch the previous data if no such csv file already exists since
    # we don't need to fetch unnecessary data
    for season_type in list_of_season_types_to_scrape:

        season_value = LATEST_SEASON if season_type == 'latest'\
              else LATEST_SEASON - 1

        all_url_links_dict: Dict[str, str] = \
            fetch_all_team_url_links(season_value)
        all_player_data: Tuple[List[str]] =\
            fetch_all_players(all_url_links_dict, season_value)

        print(f'---Fetched {season_type} player\'s data successfully---')
        all_players_info, all_goalkeepers_info, player_headers, goalie_headers\
            = all_player_data

        path_for_csv_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'data/csv/')
        for player_type in ['player', 'goalkeeper']:
            csv_file = f'{player_type}_{season_type}.csv'
            if player_type == 'player':
                create_csv_file(csv_file, path_for_csv_file, all_players_info,
                                player_headers)
            else:
                create_csv_file(csv_file, path_for_csv_file,
                                all_goalkeepers_info, goalie_headers)

        print(f'---Saved player data for {season_type} season in ' +
              f'{path_for_csv_file}{csv_file} successfully---')


if __name__ == '__main__':

    start_time = time.time()
    print(os.path.dirname(os.path.dirname(__file__)))
    load_dotenv()

    LATEST_SEASON = int(os.environ.get('LATEST_SEASON'))
    LATEST_SEASON_STARTED = bool(os.environ.get('LATEST_SEASON_STARTED'))
    MAIN_URL = "https://rollrivers.com/"

    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--previous',
                        help='Get previous season\'s players data ' +
                        'Only tag should be provided',
                        action='store_true')
    parser.add_argument('-l',
                        '--latest',
                        help='Get latest season\'s players data' +
                        'Only tag should be provided',
                        action='store_true')
    args = parser.parse_args()

    if args.latest and args.previous:
        main(['latest', 'previous'])
    elif args.latest:
        main(['latest'])
    elif args.previous:
        main(['previous'])
    else:
        print(LATEST_SEASON, LATEST_SEASON_STARTED)
        raise NeedATagException("Need -l and/or -p tag to run " +
                                "(e.g python player_scrape -l will " +
                                "fetch data for latest season")
    end_time = time.time()
    print(f'---Execution Time : {end_time-start_time}---')
