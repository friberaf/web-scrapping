
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.custom_classes import Team
import pandas as pd


def scraping():
	base_url_start = "https://resultados.as.com/resultados/futbol/primera/"
	base_url_end = "/clasificacion/#"

	all_teams_statistics = list()

	# start_year = 2001
	start_year = 2020

	if datetime.today().month >= 8:
		end_year = datetime.today().year + 1
	else:
		end_year = datetime.today().year

	current_year = start_year

	while current_year < end_year:
		season = str(current_year) + "_" + str(current_year + 1)
		# print("Season {}".format(season))

		page = requests.get(base_url_start + season + base_url_end)
		soup = BeautifulSoup(page.content)

		if current_year > 2013:
			teams = new_format_team_info(soup, season)
		else:
			teams = old_format_team_info(soup, season)

		for team in teams:
			all_teams_statistics.append(team)

		current_year += 1

	#Export results
	for team in all_teams_statistics:
		print("{} got {} points".format(team.name, team.total.points))
		df = team.export()
		# print(df)



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
		current_postition = positions[i].get_text()
		team = Team(season, team_name, current_postition, current_statistics)
		# print("{}. {}: {} points".format(team.position, team.name, team.total.points))
		teams.append(team)

	return teams


def old_format_team_info(soup, season):
	teams = []
	table = soup.find_all("table", class_="tabla-datos")[0].find_all('tbody')[0]

	team_names = table.find_all('th')
	statistics = table.find_all('td')
	positions = table.find_all("span", class_="pos")

	num_values = int(len(statistics) / len(team_names))

	for i in range(len(team_names)):
		team_name = team_names[i].find("span", class_="nombre-equipo").get_text()
		current_statistics = statistics[num_values * i:num_values * (i + 1)]
		current_postition = positions[i].get_text()
		team = Team(season, team_name, current_postition, current_statistics)
		# print("{}. {}: {} points".format(team.position, team.name, team.total.points))
		teams.append(team)

	return teams


if __name__ == "__main__":
	scraping()

