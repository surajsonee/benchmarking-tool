import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg

def light_bulbs(user_kwh, user_home, date, weather, daylight):
    home_copy = copy.copy(user_home)
    get_lights = pd.read_csv('energy_star/lighting_and_fans/ENERGY_STAR_Certified__Light_Bulbs_Version_2.0.csv')

    lights_array = get_lights.to_numpy()
    output = [dict() for _ in range(len(lights_array))]
    count = 0
    d_dict = {}

    for light in lights_array:
        d_dict = {}
        d_dict['brand'] = light[1]
        d_dict['model'] = light[2]
        lumens_per_watt = float(light[18])
        
        home_copy.lumen_watts = lumens_per_watt
        
        bill_estimate(home_copy,date,weather,daylight)
        
        bill_estimate(user_home,date,weather,daylight)
        
        savings = user_home.total_kwh - home_copy.total_kwh

        d_dict['energy_savings(kwh/month)'] = savings

        ghg_savings = get_ghg(savings, 4)
        d_dict['green house gas savings(lbs of co2)'] = ghg_savings[0]

        output[count] = d_dict
        count += 1

    return output