from flask import Flask, render_template,request
import covid_data_handler
import covid_news_handling
import sched
import time
import time_conversion
import logging

logging.basicConfig(filename='log.log',format='%(levelname)s: %(asctime)s %(message)s',level=logging.DEBUG)

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
updates={}

def time_to_update() -> int:
    """this function will subtract the clint time from current time and output the update time in seconds"""
    try:
        time_to_update_in_sec = time_conversion.time_difference(updates['update_time'])
        logging.info('time to update')
    except:
        logging.error('updat time failed')
    return time_to_update_in_sec



updates_dict={}

@app.route('/index')
def covid_interface():

    s.run(blocking= False)

    """update name"""
    text_field= request.args.get('two')
    if text_field:
       updates['title'] = text_field
       updates_dict['title']=text_field

    """update time"""
    update_time =request.args.get('update')
    if update_time:
        updates['update_time']=(update_time)
        time_to_update()
        #print(update_time)
        updates_dict['content']=update_time

    """repeat up date"""
    repeat=request.args.get('repeat')


    """update covid data"""
    covid_data= request.args.get('covid - data')
    if covid_data:
        try:
            covid_data_handler.schedule_covid_updates(time_to_update(), updates['title'])
        except:
            logging.error('covid data update failed')
    """update news"""
    update_news= request.args.get('news')
    if update_news:
        try:
            covid_news_handling.update_news(time_to_update())
        except:
            logging.error('news update failed')

    print(updates)

    return render_template('index.html',
                           title='National and Local COVID-19 NEWS',
                           news_articles=covid_news_handling.news_API_request(),
                           local_7day_infections=covid_data_handler.covid_API_request()['local_7day_infections'],
                           location= 'Exeter',
                           nation_location= 'England',
                           national_7day_infections=covid_data_handler.covid_API_request()['nation 7 day average'],
                           hospital_cases=covid_data_handler.covid_API_request()['nation hospital cases'],
                           deaths_total= covid_data_handler.covid_API_request()['total deathes'],
                           updates=updates_dict,
                           image='covid.jpg'
                           )

if __name__ == '__main__':

    try:
        app.run()
    except:
       logging.error('run app failed')