import pandas as pd


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
		output_df = pd.DataFrame()

		output_df['Season'] = self.season
		# output_df[''] = self.position
		output_df['Team'] = self.name
		output_df['Position'] = self.position

		output_df['total_Points'] = self.total.points
		output_df['total_Played'] = self.total.played
		output_df['total_Won'] = self.total.won
		output_df['total_Drawn'] = self.total.drawn
		output_df['total_Lost'] = self.total.lost
		output_df['total_GF'] = self.total.gf
		output_df['total_GA'] = self.total.ga
		output_df['total_GD'] = self.total.gd

		output_df['home_Points'] = self.home.points
		output_df['home_Played'] = self.home.played
		output_df['home_Won'] = self.home.won
		output_df['home_Drawn'] = self.home.drawn
		output_df['home_Lost'] = self.home.lost
		output_df['home_GF'] = self.home.gf
		output_df['home_GA'] = self.home.ga
		output_df['home_GD'] = self.home.gd

		output_df['away_Points'] = self.away.points
		output_df['away_Played'] = self.away.played
		output_df['away_Won'] = self.away.won
		output_df['away_Drawn'] = self.away.drawn
		output_df['away_Lost'] = self.away.lost
		output_df['away_GF'] = self.away.gf
		output_df['away_GA'] = self.away.ga
		output_df['away_GD'] = self.away.gd

		print("--- in ---")
		print(output_df)
		print("out")

		return output_df