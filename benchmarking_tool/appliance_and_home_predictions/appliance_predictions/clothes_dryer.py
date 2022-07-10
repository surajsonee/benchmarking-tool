
import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg

def clothes_dryer(user_kwh,user_home, date, weather, daylight):
    #https://www.energystar.gov/products/appliances/clothes_dryers/key_product_criteria
    # dryers are rated in different values of compact. can get kwh/load from combine energy factor
    # combine energy factor = lb/kwh
    # returns a list of dictonaries of with the keys: brand , model , energy_savings(kwh/month) , green house gas savings(lbs of co2)
    home_copy = copy.copy(user_home)
    get_dryers = pd.read_csv('energy_star/appliances/ENERGY_STAR_Certified_Residential_Clothes_Dryers.csv')

    dryer_array = get_dryers.to_numpy()
    output = [dict() for _ in range(len(dryer_array))]
    count = 0
    d_dict = {}

    for dryer in dryer_array:
        d_dict = {}
        d_dict['brand'] = dryer[1]
        d_dict['model'] = dryer[2]
        cef = dryer[13]
        drum_capacity = dryer[9]
        anual_energy = dryer[14]
        test_cycle = float(dryer[15])

        if drum_capacity >= 4.4:
            # full size so a load of 8.45lb of cloths 
            kwh_per_load = 8.45/float(cef)
        else:
            # compact dryer so a 3lb load 
            kwh_per_load = 3/float(cef)
        
        dryer_watts = (1000 * kwh_per_load)/(test_cycle/60)
        
        home_copy.dryer_w = dryer_watts
        
        bill_estimate(home_copy,date,weather,daylight)
        
        bill_estimate(user_home,date,weather,daylight)
        
        savings = user_home.total_kwh - home_copy.total_kwh

        d_dict['energy_savings(kwh/month)'] = savings

        ghg_savings = get_ghg(savings, 4)
        d_dict['green house gas savings(lbs of co2)'] = ghg_savings[0]

        output[count] = d_dict
        count += 1

    return output