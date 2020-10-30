
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url_start = "https://resultados.as.com/resultados/futbol/primera/"
base_url_end = "/clasificacion/#"

#start_year = 2001
start_year = 2020

if datetime.today().month >= 8:
	end_year = datetime.today().year + 1
else:
	end_year = datetime.today().year


current_year = start_year

#while current_year < end_year:
	# Fer l'extracció
page = requests.get(base_url_start + str(current_year) + "_" + str(current_year + 1) + base_url_end)

soup = BeautifulSoup(page.content)

table = soup.find_all("table", class_="tabla-datos")[0].find_all('tbody')[0]

for team_name in table.find_all('th'):
	print(team_name.find("span", class_="nombre-equipo").get_text())

for td in table.find_all('td'):
	print(td.get_text())

#	current_year += 1
