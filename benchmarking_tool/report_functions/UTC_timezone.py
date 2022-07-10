import pytz
import datetime

def UTC_timezone(date, city):
    now_utc = date
    # capatalize the city name

    c = city.capitalize()

    try:
        tz = pytz.timezone('America/'+c)
        
        now = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
    except:
        tz = pytz.timezone('America/Edmonton')
        now = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
    return now