#takes the home class and then computes calculations with parameters
# calcs are based on 2002 ASHRE guidliines 2002 
# calc page that is usful https://www.e-education.psu.edu/egee102/node/2067
#from home import home_model
#from assumptions import *
from datetime import datetime


# great source for calculating this: https://www.nrcan.gc.ca/energy/efficiency/housing/new-homes/energy-starr-new-homes-standard/tables-calculating-effective-thermal-resistance-opaque-assemblies/14176#a52



def heat_loss(outside_temp, inside_temp, R_value, sqrf):
    #heat loss hourly = (areasqrft * temp difference(F))/(Rvalue)
    #heat loss in a day = heat loss hourly X 24
    #heat loss in a full heating season = ((area)/R-value)*24*HDD
    #HDD = Heating Degree Days (different for all months and value on weather)
    '''
    #if ther user has not inputed their furnace set then 
    if home.furnace_set == None:

        inside_temp = 22
    
    if home.wall_R == None:

        home.wall_R = wall_R_assignmnet(home.year_built, home)

    if home.wall_sqrf == None:

        home.wall_sqrf = wall_sqrf(home)


    print(home.wall_sqrf)
    print(temp_diff_f)
    print(home.wall_R)
    ''' 

    #have to convert temp difference to F
    temp_diff_c = inside_temp - outside_temp
    temp_diff_f = (temp_diff_c * (9/5)) + 32

    hour_heat_loss = (sqrf * temp_diff_f)/R_value

    day_heat_loss = hour_heat_loss * 24

    monthly_heat_loss = day_heat_loss * 30.5   

    #home.wall_heat_loss = monthly_heat_loss

    if outside_temp > inside_temp:
        monthly_heat_loss/2

    return monthly_heat_loss

def heat_gain_sun(sunlight, window_sqrf):
    # this calculates the amount of BTUs more the sun will add to the house 
    # sun generates 316.998 BTU/sqrfoot/hour sourece : http://www.yourturn.ca/solar/solar-power/how-much-power-does-the-sun-give-us/

    windows_size = window_sqrf * 0.20 # say 30% of windows on the house are facing the right way 

    energy = windows_size * sunlight * 316.998
    # this 0.8 is the glazing of the window, in canada windows are not glazed a lot so that we get more heat in in the colder months 
    return energy * 0.8


def heat_energy_input(heat_loss, ave_temp, furnace_eff):
    # take the furnace heating input 
    # we know the heating loss in total_hl. we then take that as the total heating needed from the furnace
    # take the efficiency of the furnace and then add the precentage opposite of the furnace 
    
    total_energy = heat_loss * (1 + (1 - furnace_eff))

    return total_energy # total energy in BTU

def water_energy_input(water_use, incoming_water_temp, tank_temp_set, hotwater_eff):
    # tank is a list of 2 [tank size , daily hot water use per house]
    #we need to get the energy required for hot water
    # home.hotwater is in gallons
    '''
        Q = m * c_p * temp_difference
        m = mass of water
        C_p = the heat capacuty of water = 1 BTU/lb F
        temp_difference = start temp - desired temp

        Q = BTU/day

        1 kWh = 3,412 BTU

    '''
    #if home.hotwater == None:
    #    home.hotwater = hot_water_tank_predict(home)
    #if home.residence == None:
    #    home.residence = resident_pretict(home)

    #if home.hotwater_perday == None:# this is predicted in hot water tank prediction but if that is not ran it will then be here. 
        # could do a seperate survey to calculate this number  better 
    #    home.hotewater_perday = home.residence * 16.4877

    # we need to get total days in the current month 
    #now = datetime.datetime.now()
    #days_month = calendar.monthrange(now.year, now.month)[1]

    #water usage in gallons
    # 30.5 is days in the month
    hot_water_usage = 30.5 * water_use
    
    # we need the incoming water temp of the city the user is in. UPDATE
    # not sure how to get this going to make a assumption 
    # i am saying 10.5C (50.9F) cus thats what it was in my house on march 31 2021
    # standard hot water temp is 60C (140F)

    temp_difference = tank_temp_set - incoming_water_temp

    # what is the mass of the water? in pounds 
    # around 8.33 pounds of water in a galon 

    pounds_of_water =  hot_water_usage * 8.33

    # how much energy does it take to heat up this much hot water?

    Q = pounds_of_water * temp_difference * 1 

    # Q is the total BTu needed to heat up the amound of water that the user is using 

    energy = Q * (1 + (1 - hotwater_eff))

    return energy

# electrical loads 

def lighting_energy(square_foot, lights_type, lumen_watts, daylight) :
    # we will probably need to make this more accuarate 
    '''
    https://www.alconlighting.com/blog/residential-led-lighting/how-do-i-determine-how-many-led-lumens-i-need-for-a-space/#:~:text=To%20determine%20the%20needed%20lumens,will%20need%203%2C000%2D4%2C000%20lumens.
    calculate lumens per square foot 
        average house needs about 20 lumens per square foot
    '''
    total_lumens = square_foot * 20


    '''
    https://www.any-lamp.com/lumen-to-watt
    different bulbs have different lummen values per watt
        4 types of light bulbs we will be calculating 

        type                lumen/watts
        incandesent         10
        halogen             12
        CFL                 50
        LED                 75
    '''
    if lumen_watts == None:
        if lights_type == None: # ask the user what light bulbs that they use 
            lights_type = 'CFL'

        if lights_type == 'incandesent':
            lumen_per_watt = 10
        
        elif lights_type == 'halogen':
            lumen_per_watt = 12

        elif lights_type == 'CFL':
            lumen_per_watt = 50
        
        elif lights_type == 'LED':
            lumen_per_watt = 75

        else:
            lumen_per_watt = 30
    else:
        lumen_per_watt = lumen_watts

    # we then get the wattage taken to light the house 

    total_watts = (1/lumen_per_watt) * total_lumens

    # how many hours are the lights on per month?
    # this can change and be more detailed in  UPDATES 
    # we will say lights are on from 6pm - 11pm and 7am - 9am so 7 hours a day

    hours = daylight

    # energy in kWh
    energy = (total_watts * hours)/1000

    # now not all lights are on at all parts of the house at all times 
    # we will take a 30% reduction on this number 

    energy_reduced = energy - (energy * .3)

    return energy_reduced

