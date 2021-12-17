
import requests
import sched
import time
import json
import logging

logging.basicConfig(filename='log.log',format='%(levelname)s: %(asctime)s %(message)s',level=logging.DEBUG)

"""taking the data from a configuration file"""

config_file =open('config.json','r')
logging.info('opened the configuration file')
config_data= json.load(config_file)
config_file.close()
covid_news_handler_configs=config_data['covid_news_data']
for data in covid_news_handler_configs:
    base_link= data['baseurl']
    API_key= data['APIkey']





s = sched.scheduler(time.time, time.sleep)


def news_API_request(covidterms="Covid COVID-19 coronavirus")->dict:

	"""this function requests an API for news about covid-19 in England
	and returns the news in a list of dictionaries"""

	base_url = base_link
	api_key = API_key
	country = "gb"
	try:
		complete_url = base_url + "country=" + country + "&apiKey=" + api_key
		response = requests.get(complete_url)
		logging.info('calling the API for covid news')
	except:
		logging.error('news API error')
	#print(response.json())
	#print(complete_url)
	news_dict = response.json()
	articles = news_dict["articles"]
	covid_news=[]
	content_list=[]
	for article in articles:
		titles = article['title']
		contents = article['content']
		if 'coronavirus'in titles or 'Covid'in titles or 'COVID-19'in titles:
			covid_news.append(titles)
			content_list.append(contents)
	#print(covid_news)
	#print(content_list)
	"""putting the titles and contents in a list of dictionaries"""
	news_articles=[]
	for i in covid_news:
		for x in content_list:
			titles_list= dict(title= i,content=x)
		news_articles.append(titles_list)
		#print(news_articles)
	return news_articles





def update_news(time=int):
	logging.info('news update scheduled')
	e1 = s.enter(time, 1, (news_API_request()))


