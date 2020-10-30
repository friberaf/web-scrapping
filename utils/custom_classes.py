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
	def __init__(self, season, name, position, statistics):
		self.season = season
		# self.position = position
		self.name = name
		self.position = position
		self.total = Stats(statistics[0:7])
		self.home = Stats(statistics[7:14])
		self.away = Stats(statistics[14:21])

	def export(self):
		# TODO: Returns a string containing all the team information to be loaded into a CSV file
		pass