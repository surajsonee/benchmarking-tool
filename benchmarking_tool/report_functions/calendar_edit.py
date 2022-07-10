# making a function that changes hours of the calandar 

# can accept multiple types of dates. 
# date time type of datetime.date(2021,8,18) or a list [2021,8,18]

def calendar_edit(calendar, date_change, start_hour, end_hour):

    new_calendar = calendar

    # we need to check if the date_change is of a date time type
    day = None
    try: 
        day = date_change.day
        month = date_change.month
        year = date_change.year
    except:
        pass

    try:
        day = date_change[2]
        month = date_change[1]
        year = date_change[0]
    except:
        pass

    for d in new_calendar:
        cal_day = d['day']

        if cal_day.day == day and cal_day.month == month and cal_day.year == year:
            if d['on-hours'] == False:
                d['on-hours'] = True
            
            d['start_hours'] = start_hour
            d['end_hours'] = end_hour

    return new_calendar