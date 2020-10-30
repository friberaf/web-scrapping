
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Stats:
	def __init__(self, statistics):
		self.points = statistics[0].get_text()
		self.played = statistics[1].get_text()
		self.won = statistics[2].get_text()
		self.drawn = statistics[3].get_text()
		self.lost = statistics[4].get_text()
		self.gf = statistics[5].get_text()
		self.ga = statistics[6].get_text()
		self.gd = int(self.gf) - int(self.ga)


class Team:
	def __init__(self, season, name, statistics):
		self.season = season
		# self.position = position
		self.name = name
		self.total = Stats(statistics[0:7])
		self.home = Stats(statistics[7:14])
		self.away = Stats(statistics[14:21])

	def export(self):
		# TODO: Returns a string containing all the team information to be loaded into a CSV file
		pass


base_url_start = "https://resultados.as.com/resultados/futbol/primera/"
base_url_end = "/clasificacion/#"

all_teams_statistics = list()

# start_year = 2001
start_year = 2014

if datetime.today().month >= 8:
	end_year = datetime.today().year + 1
else:
	end_year = datetime.today().year

current_year = start_year

while current_year < end_year:
	season = str(current_year) + "_" + str(current_year + 1)
	print("Season {}".format(season))

	page = requests.get(base_url_start + season + base_url_end)
	soup = BeautifulSoup(page.content)
	table = soup.find_all("table", class_="tabla-datos")[0].find_all('tbody')[0]

	team_names = table.find_all('th')
	statistics = table.find_all('td')

	num_values = int(len(statistics)/len(team_names))

	for i in range(len(team_names)):
		team_name = team_names[i].find("span", class_="nombre-equipo").get_text()
		current_statistics = statistics[num_values*i:num_values*(i+1)]
		team = Team(season, team_name, current_statistics)
		print("{}: {} points".format(team.name, team.total.points))
		all_teams_statistics.append(team)
	
	current_year += 1

