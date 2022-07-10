import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg
def clothes_washer(user_kwh,user_home, date, weather, daylight):
    home_copy = copy.copy(user_home)
    get_washer = pd.read_csv('energy_star/appliances/ENERGY_STAR_Certified_Residential_Clothes_Washers.csv')

    washer_array = get_washer.to_numpy()
    output = [dict() for _ in range(len(washer_array))]
    count = 0
    w_dict = {}

    for washer in washer_array:
        w_dict = {}
        w_dict['brand'] = washer[1]
        w_dict['model'] = washer[2]
        imef = washer[9]
        drum_capacity = washer[8]
        anual_energy = washer[14]

        # washer is used to 
        kwh_per_load = float(drum_capacity)/float(imef)
        
        washer_watts = (1000 * kwh_per_load)/1
       
        
        home_copy.washer_w = washer_watts

        home_copy.washer_kwh_month = home_copy.laundry_loads_per_month * kwh_per_load
        
        
        
        bill_estimate(user_home,date,weather,daylight)

        home_copy.washer_kwh_month = user_home.laundry_loads_per_month * kwh_per_load

        bill_estimate(home_copy,date,weather,daylight)

        savings = user_home.total_kwh - home_copy.total_kwh

        w_dict['energy_savings(kwh/month)'] = savings

        ghg_savings = get_ghg(savings, 4)
        w_dict['green house gas savings(lbs of co2)'] = ghg_savings[0]

        output[count] = w_dict
        count += 1

    return output