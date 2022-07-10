
from home_prediction import * 
from appliance_predictions import *

home = home_model(1996, 1500)

hello = bill_estimate(home,[5,5,2021],None,None)

savings1 = clothes_dryer(home.total_kwh, home,[5,5,2021],None,None)

savings2 = clothes_washer(home.total_kwh, home,[5,5,2021],None,None)

savings3 = dishwasher(home.total_kwh, home,[5,5,2021],None,None)

savings4 = refrigerator(home.total_kwh, home,[5,5,2021],None,None)

savings5 = me_windows(home.total_gas, home,[5,5,2021],None,None)

savings6 = furnace(home.total_gas, home,[5,5,2021],None,None)

savings7 = light_bulbs(home.total_kwh, home,[5,5,2021],None,None)

savings8 = water_heaters(home.total_kwh,home.total_gas, home,[5,5,2021],None,None)

for i in savings8:
    print(i)


