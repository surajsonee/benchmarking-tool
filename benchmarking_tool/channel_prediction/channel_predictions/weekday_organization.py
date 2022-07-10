import datetime 
import numpy as np
import pandas 

# we need to organize the channel names into weekdays. 
# this will be a dictionary of dictionaries 
# outer dict will be channel names 
# inner dict will be 0-6
# each  of the 0-6 keys will have a list of lists, 24 hour of usage is each list in the list  


def weekday_organization(data): 
    channel_dict = {}
    dates_processed = []

    for data_all in data:
        
        try: 
            # make sure that the data is in a date format 
            data_day = data_all[0]

            dates_processed.append(data_day)

            weekday = data_day.weekday()

            channel_names = data_all[1::3]
            
            scheduals = data_all[3::3]
            
            

        except:
            print('Error: data is not the right format')
            return
        
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

    return channel_dict, dates_processed