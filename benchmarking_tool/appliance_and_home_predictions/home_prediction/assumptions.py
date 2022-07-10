from datetime import datetime
import numpy as np

def furnace_predict(square_footage, year_built, windows, wall, roof):
    today = datetime.today()
    current_year = today.year

    #furnaces roughly last around 15 to 30 years most being replaced around 22 year mark
    average_liftime_furnace = 30

    age = current_year - year_built 


    #furnace efficiency 
    
    number_of_furnace = age // average_liftime_furnace # this will get us the number of furnaces the house is currently on assuming that the furnace is replaced every 17 years 
    
    last_furnace_replace_year = year_built + (number_of_furnace * average_liftime_furnace)


    #the latest the furnace was replaced would be around 2000 - 2004 what was the tech of furnaces of that time?
    # basing furnace efficiency bsed on this site: https://www.fortisbc.com/news-events/stories-and-news-from-fortisbc/the-costly-truth-about-your-old-furnace

    if last_furnace_replace_year < 2010:
        efficiency_val = .76

    if (last_furnace_replace_year >= 2010) and (last_furnace_replace_year <= 2015):
        efficiency_val = .85

    if (last_furnace_replace_year > 2015):
        efficiency_val = .95

    # possibly add a rebate qualified furnace that are up to .98 efficient 


    #furnace size
    '''
    source: https://airforceheating.com/free-calgary-furnace-size-and-price-calculator/

    In Calgary and area, square footage is one way to ballpark sizing and another way, multiply the above grade square footage by 35-50 btu.

    This will give you the size of unit required. BTU/hr

    Homes built AFTER 2005 get a multiplier of 35 btu.

    Homes BETWEEN 1982 and 2005 get a multiplier of 42.5 btu. If you’ve performed upgrades to   windows and attic, you can lean towards 35 btu.

    Homes BEFORE 1982 multiply by 50 btu. If the    windows and attic are upgraded, bump to 42.5. If the exterior insulation,  windows, and attic have been upgraded, bump to 35 btu.
    '''

    if year_built > 2005:
        multi = 35

    else:
    

        # 82 house with no upgrades 

        if year_built >= 1982 and year_built <= 2005:

            multi = 42.5

            if  windows:
                multi = 40
            if wall:
                multi = 39
            if roof:
                multi = 39
            if  windows and wall:
                multi = 37
            if  windows and roof:
                multi = 37
            if wall and roof:
                multi = 36
            if wall and roof and windows:
                multi = 35
            

        if year_built < 1982:
            
            multi = 50

            if  windows:
                multi = 45
            if wall:
                multi = 42.5
            if roof:
                multi = 42.5
            if  windows and wall:
                multi = 40
            if  windows and roof:
                multi = 39
            if wall and roof:
                multi = 39
            if wall and roof and windows:
                multi = 35
    

    furnace_BTU = square_footage * multi


    #should have a BTU rating and a efficiency 
    furnace = [furnace_BTU, efficiency_val]

    return furnace

def predict_stories(footage):
    '''
    predict the houses square footage 
    possible outcomes 
    1 story
    1.5 story
    2 story
    3 story
    '''
    if footage < 1500:
        return 1
    if footage >= 1500 and footage < 2000:
        return 1.5
    if footage >= 2000 and footage < 3500:
        return 2
    if footage > 3500:
        return 3 


def resident_pretict(sqrft):
    # this is a easy question for the user to input but if they do not know we must assume and also assume for when labling real estat data. 
    '''
    2017 study showed that canadians have a large living space per person at 618sqft/person 
    source: https://www.rew.ca/news/canadians-enjoy-second-most-living-space-per-person-global-survey-1.9905436
    '''
    people = sqrft//618

    return people

