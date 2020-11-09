from src.classification_scraping import ClasificationScraping
from src.match_scraping import MatchScraping


if __name__ == "__main__":
	# Data exists from 2001. Start_year can't be smaller than this value
	start_year = 2001

	if start_year < 2001:
		print("Start year has to be at least 2001. There is no previous data")
		start_year = 2001
	
	# Class constructors
	scraping_classification = ClasificationScraping()
	scraping_matches = MatchScraping()

	# Calling both scraping functions
	scraping_classification.scraping_information(start_year)
	scraping_matches.scraping_information(start_year)

	# Export results to CSV files
	scraping_classification.export()
	scraping_matches.export()
