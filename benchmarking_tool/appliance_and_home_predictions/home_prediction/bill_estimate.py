'''
output file for calculations

    runs checks and decides what to asssume and what is already input 

    this is the first thing ran after the survey is done by the user 

'''
from .assumptions import *
from .calculations import * 
from .home import home_model
from datetime import datetime
# input is a home the home has to have a minimum of year built and square footage
# date is a list of day/month/year all integers eg: [16,5,2021]
def bill_estimate(home, date, w, daylight):
    # static values that should be inputs 
    #weather = [-30, -11, -7, 4.2, 26, 14.5, 20, 22, 15.5, 3.5, -5, -20]
    # this is actual average sedgwick data of averages
    if w == None:
        weather = [-14,-10.9,-5.1,4.5,10.5,14.8,17.1,16,13.7,3.3,-5.6,-10]
    else:
        weather = w
    '''
    this is used for calculating the heating input from sunlight on the longer days from 
    https://weather-and-climate.com/average-monthly-hours-Sunshine,edmonton,Canada
    '''

    if daylight == None:
        daylight_hours = [100,120,190,240,285,283,305,280,200,180,100,80]
    else:
        daylight_hours  = daylight

    outside_temp = weather[date[1]-1]

    daylight = daylight_hours[date[1]-1]//30.5

    sunlight_month = daylight_hours[date[1]-1]
    

    if home.furnace_set == None:
        home.furnace_set_assume = True
        home.furnace_set = 22

    if date == None:
        today = datetime.today()
        date = [today.day, today.month, today.years]



    if home.total_sqrf == None:
        return print('Home does not have a square footage value')
    if home.year_built == None:
        return print('Home does not have a year built value')


    # to estimate roof size we need the number of stories of the building

    if home.stories == None:
        home.stories = predict_stories(home.total_sqrf) 
        home.stories_assume = True
    
    # we have to try and make all of our assumptions based on the questions that where ot answered 
    if home.furnace_BTU == None and home.furnace_eff == None:
        [BTU, eff] = furnace_predict(home.total_sqrf, home.year_built, home.windows_upgrade, home.wall_upgrade, home.roof_upgrade)
        home.furnace_BTU = BTU
        home.furnace_eff = eff
        home.furnace_assume = True

    if home.window_sqrf == None:
        home.window_sqrf = window_sqrf(home.total_sqrf)
        home.window_sqrf_assume = True

    if home.roof_sqrf == None:
        home.roof_sqrf = roof_sqrf(home.total_sqrf, home.stories)
        home.roof_sqrf_assume = True

    if home.wall_sqrf == None:
        home.wall_sqrf = wall_sqrf(home.total_sqrf, home.stories)
        home.wall_sqrf_assume = True

    # get R values of the walls windows and roof
    # the second value is a 
    # the first value is the year of upgraded
    #   we may need to change the way that the we get this value
    if home.wall_R == None:
        [home.wall_R, home.wall] = wall_R_assignmnet(None, home.year_built)
        home.wall_r_assume = True
        home.wall_assume = True

    if home.roof_R == None:
        home.roof_R = roof_R_assignmnet(None, home.year_built)
        home.roof_r_assume = True

    if home.windows_R == None:
        [home.windows_R, home.windows] = windows_R_assignment(None, home.year_built)
        home.window_r_assume = True
        home.window_assume = True
    
    # calculate heat loss 
    # we need to know what they set the thermostat too
    # we should change how weather is input to the functions
    # need the amount of energy input by the sunlight and the windows
    #   this is a very rough calculation and is mostly used in the summer months 

    home.solar_heat_gain = heat_gain_sun(sunlight_month, home.window_sqrf,)

    home.wall_heat_loss = heat_loss(outside_temp, home.furnace_set, home.wall_R , home.wall_sqrf)

    home.window_heat_loss = heat_loss(outside_temp, home.furnace_set, home.windows_R, home.window_sqrf)
    
    home.roof_heat_loss = heat_loss(outside_temp, home.furnace_set, home.roof_R, home.roof_sqrf)

    home.total_heat_loss_1 = home.roof_heat_loss + home.window_heat_loss + home.wall_heat_loss

    home.total_heat_loss = home.total_heat_loss_1 - home.solar_heat_gain
    
    home.furnace_energy_input = heat_energy_input(home.total_heat_loss, outside_temp, home.furnace_eff)

    # have to calculate hot water stuff now 

    # water is dependent on the amount of people in the house
    if home.residence == None:
        home.residence = resident_pretict(home.total_sqrf)
        home.residence_assume = True

    if home.hotwater_use_per_person == None:
        # 16.4977 gallons is the average amount of hot water a person uses in a day 
        home.hotwater_use_per_person = 16.4977
        home.hotwater_use_per_person_assume = True

    if home.hotwater_tank_size == None:
        tank_use = hotwater_tank_predict(home.hotwater_use_per_person, home.residence, home.year_built)
        home.hotwater_tank_size = tank_use[0]
        home.hotwater_tank_assume = True

    if home.hotwater_per_day == None:
        tank_use = hotwater_tank_predict(home.hotwater_use_per_person, home.residence, home.year_built)
        home.hotwater_per_day = tank_use[1]

    

    if home.hotwater_eff == None:
        tank_use = hotwater_tank_predict(home.hotwater_use_per_person, home.residence, home.year_built)
        home.hotwater_eff= tank_use[3]
    
    if home.hotwater_fuel == None:
        home.hotwater_fuel = "gas"
        home.hotwater_fuel_assume = True
    # what is the incoming water tempuerature and what is the tempurature of the 
    home.hotwater_energy = water_energy_input(home.hotwater_use_per_person, home.incoming_water_temp, home.hotwater_temp_set, home.hotwater_eff)


    if home.hotwater_fuel == 'gas':
        home.total_gas = home.hotwater_energy + home.furnace_energy_input
    else:
        home.total_gas = home.furnace_energy_input

    # electrical loads 

    # lights 

    # we will also need to make a daylight function based on weather

    #daylight = 7 # hours calculated at top

    # lights are calculated on lumens per squarefoot -> 20 lumens per square foot 
    home.lights_kwh_month = lighting_energy(home.total_sqrf, home.lights, home.lumen_watts, daylight)


    # fridge energy
    # energy consumption is based on the age of the fridge
    #   there is lots on fridge stuff but it is hard to predict right now maybe imaje rec could get better

    if home.fridge_age == None: # ask use last time their firdge was replaced
        home.fridge_age = fridge_predict(home.year_built)
        home.fridge_age_assumption = True

    if home.fridge_day_kwh == None:
        home.fridge_day_kwh = 1.5
        home.fridge_day_kwh_assume = True

    # 6.44kwh this is a average usage of a fridgeg in a day 
    # should multiply this by the exact amount of days in the month but for now we are keeping it at 30.5 days in a month

    if home.fridge_kwh_month == None:
        kwh_month = home.fridge_day_kwh * 30.5

        home.fridge_kwh_month = fridge_energy(home.fridge_age, kwh_month)


    # washer and dryer variables 

    # washer_predict and dryer_predict just retrurn a number 
    # washer_w = 750 watts
    # dryer_w = 3000 watts
    if home.washer_w == None:
        home.washer_w = washer_predict(home.year_built)
        home.washer_assume = True

    if home.dryer_w == None:
        home.dryer_w = dryer_predict(home.year_built)
        home.dryer_assume = True

    if home.laundry_loads_per_month == None:
        # we are assuming that the average person does 1.2 loads of laundry a week 
        home.laundry_loads_per_month = home.residence * 4.8
        home.laundry_loads_assume = True

    
    home.washer_kwh_month = washer_energy(home.washer_w, home.laundry_loads_per_month)

    home.dryer_kwh_month = dryer_energy(home.dryer_w , home.laundry_loads_per_month)

    # oven kwh
    # to get oven kwh we need to now some behaviors, we could ask in servey or assume
    if home.cook_time_oven == None:
        '''
        how long is the oven on?

        probably 4 times a week for around 1.5 hours 

        so total 12 * 1.5 = 18 hours a month 
        '''
        home.cook_time_oven = 18 # hours in a month
        home.cook_time_oven_assume = True

    # oven wattage
    if home.oven_w == None: 
        home.oven_w = 2300 # wattage of a average oven 
        home.oven_assume = True

    home.oven_kwh_month = oven_energy(home.cook_time_oven,home.oven_w)

    # stove kwh
    if home.cook_time_stove == None:
        home.cook_time_stove = 12 # hours in a month
        home.cook_time_stove_assume = True

    if home.stove_w == None:
        home.stove_w = 1200 # watts
        home.stove_assume = True

    home.stove_kwh_month = stove_energy(home.cook_time_stove,home.stove_w)

    # microwave kwh

    if home.cook_time_microwave == None:
        home.cook_time_microwave = 2 # hours in a month
        home.cook_time_microwave_assume = True

    if home.microwave_w == None:
        home.microwave_w = 1000 # watts

    home.microwave_kwh_month = microwave_energy(home.cook_time_microwave,home.microwave_w)
    
    # dishwasher KWH usage 
    # the dishwasher is a list of 2 things [kwh/load , gallons of water/load]

    if home.dishwasher_w == None:
        [home.dishwasher_w, home.dishwasher_water] = dishwasher_predict()
        home.dishwasher_assume = True
        
    if home.dishwasher_loads == None:
        home.dishwasher_loads = 0.589
        home.dishwasher_loads_assume = True
    
    if home.dishwasher_kwh_month == None and home.dishwasher_water_per_month == None:
        [home.dishwasher_kwh_month, home.dishwasher_water_per_month] = dishwasher_energy([home.dishwasher_w,home.dishwasher_water], home.dishwasher_loads)

    home.extra_kwh = (home.lights_kwh_month + home.fridge_kwh_month + home.oven_kwh_month + home.stove_kwh_month + home.microwave_kwh_month + home.dishwasher_kwh_month + home.washer_kwh_month + home.dryer_kwh_month)* 0.15
    
    if home.hotwater_fuel == 'electric':
        #convert the btu to kwh
        home.hotwater_energy = home.hotwater_energy * 0.000293071
        home.extra_kwh = home.extra_kwh + home.hotwater_energy

    home.total_kwh = home.lights_kwh_month + home.fridge_kwh_month + home.oven_kwh_month + home.stove_kwh_month + home.microwave_kwh_month + home.dishwasher_kwh_month + home.washer_kwh_month + home.dryer_kwh_month + home.extra_kwh

    # return a range of 30% 

    home.total_gas = home.total_gas*0.0000010551

    r_kwh = home.total_kwh * 0.10

    r_gas = home.total_gas * 0.10

    kwh_range = [home.total_kwh - r_kwh , home.total_kwh + r_kwh, home.total_kwh]

    gas_range = [(home.total_gas - r_gas) , (home.total_gas + r_gas), home.total_gas]

    home.range_gj = gas_range
    home.range_kwh = kwh_range

    return




