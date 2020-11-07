
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.custom_classes import Team, Match
import csv
import pathlib

def scraping_table(start_year):
	base_url_start = "https://resultados.as.com/resultados/futbol/primera/"
	base_url_end = "/clasificacion/#"

	all_teams_statistics = list()

	if datetime.today().month >= 8:
		end_year = datetime.today().year + 1
	else:
		end_year = datetime.today().year

	current_year = start_year

	while current_year < end_year:
		season = str(current_year) + "_" + str(current_year + 1)
		print("Retrieving season {} information".format(season))

		page = requests.get(base_url_start + season + base_url_end)
		soup = BeautifulSoup(page.content, 'html.parser')

		if current_year > 2013:
			teams = new_format_team_info(soup, season)
		else:
			teams = old_format_team_info(soup, season)

		for team in teams:
			all_teams_statistics.append(team)

		current_year += 1

	export_table(all_teams_statistics)

def scraping_matches(start_year):
	base_url_start = "https://www.marca.com/estadisticas/futbol/primera/"

	all_matches = list()

	if datetime.today().month >= 8:
		end_year = datetime.today().year
	else:
		end_year = datetime.today().year - 1

	current_year = start_year

	while current_year < end_year:
		season = str(current_year) + "_" + str(current_year + 1)[-2:]

		for matchweek in range(1,39):
			print("Retrieving information season {} matchweek {}".format(season, matchweek))

			page = requests.get("https://www.marca.com/estadisticas/futbol/primera/{}/jornada_{}/".format(
				season, matchweek))
			soup = BeautifulSoup(page.content, 'html.parser')

			if current_year >= 2017:
				table = soup.find_all("div", class_="resultados rescalendario borde-caja")[0]
				matches = table.find_all('tr', class_="nolink")
			
			else:
				table = soup.find_all("div", class_="resultados borde-caja")[0]
				matches = table.find_all('tr')

			for match in matches:
				# S'ha pres la decisio de deixar en blanc els resultats
				# dels partits que no es disposa de resultat (pel motiu que sigui)
				if len(match.find_all("td", class_="resultado")) == 0:
					all_matches.append(Match(
						season,
						matchweek,
						match.find("td", class_="equipo-local").get_text(),
						match.find("td", class_="equipo-visitante").get_text(),
						""))  
						
				else:
					all_matches.append(Match(
						season,
						matchweek,
						match.find("td", class_="equipo-local").get_text(),
						match.find("td", class_="equipo-visitante").get_text(),
						match.find("td", class_="resultado").get_text()))

		current_year += 1
	
	export_matches(all_matches)

def new_format_team_info(soup, season):
	teams = []
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


def old_format_team_info(soup, season):
	teams = []
	table_rows = soup.find_all("table", class_="clasi-grup clasi-comp")[0].find_all('tbody')[0].find_all('tr')

	for row in table_rows:
		position = row.find_all("span", class_="pos")[0].get_text()
		team_name = row.find_all("a")[0].get_text()
		statistics = row.find_all("td")[1:]
		team = Team(season, team_name, position, statistics)
		teams.append(team)

	return teams


def export_table(teams):
	with open('{}\\output\\team_data.csv'.format(pathlib.Path(__file__).parent), mode='w', newline='') as teams_file:
		teams_writer = csv.writer(teams_file, delimiter=",")
		teams_writer.writerow(['season', 'name', 'position', 'points', 'played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'h_points', 'h_played', 'h_won', 'h_drawn', 'h_lost', 'h_gf', 'h_ga', 'h_gd', 'a_points', 'a_played', 'a_won', 'a_drawn', 'a_lost', 'a_gf', 'a_ga', 'a_gd'])

		for team in teams:
			teams_writer.writerow(team.export())

def export_matches(matches):
	with open('{}\\output\\matches_data.csv'.format(pathlib.Path(__file__).parent), mode='w', newline='') as matches_file:
		matches_writer = csv.writer(matches_file, delimiter=",")
		matches_writer.writerow(['season', 'matchweek', 'home', 'visitor', 'result'])
			
		for team in matches:
			matches_writer.writerow(team.export())


if __name__ == "__main__":
	start_year = 2019
	scraping_table(start_year)
	# scraping_matches(start_year)

