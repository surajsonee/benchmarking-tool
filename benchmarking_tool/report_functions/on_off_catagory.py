# we have to get on off usage by catagory 
# get this from both 

def on_off_catagory(catagory_dict, on_off_calendar):
    r_calendar = []

    for day in on_off_calendar:

        r_dict = {}
        r_dict['date'] = day['date']
        r_dict['lighting'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
        r_dict['hvac'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
        r_dict['motors_and_equipment'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
        r_dict['plug_load'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
        r_dict['hot_water'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
        r_dict['other'] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}

        # we have to go through the channel name and get it into a catagory 
        for channel  in day:
           
            if channel in catagory_dict['lighting']:
                try:
                    r_dict['lighting']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['lighting']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['lighting']['always-on'] += day[channel]['always-on']
                except:
                    pass


            elif channel in catagory_dict['hvac']:
                try:
                    r_dict['hvac']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['hvac']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['hvac']['always-on'] += day[channel]['always-on']
                except:
                    pass

            elif channel in catagory_dict['motors_and_equipment']:
                try:
                    r_dict['motors_and_equipment']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['motors_and_equipment']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['motors_and_equipment']['always-on'] += day[channel]['always-on']
                except:
                    pass

            elif channel in catagory_dict['plug_load']:
                try:
                    r_dict['plug_load']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['plug_load']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['plug_load']['always-on'] += day[channel]['always-on']
                except:
                    pass

            elif channel in catagory_dict['hot_water']:
                try:
                    r_dict['hot_water']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['hot_water']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['hot_water']['always-on'] += day[channel]['always-on']
                except:
                    pass

            else:
                try:
                    r_dict['other']['on-usage'] += day[channel]['on-usage']
                except:
                    pass
                try:
                    r_dict['other']['off-usage'] += day[channel]['off-usage']
                except:
                    pass
                try:
                    r_dict['other']['always-on'] += day[channel]['always-on']
                except:
                    pass
        r_calendar.append(r_dict)

    return r_calendar