def hotwater_tank_predict(ave_hotwater_use, people, year_built):
    '''
    water heating is unique and will need different outcomes. 

    hot water has different outcomes of heating
        gas heater == 90% 
        electric  == 100%


    hot water accounts for around 19% of energy usage of a household 

    Should calculate a per person daily usage and then also the size of a tank. 

    Average hot water heater lasts for about 13 years
        from this we could estimate how much longer is going to be left in their water heater. 

    
    source: https://blog.constellation.com/2016/10/06/which-is-more-efficient-tankless-vs-traditional-water-heaters/
    Tankless heaters can be 24-34% more energy-efficient than regular water heaters for households that use 41 gallons or fewer of hot water daily.
    Tankless heaters can be 8-14% more energy-efficient for households that use around 86 gallons daily.
    Installing a tankless heater at each hot water outlet, Energy.gov says, can increase tankless water heater energy savings by up to 27-50%.
    ENERGY STAR estimates that a typical family can save at least $100 annually in tankless water heater energy savings by using an ENERGY STAR-certified tankless heater.

        typical water usage Use	Gallons per use
            Shower	                                        7-10
            Bath (standard tub)	                            20
            Bath (whirlpool tub)	                        5-50
            Clothes washer (hot water wash, warm rinse)	    32
            Clothes washer (warm wash, cold rinse)	        7
            Automatic dishwasher	                        8-10
            Food preparation and cleanup	                5
            Personal (hand-washing, etc.)	                2
    '''

    #predict how many gallons of water used per day. 
    '''
    we assume that canadians ues about 75L of hot water a day thats 16.4977 gal
    source: https://www.nrcan.gc.ca/energy-efficiency/energy-efficiency-products/product-information/water-heaters/13735
    '''
    today = datetime.today()
    current_year = today.year

    #furnaces roughly last around 15 to 30 years most being replaced around 22 year mark
    average_liftime_hotwater = 15

    age = current_year - year_built 


    #furnace efficiency 
    
    number_of_hotwater = age // average_liftime_hotwater # this will get us the number of furnaces the house is currently on assuming that the furnace is replaced every 17 years 
    
    last_hotwater_replace_year = year_built + (number_of_hotwater * average_liftime_hotwater)

    if last_hotwater_replace_year >= 14:
        hotwater_eff = 0.50
    if last_hotwater_replace_year < 14 and last_hotwater_replace_year >= 10:
        hotwater_eff = 0.55
    if last_hotwater_replace_year < 10 and last_hotwater_replace_year >= 5:
        hotwater_eff = 0.60
    if last_hotwater_replace_year < 5:
        hotwater_eff = 0.65

    hot_water_per_day = people * ave_hotwater_use

    #hot water tanks come in variable sizes we will go 
    #  1 or 2 people    35 gallons
    #  3 people         50 gallons
    #  4 people         65 gallons
    #  5 or more people 80 gallons

    if hot_water_per_day <= 35:
        tank = 35
    if hot_water_per_day > 35 and hot_water_per_day <= 50:
        tank = 50 
    if hot_water_per_day > 50 and hot_water_per_day <= 65:
        tank = 65
    if hot_water_per_day > 65:
        tank = 80

    btu_per_hour = 35000
    #home.assumptions.append('Hot water tank is of size {} gal and there are {} people in your house'.format(tank, people))

    #home.hotwater = [tank]
    #home.hotwater_perday = hot_water_per_day

    tank_water = [tank, hot_water_per_day, btu_per_hour, hotwater_eff]

    return tank_water

#have to make a wall sqrfootage,    windowsdow squarefootage and a roof squarfootage assumptions. 

def window_sqrf(square_footage):
    '''
    https://www.energystar.gov/sites/default/files/ESWDS-ReviewOfCost_EffectivenessAnalysis.pdf
    we are assuming that    windowsdow square footage is going to be 15% of the floor square footage
    '''

    return square_footage * 0.25
    

def roof_sqrf(square_foot, stories):
    '''
    these values are alwasy different based on the pitch of the house steeper house means more heating area. 
    https://www.calculator.net/roofing-calculator.html
    pitch   angel   multiply    pitch   angle   multiply 
    1/12	4.8°	1.003	 	2/12	9.5°	1.014
    3/12	14.0°	1.031	    4/12	18.4°	1.054
    5/12	22.6°	1.083	    6/12	26.6°	1.118
    7/12	30.3°	1.158	    8/12	33.7°	1.202
    9/12	36.9°	1.250	    10/12	39.8°	1.302
    11/12	42.5°	1.357	    12/12	45.0°	1.414
    13/12	47.3°	1.474	    14/12	49.4°	1.537
    15/12	51.3°	1.601	    16/12	53.1°	1.667
    17/12	54.8°	1.734	    18/12	56.3°	1.803
    19/12	57.7°	1.873	    20/12	59.0°	1.944
    21/12	60.3°	2.016	    22/12	61.4°	2.088
    23/12	62.4°	2.162	    24/12	63.4°	2.236

    im just going to take a middle ground one for now come back and make it more accurate 
    most commong roof pitches are between 4/12 and 9/12 -> average out all these to get 1.144
    '''
    if stories > 1:
        floor_sqrf = square_foot/stories
        roof_sqrf = floor_sqrf * 1.144
    else:
        roof_sqrf = square_foot * 1.144

    return roof_sqrf

