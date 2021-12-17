"""a module to handle covid data"""
import csv
import json
import requests
import time
import sched
import logging

logging.basicConfig(filename='log.log',format='%(levelname)s: %(asctime)s %(message)s', level=logging.DEBUG)


"""configuration data"""
config_file =open('config.json','r')
config_data= json.load(config_file)
config_file.close()
covid_data_handler_configs=config_data['covid_data']
for data in covid_data_handler_configs:
    Exeter_url= data['exeterurl']
    england_url= data['englandurl']

s = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename)->list:
    """this is a function takes the data from the csv file and returns it in a list"""
    temp = []
    with open('{}'.format(csv_filename), 'r') as f:
        reader = csv.reader(f)
        logging.info('reading csv file')
        for line in reader:
            temp.append(",".join(line))


   # print(temp)
    return temp




parse_csv_data('nation_2021-10-28.csv')

"""data processing"""

def process_covid_csv_data(covid_csv_data)->int:
    """this function iterates through the data from the list in parse_csv_data and returns the last 7 days cases,
    hospital cases and cumulative deaths """
    hospital_cases, cumulative_deaths, last_7_days = "", "", ""
    commas = 0
    commass=0


    """hospital cases"""
    for character in covid_csv_data[1]:
        if character == ',':
            commas += 1
        elif commas == 5:
            hospital_cases += character
    #print(hospital_cases)

    """cumualtive deathes"""
    for character in covid_csv_data[14]:
        if character == ',':
            commass += 1
        elif commass == 4:
            cumulative_deaths += character
    #print(cumulative_deaths)

    """7 day avarage"""
    a= (covid_csv_data[3:10])
    i=0
    w=[]
    while i < len(a):
        for z in a:
            v= a[i].split(',')

            n = v[6]
            w.append(n)
        i = i +1
    w = list(dict.fromkeys(w))
    x = [int(i)for i in w]
    last_7_days= sum(x)
    #print(last_7_days)

    return last_7_days, int(hospital_cases), int(cumulative_deaths)

process_covid_csv_data(parse_csv_data("nation_2021-10-28.csv"))


"""live data access:"""
def covid_API_request(location = 'Exeter',location_type = 'ltla')->dict:

    """requesting an API"""


    england_filter= england_url
    exeter_filter= Exeter_url
    structure='{"date":"date","name":"areaName"'
    new_cases=',"newCasesByPublishDate":"newCasesByPublishDate"'
    hospital_cases=',"hospitalCases":"hospitalCases"'
    cum_deates= ',"cumDeaths28DaysByPublishDate":"cumDeaths28DaysByPublishDate"'
    end='}'
    England_url= england_filter+structure+new_cases+hospital_cases+cum_deates+end
    exeter_url =exeter_filter+structure+new_cases+end

    """requesting the API for England"""

    try:
        response_England = requests.get(England_url)
        covid_england_dict = response_England.json()
        logging.info('calling the API for covid data in England')
    except:
        logging.error('covid data API error')


    covid_england_dict = covid_england_dict["data"]
    cases_list=[]
    deathes_list=[]
    hospital_list=[]
    for data in covid_england_dict:
        newcases = data['newCasesByPublishDate']
        deathes = data['cumDeaths28DaysByPublishDate']
        hospital_Casess= data['hospitalCases']
        cases_list.append(newcases)
        deathes_list.append(deathes)
        hospital_list.append(hospital_Casess)
    last7days= cases_list[0:7]
    nation_7_day_infection_rate=sum(last7days)
    Hospital_cases=[]
    if hospital_list[0]==None:
        Hospital_cases.append(hospital_list[1])
    else:Hospital_cases.append(hospital_list[0])

    """requesting an API for Exeter"""

    response_exeter = requests.get(exeter_url)
    covid_exeter_dict = response_exeter.json()
    data_exeter_dict = covid_exeter_dict["data"]
    exeter_cases_list = []
    for data in data_exeter_dict:
        exeter_cases=data['newCasesByPublishDate']
        exeter_cases_list.append(exeter_cases)
    exeter_last_7_day_cases=exeter_cases_list[0:7]
    local_7day_infections=sum(exeter_last_7_day_cases)
    #print(local_7day_infections)

    """appending all the data in a dictionary"""
    Covid_data={'local_7day_infections':local_7day_infections,'nation 7 day average':nation_7_day_infection_rate,'nation hospital cases':Hospital_cases[0],'total deathes':deathes_list[0],}
    #print(England_url)
    #print(Covid_data)
    return Covid_data


covid_data_dict={}
firsttimerunning=True
if firsttimerunning==True:
    covid_data_dict=covid_API_request()
    firsttimerunning=False

def schedule_covid_updates(update_interval=int,update_name=str):
   """scheduling covid data"""
   logging.info('scheduling an update for covid data')
   e1 = (update_interval, 1, (covid_API_request()))



