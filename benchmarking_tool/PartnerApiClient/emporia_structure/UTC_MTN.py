# helper function to convert utc to loacal time. 
# takes in a list of date and time 
# time returned is in UTC (unix time) every second since jan 1970 
from datetime import datetime 
from dateutil import tz
import pandas as pd
def UTC_MTN(date_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    r = []
    
    for i in date_time:
        utc = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)

        r.append(central)

    

    dater = pd.DataFrame(columns = ['datetime'])

    dater['datetime'] = r
    

    return dater