# now we are onto the report functions 
# we will need to take the calandar data sets and then add up the monthly and return a data frame


def monthly_report(on_off_calendar, on_off_catagory, category_usage):
    

    monthly_on_off_calendar = {}
    monthly_on_off_catagory = {}
    monthly_catagory_usage = {}

    monthly_on_off = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}

    price_calendar_dict_total = on_off_calendar
    price_on_off_catagory_dict_total = on_off_catagory
    price_on_off_catagory_usage_dict_total = category_usage


    for i in range(len(on_off_calendar)):
        # there should be the same exact length of all 3 calandar types 
        on_off = on_off_calendar[i]


        for p in on_off:
            
            if p == 'date':
                continue
            
            if p == 'total_on_usage' or p == 'total_off_usage':
                #try:
                #    monthly_on_off_calendar[p] += on_off[p]
                #except:
                #    monthly_on_off_calendar[p] = on_off[p]
                continue
            

            for k in on_off[p]:
                
                try:
                    monthly_on_off_calendar[p][k] += on_off[p][k]
                    monthly_on_off_calendar[p][k] 
                except:
                    monthly_on_off_calendar[p] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
                    monthly_on_off_calendar[p][k] = on_off[p][k]
    
        
        
        price_on_off_catagory_dict = price_on_off_catagory_dict_total[i]

        for o in price_on_off_catagory_dict:

            
            if o == 'date':
                continue
            for h in price_on_off_catagory_dict[o]:

                monthly_on_off[h] += price_on_off_catagory_dict[o][h]

                try:
                    monthly_on_off_catagory[o][h] += price_on_off_catagory_dict[o][h]

                except:
                    monthly_on_off_catagory[o] = {'on-usage': 0, 'off-usage': 0, 'always-on': 0}
                    monthly_on_off_catagory[o][h] = price_on_off_catagory_dict[o][h]
                

        
        price_on_off_catagory_usage_dict = price_on_off_catagory_usage_dict_total[i]

        for g in price_on_off_catagory_usage_dict:
            if g == 'date':
                continue
        
            try:
                monthly_catagory_usage[g] += price_on_off_catagory_usage_dict[g]

            except:
                
                monthly_catagory_usage[g] = price_on_off_catagory_usage_dict[g]

            
    
    return monthly_on_off_calendar, monthly_on_off_catagory, monthly_catagory_usage, monthly_on_off