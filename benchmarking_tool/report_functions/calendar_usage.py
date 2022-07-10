# this function will take the results from the sql call and the calander and put in on hours usage and off hours usage 
# location is the city where the building is. if it is not found it will default to edmonton 
# the schedual list is already in number 0-24 for that day it is processed before deposited into the database 
def calendar_usage(calendar_dict, data):
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

                total_on_usage = 0
                total_off_usage = 0
                always_on = 0
                r_dict = {}
             
                r_dict['date'] = calendar_date
                for l in range(len(scheduals)):
                    u = scheduals[l]
                    u_list = u.strip('][').split(',')
                    u_list_float = [float(x) for x in u_list]

                    c_name = channel_names[l]
                    r_dict[c_name] = {}


                    off_usage = 0
                    on_usage = 0
                    
                    temp_always_on = 0
                    # check for always on
                    a_o = True
                    for hour in range(24):
                        if u_list_float[hour] != u_list_float[hour]:
                            u_list_float[hour] = 0.0
                        
                        if u_list_float[hour] != 0 or u_list_float[hour] != 0.0: 
                            temp_always_on += u_list_float[hour]/1000
                        else:
                            a_o = False
                            temp_always_on = 0
                        
                    if a_o == True:

                        always_on += temp_always_on
                        r_dict[c_name]['always-on'] = round(always_on,2)
                        
                        continue



                    for h in range(24):
                        #print(u_list_float[h])
                        #print(type(u_list_float[h]))
                        if u_list_float[h] != u_list_float[h]:
                            u_list_float[h] = 0.0

                        if calendar_day['on-hours'] == False:# and start_hour == None and end_hour == None:
                                # this is if it is a weekday were the facility is off
                                off_usage += u_list_float[h]/1000
                                total_off_usage += u_list_float[h]/1000
                                
                                continue
                        # we have to go through the hours in the schedual list to see if the hours are lined up. 
                        if h >= start_hour and h <= end_hour:
                            on_usage += u_list_float[h]/1000
                            total_on_usage += u_list_float[h]/1000
                            

                        else:
                            off_usage += u_list_float[h]/1000
                            total_off_usage += u_list_float[h]/1000
                            

                    

                    r_dict[c_name]['on-usage'] = round(on_usage,2)
                    r_dict[c_name]['off-usage'] = round(off_usage,2)
                
                r_dict['total_on_usage'] = round(total_on_usage,2)
                r_dict['total_off_usage'] = round(total_off_usage,2)
                
                return_calender.append(r_dict)

            else: 
                continue

    return return_calender