def wall_sqrf(square_foot, stories):
    '''
    we will need number of floors in the 

    cant find a rule of thumb for this right now will just do the cube with assumed 14 feet level 

    take the root of the square footage. then multiply it by 14 for hight. multiply that by 4 for each wall and then take away .30 of total squar feet
    '''

   

    if stories == None:
        # if there is no input just say that there is one story 

        stories = 1

    # we just need the bottom floor square footage
    bottom_floor = square_foot/stories

    root_footage = np.sqrt(bottom_floor)

    wall_size = root_footage * (14 * stories) * 4

    total_exterior_wall = wall_size - (.3 * square_foot)

    #home.wall_sqrf = total_exterior_wall

    #home.assumptions.append("Assuming that the exterior wall squarfootage is {}".format(total_exterior_wall))
    
    return total_exterior_wall


# R values --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#this is used to determin R values of walls 
# going to try and assume roof and  windows here too

'''
code of 2017 R-values source: https://www.canadianhomeinspection.com/home-reference-library/attic-roof-space/insulation/
Zone 1 <5000 HDD, gas/ propane heating 
ceiling with attic space:       RSI 10.56 (R60)
ceiling without attic space:    RSI 5.46 (R31)
walls above grade:              RSI 3.87 (R20)
basement walls:                 RSI 3.52 (R20)
exposed floor:                  RSI 5.46 (R31)
'''
def wall_R_assignmnet(year, year_built):
    # we should check for uprgades first if the walls/insulation has been upgraded we change it to the year it was done. 
    '''
    Insulation Type:	R-Value per Inch:
    Fiberglass (loose)	    2.2 – 2.9
    Fiberglass (batts)	    2.9 – 3.8
    Cellulose (loose)	    3.1 – 3.8
    Stone Wool (loose)	    2.2 – 3.3
    Stone Wool (batts)	    3.3 – 4.2
    Cotton (batts)	        3.0 – 3.7
    Cementitious (foam)	    2.0 – 3.9
    Polyicynene (foam)	    3.6 – 4.3
    Phenolic (foam)	        4.4 – 8.2
    Polyisocyanurate (foam)	5.6 – 8.0
    Polyurethane (foam)	    5.6 – 8.0

    going to say walls are to be 190mm thick so 7.5 inch

    can find a solid source to say what years used what will go off this: https://www.retrofoamofmichigan.com/blog/home-insulation-history

    1930 - 40 : loose fiberglass R = 2.2

    1950 - 70 : fire retardant was added loose cellulose was used  R = 3.2

    1970 - : pink fiberglass value of 3.8
    
    Polyicynene foam 4.3

    new sparyfoam : 5.6

    '''
    # if no year is provided then no upgrades have happend
    if year == None:
        year = year_built

    if year <= 1930:
        #old house has the worst 
        wall_R = 16.5
        wall = 'loose fiberglass'


    
    if (year > 1930) and (year < 1950):
        wall_R = 20
        wall = 'loosr fiberglass'
        

    if (year >= 1950) and (year <= 1970):
        wall_R = 24 
        wall = 'loose cellulose'
        

    if year > 1970 and year <= 2000:
        # these houses are using foam for their insulation
        wall_R = 28
        wall = 'foam'
        

    
    if year > 2000 and year < 2010:
        wall_R = 35.25
        wall = 'foam'
        

    
    if year >= 2010:
        # spary foam insulation best it can be R = 5.6
        wall_R = 42
        wall = 'spray foam'
        

    #home.assumptions.append('Walls are 7.5inch thick and insulated with {} or fiberglass, R = {}'.format(wall,home.wall_R))

    walls = [wall_R , wall]
    
    return walls

        


# for now i am going to leave this the same as the assigning wall values
def roof_R_assignmnet(year, year_built):
    # if no year is provided then no upgrades have happend
    if year == None:
        year = year_built

    if year <= 1930:
        #old house has the worst 
        roof_R = 16.5
        
        
    
    if (year > 1930) and (year <= 1950):
        # sort of old house 
        roof_R = 23


    if (year > 1950) and (year <= 1970):
        roof_R = 27

    if year > 1970 and year <= 2000:
        # these houses are using foam for their insulation
        roof_R = 30
        
    
    if year > 2000 and year <= 2010:
        roof_R = 35.25
        
    
    if year > 2010:
        # spary foam insulation best it can be R = 5.6
        roof_R = 42
        
    return roof_R


    

