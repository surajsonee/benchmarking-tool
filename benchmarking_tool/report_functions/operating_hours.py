# we need a function to get operating hours of the facility for the past month
from datetime import date
# d is the 
# start hour and end hour have to be in 24 hour time from
def operating_hours(d, days_per_week, start_hour, end_hour):
    #get the number of days in that month
    try:
        if d.month + 1 > 12:
            m = 1 
            y = d.year + 1
        else:
            m = d.month + 1
            y = d.year

    except:
        print('date is not a data time structure')
        return


    number_days = (date(y,m,1) - date(d.year,d.month,1)).days
    if number_days > 31: # this is if the year has changed over
        number_days = 31 # this will only happen in december that has 31 days 

    # init a on hours list. this is a list that will show number of hours that are in operation 
    calander = []
    days_per_week = days_per_week - 1 # this gets the days per week into the right format 
    for day in range(number_days):
        day_dict = {}
        date_day = date(d.year,d.month,day+1)
        '''
        weekday is a number between 0-6 for monday to sunday 
        
        monday = 0
        tuesday = 1
        wednesday = 2
        thursday = 3
        friday = 4
        saturday = 5
        sunday = 6
        '''
        weekday = date_day.weekday()
        '''
        now we need to know the operational days 
        need to make some assumptions here. 
        if there is only 1 day we will assume it is a monday. 
        if it is 5 days we will assume it is monday-friday. 

        the datastructure for a calander will be a list of length 31 all dictionaries dictionaries. 

        a day structure if {day: 00-00-00, weekday: 0-6,on-hours: boolean, start_hours: 0-24, end_hours: 0-24, total_energy_usage:  }
        '''
        if weekday <= days_per_week: 
            # then the day in the week is part of the on day 
            day_dict['day'] = date_day
            day_dict['weekday'] = weekday
            day_dict['on-hours'] = True
            day_dict['start_hours'] = start_hour
            day_dict['end_hours'] = end_hour

        elif weekday > days_per_week:
            # the off hours day
            day_dict['day'] = date_day
            day_dict['weekday'] = weekday
            day_dict['on-hours'] = False
            day_dict['start_hours'] = None
            day_dict['end_hours'] = None

        calander.append(day_dict)



    return calander