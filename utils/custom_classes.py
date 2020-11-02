
class Stats:
	def __init__(self, statistics):
		self.points = statistics[0].get_text().strip()
		self.played = statistics[1].get_text().strip()
		self.won = statistics[2].get_text().strip()
		self.drawn = statistics[3].get_text().strip()
		self.lost = statistics[4].get_text().strip()
		self.gf = statistics[5].get_text().strip()
		self.ga = statistics[6].get_text().strip()
		self.gd = int(self.gf) - int(self.ga)


class Team:
	def __init__(self, season, name, position, statistics):
		self.season = season.strip()
		self.name = name.strip()  # Strip as there's break lines in both sides.
		self.position = position.strip()
		self.total = Stats(statistics[0:7])
		self.home = Stats(statistics[7:14])
		self.away = Stats(statistics[14:21])

	# Ordre del header:
	# season,name,position,points,played,won,drawn,lost,gf,ga,gd,h_points,h_played,h_won,h_drawn,h_lost,h_gf,h_ga,h_gd,a_points,a_played,a_won,a_drawn,a_lost,a_gf,a_ga,a_gd
	def export(self):
		team_list = list()
		team_list.extend((self.season, self.name, self.position, self.total.points, self.total.played, self.total.won, self.total.drawn, self.total.lost, self.total.gf, self.total.ga, self.total.gd, self.home.points, self.home.played, self.home.won, self.home.drawn, self.home.lost, self.home.gf, self.home.ga, self.home.gd, self.away.points, self.away.played, self.away.won, self.away.drawn, self.away.lost, self.away.gf, self.away.ga, self.away.gd))

		return team_list