def fridge_energy(fridge_age, kwh_month):
    # a fridge lasts anywhere from 10-18 years we will assume 18 years 
    # we need the age of a fridge because fridges get less efficient as time goes on 
    '''
    https://cleantechnica.com/2012/12/22/is-your-fridge-eating-your-savings/#:~:text=Does%20Age%20Matter%3F,at%20least%2030%25%20more%20energy.
    As a fridge gets older they become less efficient we also have a average fridge efficiency and average usage 


    https://paylesspower.com/blog/how-many-watts-does-a-refrigerator-use/#:~:text=Calculating%20Average%20Wattage%20for%20Refrigerators&text=Older%20refrigerators%20typically%20use%20115,150%2Dwatt%20hours%2Fday.
    the average fridge uses around 805 watt-hours a day. with 8 hours of usage so 6440 watts per dat or 6.44 kWh
    fridge is usually around 

    fridges are quite efficient on their own but lose it over time, we will say new fridges are a 95% efficient the leaks come from the insulation and door opening 
    to get a true fridge efficiency you need: Refrigerator Efficiency = Volume Cooled (ft3) / Unit Electrical Energy per day (KWh)

    '''
    if fridge_age <= 5:
        # fridge is new and still as efficient it was at the start of the day. 
        multi = 1
    if fridge_age > 5 and fridge_age <= 10:
        # older fridge uses 10% more energy
        multi = 1.1

    if fridge_age > 10 and fridge_age <= 15:
        # older fridge uses 20% more energy
        multi = 1.2

    if fridge_age > 15:
        # older fridge uses 30% more energy
        # probabkly should get a new fridge
        multi = 1.3
    
    fridge_energy = kwh_month * multi

    return fridge_energy

def washer_energy(washer_w, loads_per_month):
    '''
    source: https://blog.arcadia.com/electricity-costs-10-key-household-products/

    we are going to say 1.2 loads of laundry per week per person so 4.8 

    washers 
        efficient washers only need about 500 wattts per hour average run time of 30 min
        energy star models average around 500 watts per hour so we will then assume the wattage to be 750
    '''
    # a washer takes about 55 min
    hours = loads_per_month * 0.9166

    total_w = hours * washer_w

    return total_w/1000

def dryer_energy(dryer_w , loads_per_month):
    '''
    dryers
        dryers take around 3000 watts per hour average runtime of 45 min
        ENERGY STAR does not rate dryers because their efficiency has been about the same for years 
    '''

    
    #loads_per_month

    # a dryer takes about a 45 min
    hours = loads_per_month * 0.75

    total_w = hours * dryer_w

    return total_w/1000


def oven_energy(t, oven_w):
    # t is the time used 
    '''
    https://www.siliconvalleypower.com/residents/save-energy/appliance-energy-use-chart
    oven uses about 2.3 kWh per hour 

    how long is the oven on?

        probably 4 times a week for around 1.5 hours 

        so total 12 * 1.5 = 18 hours a month 


    we can make this assumption now and change it later 
    '''
    total_kwh = oven_w * t

    return total_kwh/1000


def stove_energy(t , stove_w): 
    # t is the time used 
    '''
    https://www.siliconvalleypower.com/residents/save-energy/appliance-energy-use-chart

    we are assuming that it is electric for now but could be gas

    says oven surface uses about 1-1.5 kwh per hour 


    how much do people use the cook top?
        people probably less then their oven 

    '''

    total_kwh = stove_w * t
    
    return total_kwh/1000

def microwave_energy(t , micro_w): 

    total_kwh = micro_w * t
    
    return total_kwh/1000

def dishwasher_energy(dishwasher, loads_per_day):
    '''
    source:

    https://www.directenergy.com/learning-center/how-much-energy-dishwasher-use#:~:text=A%20dishwasher's%20base%20electricity%20usage,cent%20per%20kWh%20electricity%20plan.

    how much energy does a dishwasher use and water 

    a 1994 dishwasher useing 10 gallons per load and 1.27 kwh

    older energystar dishwashers useing 5 gallons and need 0.64 kwh

    a new energy star dishwasher 3.2 gallons per load and only 0.38 kwh

    '''
    # dishwahser is a list of 2 [kwh, gallons of water]
    # how man loads of dishes to the average people do?
    # around 1 per day or 215 loads in a year. 
    # we will say 0.589 loads per day 
    # loads take about 1.5 hours

    loads_per_month = loads_per_day * 30.5 
    kwh = (loads_per_month * 1.5) * dishwasher[0]
    water = loads_per_month * dishwasher[1]

    return [kwh, water]

    