def windows_R_assignment(year, year_built):
    # if    windows have been upgraded then put year as the year the   windows where upgraded 
    '''
    windowsdow                                          R-value

    single pain wood                                1
    Double-Pane/Aluminum Frame                      1.7
    Double-Pane Vinyl Argon                         2.9
    Average ENERGY STAR windowsdow                      2.9
    Triple-Pane/Two Low-E                           3.2
    Double-Pane Wood Low-E + Storm                  3.4

    '''
    # if no year is provided then no upgrades have happend
    if year == None:
        today = datetime.today()
        current_year = today.year

        #We will assume that    windows are replaced every 30 years
        average_window_liftime = 35

        age = current_year - year_built 

        number_of_window = age // average_window_liftime
        
        last_windows_replace_year = year_built + (number_of_window * average_window_liftime)


    if last_windows_replace_year <= 1960:
        #old house has the worst 
        windows_R = 1
        windows = 'Single pane old windows'
        
    
    if (last_windows_replace_year > 1960) and (last_windows_replace_year <= 1980): 
        windows_R = 1.2
        windows = 'Double pane aluminum frame no thermal break'
         
        

    if (last_windows_replace_year > 1980) and (last_windows_replace_year <= 1990): # houses in the 80s and 90s where wood or aluminum frame double pain   windows source:https://sdinspect.com/wp-content/uploads/Buying-a-house-built-in-the-1980s-or-1990s.pdf
        windows_R = 1.7 
        windows = 'Double pane aluminum frame with thermal break'
        

    if (last_windows_replace_year > 1990) and (last_windows_replace_year <= 2000):
        windows_R = 2.5
        windows = 'Double Pane/Med solar Low-E'
        
    if (last_windows_replace_year > 2000) and (last_windows_replace_year <= 2010):
        windows_R = 3.0
        windows = 'Double Pane Vinyle/wood with low-E argon'

    if (last_windows_replace_year > 2010):
        windows_R = 3.4
        windows = 'Double Pane low-E + storm or tripple panel'

    #home.assumptions.append(   windows are {} with a R value of {} last replaced in {}'.format(home  windows, home    windowsdow_R, last windowsdow_replace_year))

    return  [windows_R,   windows]
        

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
 electrical assumptions
    fridge 
    plug load 
    oven
'''

def fridge_predict(year_built):
    # this will predict how old a fridge is
    # if no year is provided then no upgrades have happend
    today = datetime.today()
    current_year = today.year

    #We will assume that    windows are replaced every 30 years
    average_liftime_fridge = 18

    age = current_year - year_built 

    number_of_fridge = age // average_liftime_fridge 
    
    year = year_built + (number_of_fridge * average_liftime_fridge)

    #year is the year the fridge was last replaced.

    age_of_fridge = current_year - year

    return age_of_fridge
    
def washer_predict(year_built):
    '''
    we have to predict the washer energy usage maybe even water usage 
        energy star washers are rated around 500 watts, we will set the wattage of the washer higher then that 

    '''
    return 1600

def dryer_predict(year_built):
    '''
     how to predict the washer and dryer?
     not sure yet we will assume that dryers user 3000w per hour energy star does not track dryers because they have not changed for a while 


    '''
    return 3000

def dishwasher_predict():
    '''
    dishwashers are hard because they do not last long and break often so people dont spend a lot on them. 
    might have to ask if the user has a energy star dish washer or assume that they do not 
    
    https://www.directenergy.com/learning-center/how-much-energy-dishwasher-use#:~:text=A%20dishwasher's%20base%20electricity%20usage,cent%20per%20kWh%20electricity%20plan.

    how much energy does a dishwasher use and water 

    a 1994 dishwasher useing 10 gallons per load and 1.27 kwh

    older energystar dishwashers useing 5 gallons and need 0.64 kwh

    a new energy star dishwasher 3.2 gallons per load and only 0.38 kwh


    for now we will just say that they have a mid range dishwasher 
    '''

    dishwasher = [1.10, 5]

    return dishwasher 
