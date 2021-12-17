introduction:
the 'interface.py' module has the code for the website in 'index.html'.
it uses the code from 'covid_data_handler.py'and 'covid_news_handling.py'
to call an API to display local and national covid news and statistics.


openning the dashboard:
the 'interface.py' will be hosted at http://127.0.0.1:5000/index.updates can 
be schdueled by the client and the news will be related to covid news in the
UK, the covid data is updated every 24h. 'log.log' will record all events and
errors when running the module.


python packages:
flask(Flask,render_template,repuest)
sched
logging
time
repuests
json
csv


functionality:
the 'config.json' has all the important data incase the user wants to change
any thing.
the 'time_conversion.py' is used to convert the update time askes from the
client and returns it in seconds.
the 'test_covid_data_handler.py' and 'test_covid_news_handling.py' 
test wether the functions are returning the correct values.


important links:
GitHub repository -
how to get your own API key here: "https://newsapi.org/account"
News API link - https://newsapi.org/
Covid API link - https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/


this module was written by Omar Nasser, Exeter University.