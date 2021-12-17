import datetime


def minutes_to_seconds(minutes: str) -> int:
    """Converts minutes to seconds"""
    return int(minutes) * 60


def hours_to_minutes(hours: str) -> int:
    """Converts hours to minutes"""
    return int(hours) * 60


def hhmm_to_seconds(hhmm: str) -> int:
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
           minutes_to_seconds(hhmm.split(':')[1])

def current_time() ->str:
    """this function gets the real time"""
    now= datetime.datetime.now().strftime('%H:%M')
    return now
current_time()

def time_difference(clint_time):
    print('updating...')
    x= hhmm_to_seconds(current_time())
    y= hhmm_to_seconds(clint_time)
    time_in_seconds=y-x
    return time_in_seconds