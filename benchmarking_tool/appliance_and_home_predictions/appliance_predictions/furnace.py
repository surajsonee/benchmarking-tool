import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg
def furnace(user_gas, user_home,date, weather, daylight):
    home_copy = copy.copy(user_home)
    get_furnace = pd.read_csv('energy_star/heating_and_cooling/ENERGY_STAR_Certified_Furnaces.csv')

    furnace_array = get_furnace.to_numpy()
    output = [dict() for _ in range(len(furnace_array))]
    count = 0
    w_dict = {}

    for furnace in furnace_array:
        w_dict = {}
        w_dict['brand'] = furnace[2]
        w_dict['model'] = furnace[3]
        
        eff = float(furnace[8])/100
        
        home_copy.furnace_eff = eff
        
        bill_estimate(user_home,date,weather,daylight)
        
        bill_estimate(home_copy,date,weather,daylight)
        
        print()
        
        

        savings = user_home.total_gas - home_copy.total_gas
        
        w_dict['energy_savings(GJ/month)'] = savings

        ghg_savings = get_ghg(savings, savings)
        w_dict['green house gas savings(lbs of co2)'] = ghg_savings[1]

        output[count] = w_dict
        count += 1

    return output