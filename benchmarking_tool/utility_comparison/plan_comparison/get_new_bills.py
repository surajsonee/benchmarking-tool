# this function take in the city, user kwh, user gj, and the database and returns a list of comparison lists 
from .electrical_comparison import electrical_comparison
from .gas_comparison import gas_comparison
from .bundle_comparison import bundle_comparison
#from sub_pkg import electrical_comparison, gas_comparison, bundle_comparison

import pandas as pd
import numpy as np
import sqlite3

def get_new_bills(db_string, city, user_kwh, user_gj):
    cnx = sqlite3.connect(db_string)

    df = pd.read_sql_query("SELECT * FROM usahelps_alberta", cnx)
    city_c = city.capitalize()

    try:
        df_city = df.loc[df['City'] == city_c]
    except:
        print("Do not have that city in our database")
        return 
    elec_df = df_city.loc[df['utility_type'] == 'Electricity']
    gas_df = df_city.loc[df['utility_type'] == 'Natural Gas']
    bundle_df = df_city.loc[df['utility_type'] == 'Bundeled']

    
    elec_bills = electrical_comparison(elec_df, user_kwh)
    gas_bills = gas_comparison(gas_df, user_gj)
    bundle_bills = bundle_comparison(bundle_df, user_gj, user_kwh)

    return [elec_bills, gas_bills, bundle_bills]



def print_bills(bill_list):
    elec = bill_list[0]
    gas = bill_list[1]
    bundle = bill_list[2]

    print('electrical bills')
    for plan in elec:
        for deet in plan: 
            print('{}: {}'.format(deet, plan[deet]))
        print('---------------------------------')
    
    print('gas bills')
    for plan in gas:
        for deet in plan: 
            print('{}: {}'.format(deet, plan[deet]))
        print('---------------------------------')
    
    print('bundle bills')
    for plan in bundle:
        for deet in plan: 
            print('{}: {}'.format(deet, plan[deet]))
        print('---------------------------------')

