# shows the total hourly usage over a entire month in a single list 


def monthly_hour_usage(calendar_dict, data):
    return_calender = []

    try:
        if len(data) != len(calendar_dict):
            print('Error: data and calandar length are not the same')
         
    except:
        print('Error: data and/or calandar are not the right data form')
        return 


    for data_all in data:
        
        try: 
            # make sure that the data is in a date format 
            data_day = data_all[0]

            #new_date = UTC_timezone(data_day,location)
            d_day = data_day.day
            d_month = data_day.month

            channel_names = data_all[1::3]
            total_usage = data_all[2::3]
            scheduals = data_all[3::3]

        except:
            print('Error: data is not the right format')
            return

        for calendar_day in calendar_dict:
            calendar_date = calendar_day['day']
            if d_day == calendar_date.day and d_month == calendar_date.month:
                
                # get the start hour and end hour
                start_hour = calendar_day['start_hours']
                end_hour = calendar_day['end_hours']


                # get on hours and off hours usage 
                # whle looping through the schedual lists 

                total_on_usage = []  
                total_off_usage = []
                always_on = 0
                r_dict = {}
             
                r_dict['date'] = calendar_date
                for l in range(len(scheduals)):
                    u = scheduals[l]
                    u_list = u.strip('][').split(',')
                    u_list_float = [float(x) for x in u_list]

                    c_name = channel_names[l]
                    r_dict[c_name] = {}

                    off_usage_schedual = []
                    on_usage_schedual = []

                    for h in range(24):

                        if u_list_float[h] != u_list_float[h]:
                            u_list_float[h] = 0.0

                        if calendar_day['on-hours'] == False:# and start_hour == None and end_hour == None:
                                # this is if it is a weekend were the facility is off
                                off_usage_schedual.append(u_list_float[h]/1000)
                                on_usage_schedual.append(0.0)
                                total_off_usage.append(u_list_float[h]/1000)
                                total_on_usage.append(0.0)
                                
                                continue
                        # we have to go through the hours in the schedual list to see if the hours are lined up. 
                        if h >= start_hour and h <= end_hour:
                            on_usage_schedual.append(u_list_float[h]/1000)
                            off_usage_schedual.append(0.0)
                            total_off_usage.append(0.0)
                            total_on_usage.append(u_list_float[h]/1000)
                            

                        else:
                            off_usage_schedual.append(u_list_float[h]/1000)
                            on_usage_schedual.append(0.0)
                            total_off_usage.append(u_list_float[h]/1000)
                            total_on_usage.append(0.0) 

                    r_dict[c_name]['on-usage'] = on_usage_schedual
                    r_dict[c_name]['off-usage'] = off_usage_schedual
                
                
                return_calender.append(r_dict)

            else: 
                continue
    last_dict = {'total_on_usage': total_on_usage, 'total_off_usage':total_off_usage}

    return_calender.append(last_dict)
            
    return return_calender