# we have to get the last week usage to get a actual data 
import datetime 
import numpy as np
def last_week_usage(data):

    
    channel_dict = {}
    dates_processed = []

    last_week_dates = []

    for dates in data:
        data_day = dates[0]
            
        dates_processed.append(data_day)

    # have to get the newest date and then go a week back from that 

    latest_date = max(dates_processed)

    last_week_day = latest_date - datetime.timedelta(days=7)

    last_monday = last_week_day - datetime.timedelta(days=last_week_day.weekday())
    coming_monday = last_week_day + datetime.timedelta(days=-last_week_day.weekday(), weeks=1)


    for data_all in data:
        
        try: 
            # make sure that the data is in a date format 
            data_day = data_all[0]
        
            weekday = data_day.weekday()

            channel_names = data_all[1::3]
            
            scheduals = data_all[3::3]
            
        except:
            print('Error: data is not the right format')
            return

        
        
        if data_day >= last_monday and data_day < coming_monday:

            last_week_dates.append(data_day)
            
            for i in range(len(scheduals)):
                channel_name = channel_names[i]
               
                
                # get the sqedual into a numpy array 

                u = scheduals[i]
                
                u_list = u.strip('][').split(',')
                #print(u_list)
                u_list_float = np.zeros(24) 

                #u_list_float = [float(x) for x in u_list]

                # turn the 24 hour usage list in to numpy array
                for x in range(24): 
                    try:
                        u_list_float[x] = float(u_list[x])/1000
                    except:
                        continue
                
                #check to see if the channel name is already in the return dict
                
                if channel_name not in channel_dict.keys():
                    # It is not in the dict then we have to init a dict of days and lists 
                    
                    
                    #weekday_dict = dict.fromkeys(range(7),[])

                    weekday_dict = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

                    channel_dict[channel_name] = weekday_dict

                    channel_dict[channel_name][weekday].append(u_list_float)
                
                else:

                    channel_dict[channel_name][weekday].append(u_list_float)
            
    
    return channel_dict, last_week_dates