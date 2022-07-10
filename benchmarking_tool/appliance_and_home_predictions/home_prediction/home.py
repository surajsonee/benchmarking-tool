# Home file 
# class that will be used to model a house 
from datetime import datetime
import calendar

class home_model:
    def __init__(self, year_built, total_sqrf):
        # some functions need the current date and time 
        #today = datetime.today
        #month = today.month
        #now = datetime.datetime.now()
        #days_month = calendar.monthrange(now.year, now.month)[1]

        self.year = None
        self.month = None
        self.day = None

        #year the house was built 
        self.year_built = year_built

        # square footages 
        self.total_sqrf = total_sqrf # floor square footage
        self.window_sqrf = None
        self.wall_sqrf = None
        self.roof_sqrf = None

        # heat loss and walls
        self.wall = None
        self.wall_R = None
        

        self.windows = None
        self.windows_R = None 
       

        self.roof = None
        self.roof_R = None
        

        #heat_loss
        self.wall_heat_loss = None
        self.window_heat_loss = None
        self.roof_heat_loss = None

        self.total_heat_loss = None
        
        self.heat_energy_input = None

        self.furnace_energy_input = None

        self.furnace_BTU = None 
        self.furnace_eff = None
        self.furnace_set = None # what do they set the furnace to in the coldest months?


        self.hotwater_fuel = None
        self.hotwater_eff = None
        self.hotwater_fuel_assume = None
        self.hotwater_tank_size = None
        self.hotwater_per_day = None
        self.hotwater_energy = None
        self.hotwater_perday = None # prediction of hot water used per day (# of residence * 16.4977)
        self.hotwater_use_per_person = None # gallons of water used per person, there could be a quiz to calculate this 

        #average tempurature of water coming into the house 
        self.incoming_water_temp = 50.9 # 10.5C
        self.hotwater_temp_set = 140 # 60C

        self.total_gas = None

        self.range_gj = None
        self.range_kwh = None
        # upgrades this will be true or false 

        self.windows_upgrade = None
        self.wall_upgrade = None
        self.roof_upgrade = None
        
        #ask user to input levels of their house not including basement 
        self.stories = None

        #people living in the house
        self.residence = None
        
        # electrical 

        # this is the type of lights that could be used 
        # one of 4 options incandesent,  halogen, CFL, LED  
        # if there is no option applied we will assume that it is CFL
        self.lights = None
        self.lumen_watts = None
        self.lights_kwh_month = None


        #appliances 

        # this is the age of the fridge
        self.fridge_age = None
        self.fridge_day_kwh = None
        # kWh of fridge per month 
        self.fridge_kwh_month = None

        self.oven_w = None
        self.cook_time_oven = None
        self.oven_kwh_month = None

        self.stove_w = None
        self.cook_time_stove = None
        self.stove_kwh_month = None

        self.microwave_w = None
        self.cook_time_microwave = None
        self.microwave_kwh_month = None
        
        self.dishwasher_w = None
        self.dishwasher_kwh_month = None
        self.dishwasher_water = None
        self.dishwasher_water_per_month = None
        self.dishwasher_loads = None # loads per day

        # laundry per person 
        # should we ask the user how many loads the house does in a week or how many loads a person does in a week?
        self.laundry_loads_per_month = None

        # this is a wattage of a washer
        self.washer_w = None
        # washer energy usage
        self.washer_kwh_month = None

        # this is wattage
        self.dryer_w = None
        self.dryer_kwh_load = None
        self.dryer_kwh_month = None

        self.extra_kwh = None

        self.total_kwh = None

        self.range_gj = []

        self.range_kwh = []

        # assumptions varuables should be true or false
        self.furnace_assume = None
        self.furnace_set_assume = None
        self.hotwater_assume = None
        self.hotwater_tank_assume = None
        self.hotwater_use_per_person_assume = None
        self.wall_assume = None
        self.wall_sqrf_assume = None
        self.wall_r_assume = None
        self.window_assume = None
        self.window_sqrf_assume = None
        self.window_r_assume = None
        self.roof_assume = None
        self.roof_sqrf_assume = None
        self.roof_r_assume = None
        self.residence_assume = None
        self.stories_assume = None
        self.lights_assume = None
        self.fridge_assume = None
        self.fridge_age_assume = None
        self.fridge_day_kwh_assume = None
        self.oven_assume = None
        self.cook_time_oven_assume = None
        self.microwave_assume = None
        self.cook_time_microwave_assume = None
        self.cook_time_oven_assume = None
        self.stove_assume = None
        self.cook_time_stove_assume = None
        self.washer_assume = None
        self.dryer_assume = None
        self.laundry_loads_assume = None
        self.dishwasher_assume = None
        self.dishwasher_loads_assume = None

        self.assumptions = [self.furnace_assume,
                            self.furnace_set_assume,
                            self.hotwater_assume,
                            self.hotwater_assume,
                            self.hotwater_tank_assume,
                            self.hotwater_use_per_person_assume,
                            self.wall_assume,
                            self.wall_sqrf_assume,
                            self.wall_r_assume,
                            self.window_assume,
                            self.window_sqrf_assume,
                            self.window_r_assume,
                            self.roof_assume,
                            self.roof_sqrf_assume,
                            self.roof_r_assume,
                            self.residence_assume,
                            self.stories_assume,
                            self.lights_assume,
                            self.fridge_assume,
                            self.oven_assume,
                            self.washer_assume,
                            self.dryer_assume]
        self.assumptions_dict = {}


    def p_usage_gas(self):
        print("Gas Usage")
        print("wall heat loss: {}".format(self.wall_heat_loss))
        print("window heat loss: {}".format(self.window_heat_loss))
        print("roof heat loss: {}".format(self.roof_heat_loss))
        print("total heat loss: {}".format(self.total_heat_loss))
        print("furnace energy: {} BTU, {} GJ".format(self.furnace_energy_input, self.furnace_energy_input*0.0000010551))
        print("hot water gas usage {} BTU, {} GJ".format(self.hotwater_energy, self.hotwater_energy*0.0000010551))
        print("total gas usage: {} BTU, {} GJ".format(self.total_gas, self.total_gas*0.0000010551))

    def p_usage_kwh(self):
        print("electrical usage")
        print("lights: {} kwh".format(self.lights_kwh_month))
        print("fridge: {} kwh".format(self.fridge_kwh_month))
        print("oven: {} kwh".format(self.oven_kwh_month))
        print("stove: {} kwh".format(self.stove_kwh_month))
        print("microwave: {} kwh".format(self.microwave_kwh_month))
        print("dishwasher: {} kwh".format(self.dishwasher_kwh_month))
        print("washer: {} kwh".format(self.washer_kwh_month))
        print("dryer: {} kwh".format(self.dryer_kwh_month))
        print("extra: {} kwh".format(self.extra_kwh))
        print("total: {} kwh".format(self.total_kwh))


    def get_assumptions(self, p):
        # we need to show what as been assumed 
        # if p is true it will print but if it is false then there will be no prints and it will just assign the dictionary
        if p == True:
            print('these are all the assumptions made')

        if self.furnace_assume == True:
            if p == True:
                print("furnace size is {} BTU and at {} efficiency".format(self.furnace_BTU,self.furnace_eff))
            self.assumptions_dict['furnace_BTU'] = self.furnace_BTU
            self.assumptions_dict['furnace_eff'] = self.furnace_eff
        
        if self.furnace_set_assume == True:
            if p == True:
                print("Furnace is set to {} F in the coldest months of the year".format(self.furnace_set))
            self.assumptions_dict['furnace_set'] = self.furnace_set
        
        if self.hotwater_tank_assume == True:
            if p == True:
                print("the hot water tank is {} gallons".format(self.hotwater_tank_size))
            self.assumptions_dict['hotwater_tank_size'] = self.hotwater_tank_size
        
        if self.hotwater_use_per_person_assume == True:
            if p == True:
                print("each person in the house uses {} gallons of hot water a day".format(self.hotwater_use_per_person))
            self.assumptions_dict['hotwater_use_per_person'] = self.hotwater_use_per_person
        
        if self.wall_assume == True:
            if p == True:
                print("The exterior walls are insulated with {}".format(self.wall))
            self.assumptions_dict['wall'] = self.wall
        
        if self.wall_sqrf_assume == True:
            if p == True:
                print("exterior wall square footage is {} sqrf".format(self.wall_sqrf))
            self.assumptions_dict['wall_squrf'] = self.wall_sqrf
        
        if self.wall_r_assume == True:
            if p == True:
                print("Wall R values are {}".format(self.wall_R))
            self.assumptions_dict['wall_R'] = self.wall_R

        if self.window_assume == True:
            if p == True:
                print("Windows are {}".format(self.windows))
            self.assumptions_dict['window'] = self.windows
        
        if self.window_sqrf_assume == True:
            if p == True:
                print("window square footage is {} sqrf".format(self.window_sqrf))
            self.assumptions_dict['window_sqrf'] = self.window_sqrf
        
        if self.window_r_assume == True:
            if p == True:
                print("that window R values are {}".format(self.windows_R))
            self.assumptions_dict['window_R'] = self.windows_R
        
        if self.roof_sqrf_assume == True:
            if p == True:
                print("roof square footage is {} sqrf".format(self.roof_sqrf))
            self.assumptions_dict['roof_sqrf'] = self.roof_sqrf
        
        if self.roof_r_assume == True:
            if p == True:
                print("roof R is {}".format(self.roof_R))
            self.assumptions_dict['roof_R'] = self.roof_R
        
        if self.residence_assume == True:
            if p == True:
                print("there are {} people living in the house".format(self.residence))
            self.assumptions_dict['residence'] = self.residence
        
        if self.stories_assume == True:
            if p == True:
                print("this house is {} stories".format(self.stories))
            self.assumptions_dict['stories'] = self.stories
        
        if self.lights_assume == True:
            if p == True:
                print('the primary type of light bulb in your house is a {}'.format(self.lights))  
            self.assumptions_dict['lights'] = self.lights      
        
        if self.fridge_assume == True:
            if p == True:
                print('your firdge uses {} kwh per day'.format(self.fridge_day_kwh))
            self.assumptions_dict['fridge_day_kwh'] = self.fridge_day_kwh

        if self.fridge_age_assume == True:
            if p == True:
                print('your fridge is {} years old'.format(self.fridge_age))
            self.assumptions_dict['fridge_age'] = self.fridge_age
        
        if self.fridge_day_kwh_assume == True:
            if p == True:
                print('your fridge uses {} kwh per day'.format(self.fridge_day_kwh))
            self.assumptions_dict['fridge_day_kwh'] = self.fridge_day_kwh_assume

        if self.oven_assume == True:
            if p == True:
                print('your oven is {} watts'.format(self.oven_w))
            self.assumptions_dict['oven_w'] = self.oven_w

        if self.cook_time_oven_assume == True:
            if p == True:
                print('your estimated cook time is {} hours'.format(self.cook_time_oven))
            self.assumptions_dict['cook_time_oven'] = self.cook_time_oven
        
        if self.washer_assume == True:
            if p == True:
                print('your washer is {} watts'.format(self.washer_w))
            self.assumptions_dict['washer_w'] = self.washer_w

        if self.dryer_assume == True:
            if p == True:
                print('your dryer is {} watts'.format(self.dryer_w))
            self.assumptions_dict['dryer_w'] = self.dryer_w

        if self.dishwasher_assume == True:
            if p == True:
                
                print('your dishwasher is {} watts, and {} gallons of water per load'.format(self.dishwasher_w, self.dishwasher_water))
            self.assumptions_dict['dishwasher_w'] = self.dishwasher_w

        if self.dishwasher_loads_assume == True:
            if p == True:
                print('you do {} dishwasher cycles a day'.format(self.dishwasher_loads))
            self.assumptions_dict['dishwasher_loads'] = self.dishwasher_loads

        
        return 

    def print_range(self):
        if self.range_gj == [] or self.range_kwh == []:
            return 

        print('Your gas bill estimation is {} GJ - {} GJ'.format(self.range_gj[0], self.range_gj[1]))

        print('Your electrical bill estimation is {} kWh - {} kWh'.format(self.range_kwh[0], self.range_kwh[1]))

        return