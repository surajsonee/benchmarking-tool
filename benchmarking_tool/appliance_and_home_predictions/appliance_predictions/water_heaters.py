import copy
import pandas as pd
import numpy as np
from home_prediction import bill_estimate
from .get_ghg import get_ghg

def water_heaters(user_kwh, user_gj, user_home, date, weather, daylight):
    home_copy = copy.copy(user_home)
    get_water = pd.read_csv('energy_star/water_heaters/ENERGY_STAR_Certified_Water_Heaters.csv')

    water_array = get_water.to_numpy()
    output = [dict() for _ in range(len(water_array))]
    count = 0
    d_dict = {}

    for water in water_array:
        d_dict = {}
        d_dict['brand'] = water[2]
        d_dict['model'] = water[3]
        d_dict['model number'] = water[4]
        fuel = water[7]
        d_dict['fuel'] = water[7]
        storage = water[9]
        input_rate = water[18]
        uniform_energy_factor = water[19]
        if fuel == 'Propane, Natural Gas' or fuel == 'Natural Gas' or fuel == 'Propane':
            fuel = 'gas'
        if fuel == 'Electric':
            fuel = 'electric'
            
        home_copy.hotwater_eff = float(uniform_energy_factor)
        home_copy.hotwater_fuel = fuel
        
        bill_estimate(home_copy,date,weather,daylight)
        
        bill_estimate(user_home,date,weather,daylight)
        
        
        gas_s = user_home.total_gas - home_copy.total_gas
            
        
        elec_s = user_home.total_kwh - home_copy.total_kwh

        d_dict['electrical savings(kwh/month)'] = elec_s

        d_dict['gas savings(GJ/month)'] = gas_s
        

        ghg_savings = get_ghg(elec_s, gas_s)
        d_dict['green house gas savings(lbs of co2)'] = ghg_savings[0] + ghg_savings[1]

        output[count] = d_dict
        count += 1

    return output