# we need to get all the types of calandars into a price type. 
import pandas as pd 

def kwh_price(price_kwh, on_off_calendar, on_off_catagory, category_usage):
    wh_to_price = price_kwh

    price_calendar = []
    price_on_off_catagory = []
    price_on_off_catagory_usage = []

    price_calendar_dict_total = on_off_calendar
    price_on_off_catagory_dict_total = on_off_catagory
    price_on_off_catagory_usage_dict_total = category_usage


    for i in range(len(on_off_calendar)):
        # there should be the same exact length of all 3 calandar types 
        price_calendar_dict = price_calendar_dict_total[i]

        for p in price_calendar_dict:
            
            if p == 'date':
                continue

            if p == 'total_on_usage' or p == 'total_off_usage':
                price_calendar_dict[p] *= wh_to_price
                continue

            for k in price_calendar_dict[p]:
                price_calendar_dict[p][k] *= wh_to_price
                
        price_on_off_catagory_dict = price_on_off_catagory_dict_total[i]

        for o in price_on_off_catagory_dict:
            
            if o == 'date':
                continue
            for h in price_on_off_catagory_dict[o]:
                #print(price_on_off_catagory_dict[o])
                #print(price_on_off_catagory_dict[o][h])
                price_on_off_catagory_dict[o][h] *= wh_to_price


        price_on_off_catagory_usage_dict = price_on_off_catagory_usage_dict_total[i]

        for g in price_on_off_catagory_usage_dict:
            if g == 'date':
                continue
            
            price_on_off_catagory_usage_dict[g] *= wh_to_price
        
        price_calendar.append(price_calendar_dict)
        price_on_off_catagory.append(price_on_off_catagory_dict)
        price_on_off_catagory_usage.append(price_on_off_catagory_usage_dict)
    
    return price_calendar,price_on_off_catagory,price_on_off_catagory_usage