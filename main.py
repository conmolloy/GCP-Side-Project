import requests
from bs4 import BeautifulSoup 
import re
import pandas as pd


#Returns a pandas dataframe of the results page
def get_results_page_df():	
	#Constants
	#URL for Results on HLTV
	URL = "https://www.hltv.org/results"
	#out_array = array({'winning_team','winning_score','losing_score' , 'losing_team', 'event_name', 'match_URL', 'map_name' })
	out_array = []
	#requesting page an turning it in to a beautiful soup parsing object
	r = requests.get(URL)
	soup = BeautifulSoup(r.text, "html.parser")

	#Selecting CSS element of tables with result sublist
	only_new = soup.select("body > div.bgPadding > div > div.colCon > div.contentCol > div > div.results-holder > div.results-all > div.results-sublist")

	#Selecting only the top 2 tables
	only_top2_soup = BeautifulSoup(str(only_new[0])+str(only_new[1]) , "html.parser")

	#This is going to be the table row that we are going to recursivly search on i.e the rows of our data
	base_tag = only_top2_soup.find_all("div","result-con")

	#Collecting the date before we start
	date = re.findall(r'<span class="standard-headline">Results for(.*)<\/span>', str(only_new[0])+str(only_new[1]))
	print("the date = " + str(date))

	for x in base_tag:
		text = str(x)
		#Regular expressions where data is being collected in the (.*) brackets
		winning_team = re.findall(r'<div class="team team-won">(.*)<\/div>', text)
		winning_score = re.findall(r'<span class="score-won">(\d+)<\/span>', text)
		losing_score = re.findall(r'<span class="score-lost">(\d+)<\/span>', text)
		losing_team = re.findall(r'<div class="team ">(.*)<\/div>', text)
		event_name = re.findall(r'<span class="event-name">(.*)<\/span>', text)
		map_names = re.findall(r'<div class="map-text">(.*)<\/div>|<div class="map map-text">(.*)</div>', text)
		match_URL = re.findall(r'<div class="result-con" data-zonedgrouping-entry-unix="\d+"><a class="a-reset" href="(.*)">', text)
		"""Sometimes the maps can be in 2 different formats so the | in the regular expression turns the data type to a tuple array, so to 
		print i have to iterate through the array first. (Must be a better way!)"""
		test2 = map_names[0][0] + map_names[0][1]

	#if there is a draw
		if (len(losing_team)>1):
			winning_team = losing_team[0]
			losing_team = losing_team[1]
			winning_score = "15"
			losing_score = "15"
		#print outputs
		#print(winning_team , winning_score , losing_score ,  losing_team, event_name, match_URL, map_name)

		out_array.append({'winning_team': winning_team[0], 'winning_score': winning_score[0], 'losing_score': losing_score[0],
		 'losing_team': losing_team[0], 'event_name': event_name[0], 'match_URL': match_URL[0], 'map_name': test2})

		df = pd.DataFrame.from_dict(out_array)

		
	return df
print(get_results_page_df())

#testcommitfromc9
		


