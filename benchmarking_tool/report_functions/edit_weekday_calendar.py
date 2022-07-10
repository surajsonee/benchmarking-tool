# this is a function to edit all the weekdays in calendar with 
# weekday is a int from 0-6
def edit_weekday_calendar(calendar, weekday, start_hour, end_hour): 

    if weekday > 6 and weekday < 0:
        print("Error: edit_weekday_calendar, weekday needs to be between 0-6")
        return 

    for day in calendar:
        if day['weekday'] == weekday:
            if day['on-hours'] == False:
                day['on-hours'] = True
            day['start_hours'] = start_hour
            day['end_hours'] = end_hour

    return calendar