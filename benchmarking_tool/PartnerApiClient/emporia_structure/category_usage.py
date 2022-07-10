# gets the category usage for the past 24 hours 


def category_usage(data):

    category_dict = {}
    
    hours = data.drop(columns = ['year','month','day','hour','minute'])

    channel_names = list(hours.columns)

    channel_usage = hours.sum() 

    if type(channel_usage) != float:
        for c in range(len(channel_usage)):
            new = float(channel_usage[c])
            channel_usage[c] = new

    # we need to put the names of the channels in catagories 
    # this is to init the dict 
    if category_dict == {}:
        # init the dict 
        category_dict['lighting'] = []
        category_dict['hvac'] = []
        category_dict['motors_and_equipment'] = []
        category_dict['plug_load'] = []
        category_dict['hot_water'] = []
        category_dict['other'] = []

        # we then distripute the channel names into the catagories 
        for name in channel_names:
            
            # make everything lowercase 
            name_l = name.lower()
            if 'light' in name_l or 'lights' in name_l or 'lighting' in name_l:
                category_dict['lighting'].append(name)

            elif 'hot water' in name_l or 'dhw' in name_l or 'water' in name_l or 'water heater' in name_l:
                category_dict['hot_water'].append(name)

            elif 'fan' in name_l or 'heat' in name_l or 'hvac' in name_l or 'cooling' in name_l:
                category_dict['hvac'].append(name)

            elif 'motor' in name_l or 'pump' in name_l or 'compressor' in name_l or 'vacuum' in name_l or 'dryer' in name_l:
                category_dict['motors_and_equipment'].append(name)
            
            elif 'plug' in name_l or 'plugs' in name_l or 'receptacle' in name_l or 'receptacle' in name_l:
                category_dict['plug_load'].append(name)
            
            else:
                category_dict['other'].append(name)

    # we now need to get the usage 
    r_dict = {}
    r_dict['lighting'] = 0
    r_dict['hvac'] = 0
    r_dict['motors_and_equipment'] = 0
    r_dict['plug_load'] = 0
    r_dict['hot_water'] = 0
    r_dict['other'] = 0
    r_dict['total_usage'] = 0
    r_dict['total_usage'] = sum(channel_usage)

    for i in channel_names:
        
        # check to see what catagory the channel is in. 
        if i in category_dict['lighting']:
            r_dict['lighting'] += channel_usage[i]
            

        elif i in category_dict['hot_water']:
            r_dict['hot_water'] += channel_usage[i]

        elif i in category_dict['hvac']:
            r_dict['hvac'] += channel_usage[i]

        elif i in category_dict['motors_and_equipment']:
            r_dict['motors_and_equipment'] += channel_usage[i]

        elif i in category_dict['plug_load']:
            r_dict['plug_load'] += channel_usage[i]

        else:
            r_dict['other'] += channel_usage[i]

    return r_dict, category_dict
    
    