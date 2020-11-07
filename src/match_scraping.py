import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pathlib
from src.custom_classes import Match


class MatchScraping:
    def __init__(self):
        pass

    def scraping_information(self, start_year):
        self.all_matches = list()

        # Automatically detects the end year (current season)
        if datetime.today().month >= 8:
            end_year = datetime.today().year
        else:
            end_year = datetime.today().year - 1

        current_year = start_year

        # For each season
        while current_year < end_year:
            season = str(current_year) + "_" + str(current_year + 1)[-2:]

            # For each matchweek
            for matchweek in range(1,39):
                print("Retrieving information season {} matchweek {}".format(season, matchweek))

                # Get the HTML information
                page = requests.get("https://www.marca.com/estadisticas/futbol/primera/{}/jornada_{}/".format(
                    season, matchweek))
                soup = BeautifulSoup(page.content, 'html.parser')

                # Scraping and parsing information
                if current_year >= 2017:
                    table = soup.find_all("div", class_="resultados rescalendario borde-caja")[0]
                    matches = table.find_all('tr', class_="nolink")
                
                else:
                    table = soup.find_all("div", class_="resultados borde-caja")[0]
                    matches = table.find_all('tr')

                for match in matches:
                    # Append each match to the list
                    # If the result does not exist, it is repaced for blank
                    if len(match.find_all("td", class_="resultado")) == 0:
                        self.all_matches.append(Match(
                            season,
                            matchweek,
                            match.find("td", class_="equipo-local").get_text(),
                            match.find("td", class_="equipo-visitante").get_text(),
                            ""))  
                            
                    else:
                        self.all_matches.append(Match(
                            season,
                            matchweek,
                            match.find("td", class_="equipo-local").get_text(),
                            match.find("td", class_="equipo-visitante").get_text(),
                            match.find("td", class_="resultado").get_text()))

            current_year += 1

    def export(self):
        # Write a CSV file
        with open('{}\\..\\output\\match_data.csv'.format(pathlib.Path(__file__).parent), mode='w', newline='') as matches_file:
            matches_writer = csv.writer(matches_file, delimiter=",")
            matches_writer.writerow(['season', 'matchweek', 'home', 'visitor', 'result'])
                
            for team in self.all_matches:
                matches_writer.writerow(team.export())