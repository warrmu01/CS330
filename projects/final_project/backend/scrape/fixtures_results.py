import argparse
import csv
import os
from typing import Dict, List
from datetime import datetime
import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_game_days(LATEST_SEASON: int) -> Dict[str, List[List[str]]]:
    gamedaysdict = {}  # Initialize the dictionary outside the loop
    fetch_link = "https://rollrivers.com/calendar.aspx?path=msoc"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    try:
        browser.get(fetch_link)

        # Wait for dynamic content to load using WebDriverWait with an increased timeout
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.sidearm-calendar-application'))
        )

        parent_elements = browser.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-list-group.sidearm-calendar-table')

        for parent_index, parent_element in enumerate(parent_elements):
            gamedaysdict[parent_index] = {}  # Initialize the dictionary for the current parent

            headers = parent_element.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-list-group-heading.sidearm-calendar-table-caption')

            for header_index, header in enumerate(headers):
                current_date = None  # Move the initialization outside the loop

                date_element = header.find_element(By.CSS_SELECTOR, '.hide-on-medium-down.sidearm-calendar-list-group-heading-date')
                date_str = date_element.text
                current_date = datetime.strptime(date_str, "%A, %B %d, %Y").date()
                # print(f"date_element: {current_date}")

                # Locate the games elements inside the loop for the current header
                games = parent_element.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-list-group-list-game.sidearm-calendar-table-tbody-tr')

                current_games_list = []  # Move the initialization inside the loop

                for game in games:
                    team_elements = game.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-list-group-list-game-team-title')
                    game_played = game.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-time')
                    team_results = game.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-list-group-list-game-team-score.text-no-wrap')
                    game_location_elements = game.find_elements(By.CSS_SELECTOR, '.sidearm-calendar-location')

                    if len(team_elements) == 2 and len(team_results) == 2:
                        away_team = team_elements[0].text.strip()
                        home_team = team_elements[1].text.strip()

                        away_team_score = team_results[0].text.strip()
                        home_team_score = team_results[1].text.strip()

                        game_location = game_location_elements[0].text.strip() if game_location_elements else ""

                        # Check if the game has been played
                        game_played_text = game_played[0].text.strip() if game_played else ""
                        is_final = "Final" in game_played_text

                        current_game_info = [away_team, away_team_score, home_team, home_team_score, game_location, is_final]
                        current_games_list.append(current_game_info)
                    else:
                        print("Warning: Team elements not found or count is not equal to 2.")

                gamedaysdict[parent_index][current_date] = current_games_list

    finally:
        # Make sure to close the browser
        browser.quit()

    # Print the result
    print(f"Final team_link_dict: {gamedaysdict}")

    return gamedaysdict
import os
import csv
from typing import Dict, List

def write_to_csv(gamedaysdict: Dict[str, List[List[str]]], csv_filename: str = "output.csv"):
    parent_directory = os.path.join(os.pardir, "data")
    subdirectory = os.path.join(parent_directory, "csv")

    # Create the subdirectory if it doesn't exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    csv_filename = os.path.join(subdirectory, csv_filename)

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header
        csv_writer.writerow(["Parent Index", "Date", "Away Team", "Away Team Score", "Home Team", "Home Team Score", "Location", "Is Final"])

        for parent_index, date_info in gamedaysdict.items():
            for date, games_list in date_info.items():
                for game_info in games_list:
                    csv_writer.writerow([parent_index, date] + game_info)

    print(f"CSV file '{csv_filename}' created successfully.")

# Example usage:
gamedaysdict = get_game_days(2023)
write_to_csv(gamedaysdict, csv_filename="schedule&results.csv")




# get_game_days(2023)
