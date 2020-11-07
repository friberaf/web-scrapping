import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pathlib
from src.custom_classes import Team


class ClasificationScraping:
    def __init__(self):
        pass

    def scraping_information(self, start_year):
        # Create the URL baseline
        base_url_start = "https://resultados.as.com/resultados/futbol/primera/"
        base_url_end = "/clasificacion/#"

        self.all_teams_statistics = list()

        # Automatically detects the end year (current season)
        if datetime.today().month >= 8:
            end_year = datetime.today().year + 1
        else:
            end_year = datetime.today().year

        current_year = start_year

        # For each season
        while current_year < end_year:
            season = str(current_year) + "_" + str(current_year + 1)
            print("Retrieving season {} information".format(season))

            # Get the HTML information
            page = requests.get(base_url_start + season + base_url_end)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Scraping different versions of HTML information
            if current_year > 2013:
                teams = self.new_format_team_info(soup, season)
            else:
                teams = self.old_format_team_info(soup, season)

            # Append each team and its statistics to the list
            for team in teams:
                self.all_teams_statistics.append(team)

            current_year += 1
    
    def new_format_team_info(self, soup, season):
        # Scraping and parsing information
        teams = list()
        table = soup.find_all("table", class_="tabla-datos")[0].find_all('tbody')[0]

        team_names = table.find_all('th')
        statistics = table.find_all('td')
        positions = table.find_all("span", class_="pos")

        num_values = int(len(statistics) / len(team_names))

        for i in range(len(team_names)):
            team_name = team_names[i].find("span", class_="nombre-equipo").get_text()
            current_statistics = statistics[num_values * i:num_values * (i + 1)]
            current_position = positions[i].get_text()
            team = Team(season, team_name, current_position, current_statistics)
            teams.append(team)

        return teams

    def old_format_team_info(self, soup, season):
        # Scraping and parsing information
        teams = list()
        table_rows = soup.find_all("table", class_="clasi-grup clasi-comp")[0].find_all('tbody')[0].find_all('tr')

        for row in table_rows:
            position = row.find_all("span", class_="pos")[0].get_text()
            team_name = row.find_all("a")[0].get_text()
            statistics = row.find_all("td")[1:]
            team = Team(season, team_name, position, statistics)
            teams.append(team)

        return teams

    def export(self):
        # Write a CSV file
        with open('{}\\..\\output\\team_data.csv'.format(pathlib.Path(__file__).parent), mode='w', newline='') as teams_file:
            teams_writer = csv.writer(teams_file, delimiter=",")
            teams_writer.writerow(['season', 'name', 'position', 'points', 'played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'h_points', 'h_played', 'h_won', 'h_drawn', 'h_lost', 'h_gf', 'h_ga', 'h_gd', 'a_points', 'a_played', 'a_won', 'a_drawn', 'a_lost', 'a_gf', 'a_ga', 'a_gd'])

            for team in self.all_teams_statistics:
                teams_writer.writerow(team.export())
