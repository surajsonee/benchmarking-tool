import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg

def me_windows(user_gj, user_home,date, weather, daylight):
    home_copy = copy.copy(user_home)
    get_windows = pd.read_csv('energy_star/building_products/ME_Windows.csv')

    windows_array = get_windows.to_numpy()
    output = [dict() for _ in range(len(windows_array))]
    count = 0
    w_dict = {}

    for window in windows_array:
        w_dict = {}
        w_dict['brand'] = window[0]
        w_dict['model'] = window[2]
        
        min_u = float(window[6])
        max_u = float(window[7])
        ave_u = (min_u + max_u) / 2
        new_r = 1/ave_u

        home_copy.windows_R = new_r
        
        bill_estimate(user_home,date,weather,daylight)
        
        bill_estimate(home_copy,date,weather,daylight)
        
        savings = user_home.total_gas - home_copy.total_gas
        
        w_dict['energy_savings(GJ/month)'] = savings

        ghg_savings = get_ghg(savings, savings)
        w_dict['green house gas savings(lbs of co2)'] = ghg_savings[1]

        output[count] = w_dict
        count += 1

    return output