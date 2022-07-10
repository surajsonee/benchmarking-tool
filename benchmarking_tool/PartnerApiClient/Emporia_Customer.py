from benchmarking_tool.PartnerApiClient.emporia_structure import ave_channel_usage, Channel, clean_data,get_channels,on_off_usage,UTC_MTN,category_usage
from benchmarking_tool.PartnerApiClient.get_data import get_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime


class Emporia_Customer():
    def __init__(self, serial_number):
        self.serial_number = serial_number # string 

        self.address = None
        self.description = None # a description of the channels 

        # need to set all the channels and names on the channels 

        # init all channel classes 
        self.mains = Channel()

        self.channel1 = Channel()
        self.channel2 = Channel()
        self.channel3 = Channel()
        self.channel4 = Channel()
        self.channel5 = Channel()
        self.channel6 = Channel()
        self.channel7 = Channel()
        self.channel8 = Channel()
        self.channel9 = Channel()
        self.channel10 = Channel()
        self.channel11 = Channel()
        self.channel12 = Channel()
        self.channel13 = Channel()
        self.channel14 = Channel()
        self.channel15 = Channel()
        self.channel16 = Channel()
        self.channel17 = Channel()
        self.channel18 = Channel()
        self.channel19 = Channel()
        self.channel20 = Channel()
        self.channel21 = Channel()
        self.channel22 = Channel()
        self.channel23 = Channel()

        self.channel_list = [self.channel1,
                                self.channel2,
                                self.channel3,
                                self.channel4,
                                self.channel5,
                                self.channel6,
                                self.channel7,
                                self.channel8,
                                self.channel9,
                                self.channel10,
                                self.channel11,
                                self.channel12,
                                self.channel13,
                                self.channel14,
                                self.channel15,
                                self.channel16,
                                self.channel17,
                                self.channel18,
                                self.channel19,
                                self.channel20,
                                self.channel21,
                                self.channel22,
                                self.channel23]

        

    def get_data(self, days):
        #mains, channels = get_data(serial_number=self.serial_number, days=days)
        
        l, channel_names = get_data(self.serial_number, days)

        self.days = days

        mint = l[0]
        fivmin = l[1]
        hour = l[2]

        
        self.channel_names = channel_names[self.serial_number]

        mains_hours, chan_hours = clean_data(hour,self.channel_names )
        mains_fivmin, chan_fivmin = clean_data(fivmin,self.channel_names)
        mains_min, chan_min = clean_data(mint,self.channel_names)

        self.mains_hours = mains_hours
        self.mains_fivmin = mains_fivmin
        self.mains_min = mains_min

        self.chan_hours = chan_hours
        self.chan_fivmin = chan_fivmin
        self.chan_min = chan_min

    def get_data_minute(self, days):
        #mains, channels = get_data(serial_number=self.serial_number, days=days)
        
        l, channel_names = get_data(self.serial_number, days)

        self.days = days

        mint = l[0]

        
        self.channel_names = channel_names[self.serial_number]


        mains_min, chan_min = clean_data(mint,self.channel_names)

        self.mains_min = mains_min

        self.chan_min = chan_min

        return chan_min

    def day_category_usage(self):
        # needs to have hours data to use 
        usage, categories = category_usage(self.chan_hours)
        last_hour = self.chan_hours.tail(1)
        d = datetime(last_hour['year'].values[0],last_hour['month'].values[0],last_hour['day'].values[0],last_hour['hour'].values[0],last_hour['minute'].values[0])
        return usage, categories, d 

    def hour_category_usage(self):
        last_hour = self.chan_hours.tail(1)
        t = 1
        d = datetime(last_hour['year'].values[0],last_hour['month'].values[0],last_hour['day'].values[0],last_hour['hour'].values[0],last_hour['minute'].values[0])
        for i in last_hour:
            if last_hour[i].values != last_hour[i].values:
                t += 1
                last_hour = 0
                last_hour = self.chan_hours.tail(t)
                d = datetime(last_hour['year'].values[0],last_hour['month'].values[0],last_hour['day'].values[0],last_hour['hour'].values[0],last_hour['minute'].values[0])
                break


        usage, categories = category_usage(last_hour)
        return usage,categories, d

    def minute_category_usage(self):
        last_min = self.chan_min.tail(1)
        t = 1
        d = datetime(last_min['year'].values[0],last_min['month'].values[0],last_min['day'].values[0],last_min['hour'].values[0],last_min['minute'].values[0])
                
        for i in last_min:
            
            if last_min[i].values != last_min[i].values:
                t += 1
                last_min = 0
                last_min = self.chan_min.tail(t)
                d = datetime(last_min['year'].values[0],last_min['month'].values[0],last_min['day'].values[0],last_min['hour'].values[0],last_min['minute'].values[0])
                break

        last_min = last_min.multiply(other = 60)

        print(last_min)

        usage, categories = category_usage(last_min)

        return usage, categories, d
    
    def get_schedule(self): 
        # gets the schedule of the pas days 

        self.schedule = on_off_usage(self.chan_hours)
        self.mains_schedule = on_off_usage(self.mains_hours)

    def get_price_per_channel_day(self, price_per_kwh):
        # this function takes the total energy used on all channels for a day and then returns how much it is costing per hour 

        hours = self.chan_hours

        hours = hours.drop(columns = ['year','month','day','hour','minute'])

        

        # only way to get the mains off is to look at the first 3 names in the channel names list 

        main_names = self.channel_names[:3]
        try:
            hours = hours.drop(columns = main_names)
        except:
            pass

        # need to get the total 

        totals  = hours.sum()

        totals = totals /1000

        
        total_energy = totals.sum()

        

        cols = ['circuit name', 'percentage','price per hour']

        df = pd.DataFrame(columns=cols)

        hours = self.days * 24
        

        

        for i in range(len(totals.index)): 
            percent_usage = float(totals[i])/float(total_energy)
            usage_price = price_per_kwh * (float(totals[i])/float(hours)) # divide it by 24 to get average usage per hour 

            df.loc[i] = [totals.index[i],percent_usage,usage_price]

            #df['circuit name'].append(i)
            #df['percentage'].append(percent_usage)
            #df['price per hour'].append(usage_price)

        self.channel_cost = df

        return df

    def get_price_per_channel_hour(self, price_per_kwh):
         
        try:
            hours = self.chan_hours
        except:
            get_data(1)
            hours = self.chan_hours
        
        # need to get the latest hour
        t = 1

        last_hour = hours.tail(t)

        d = datetime(last_hour['year'].values[0],last_hour['month'].values[0],last_hour['day'].values[0],last_hour['hour'].values[0],last_hour['minute'].values[0])
        
        last_hour = last_hour.drop(columns = ['year','month','day','hour','minute'])

        # if the final minute did not come in properly it will look at one back 
        for i in last_hour:
            
            if last_hour[i].values != last_hour[i].values:
                t += 1
                last_hour = 0
                last_hour = hours.tail(t)
                d = datetime(last_hour['year'].values[0],last_hour['month'].values[0],last_hour['day'].values[0],last_hour['hour'].values[0],last_hour['minute'].values[0])
                last_hour = last_hour.drop(columns = ['year','month','day','hour','minute'])
                break
                
        

        # only way to get the mains off is to look at the first 3 names in the channel names list 

        main_names = self.channel_names[:3]
        try:
            last_hour = last_hour.drop(columns = main_names)
        except:
            pass

        # need to get the total 
        
        total_watts  = last_hour.sum()
    
       

        cols = ['circuit name', 'percentage','price per hour','watts in hour']

        df = pd.DataFrame(columns=cols)

        # have to get the total to kwh right now it is in watts per min 
        
        # 1 watt minute = 0.000017 kwh

        hour_kwh = total_watts /1000

        total_energy = total_watts.sum()



        for i in range(len(total_watts.index)): 
            try:
                percent_usage = float(total_watts[i])/float(total_energy)
            except:
                percent_usage = 0.0
            #usage_price = price_per_kwh * (float(totals[i])/float(hours)) # divide it by 24 to get average usage per hour 
            usage_price = price_per_kwh * hour_kwh[i]

            df.loc[i] = [total_watts.index[i],percent_usage,usage_price,total_watts[i]]



        self.channel_cost_hour = df

        return df, d

        
    def percent_usage_minute_update(self, price_per_kwh):
        # this function will get the latest minute it can from emporia 

        minutes = self.get_data_minute(days = 1)

        
        # need to get the latest minute 
        t = 1

        last_min = minutes.tail(t)

        d = datetime(last_min['year'].values[0],last_min['month'].values[0],last_min['day'].values[0],last_min['hour'].values[0],last_min['minute'].values[0])
        


        last_min = last_min.drop(columns = ['year','month','day','hour','minute'])

        # if the final minute did not come in properly it will look at one back 
        for i in last_min:
            
            if last_min[i].values != last_min[i].values:
                t += 1
                last_min = 0
                last_min = minutes.tail(t)
                d = datetime(last_min['year'].values[0],last_min['month'].values[0],last_min['day'].values[0],last_min['hour'].values[0],last_min['minute'].values[0])
                last_min = last_min.drop(columns = ['year','month','day','hour','minute'])
                break
                
        

        # only way to get the mains off is to look at the first 3 names in the channel names list 

        main_names = self.channel_names[:3]
        try:
            last_min = last_min.drop(columns = main_names)
        except:
            pass

        # need to get the total 
        
        totals  = last_min.sum()
        
        totals = totals * 60
        
        #total_energy = totals.sum()
       

        cols = ['circuit name', 'percentage','price per hour','watts in minute']

        df = pd.DataFrame(columns=cols)

        # have to get the total to kwh right now it is in watts per min 
        
        # 1 watt minute = 0.000017 kwh

        total_watts = totals

        kw_totals = total_watts /1000



        total_energy = totals.sum()

        kwh_minute = kw_totals * (1/60) # take kw and multiplyit by the time so 1 min = 1/60 hours

        hour_kwh = kwh_minute * 60  # how many kwh would it take if it was on for a hour 


        for i in range(len(totals.index)): 
            try:
                percent_usage = float(totals[i])/float(total_energy)
            except:
                percent_usage = 0.0
            #usage_price = price_per_kwh * (float(totals[i])/float(hours)) # divide it by 24 to get average usage per hour 
            usage_price = price_per_kwh * hour_kwh[i]

            df.loc[i] = [totals.index[i],percent_usage,usage_price,total_watts[i]]



        self.channel_cost_min = df
        
        return df, d

    def save_channels(self):  

        # first save the mains 
        self.mains.data_hour = self.mains_hours
        self.mains.data_fivmin = self.mains_fivmin
        self.mains.data_min = self.mains_min
        self.mains.schedule = self.mains_schedule

        # store the channels into a list for the customer
        channels = self.chan_min.drop(columns = ['year','month','day','hour','minute'])
        cols = channels.columns.tolist()
        
        
        for i in range(len(cols)):
            if cols[i] == 'year' or cols[i] == 'month' or cols[i] == 'day' or cols[i] == 'minute':
                continue

            if i == 0: # the 4th channel 

                self.channel4.name = cols[i]
                self.channel4.data_hour = self.chan_hours[cols[i]]
                self.channel4.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel4.data_min = self.chan_min[cols[i]]
                self.channel4.schedule = self.schedule[cols[i]]

            if i == 1:
                self.channel5.name = cols[i]
                self.channel5.data_hour = self.chan_hours[cols[i]]
                self.channel5.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel5.data_min = self.chan_min[cols[i]]
                self.channel5.schedule = self.schedule[cols[i]]

            if i == 2:
                self.channel6.name = cols[i]
                self.channel6.data_hour = self.chan_hours[cols[i]]
                self.channel6.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel6.data_min = self.chan_min[cols[i]]
                self.channel6.schedule = self.schedule[cols[i]]


            if i == 3:
                self.channel7.name = cols[i]
                self.channel7.data_hour = self.chan_hours[cols[i]]
                self.channel7.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel7.data_min = self.chan_min[cols[i]]
                self.channel7.schedule = self.schedule[cols[i]]

            if i == 4:
                self.channel8.name = cols[i]
                self.channel8.data_hour = self.chan_hours[cols[i]]
                self.channel8.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel8.data_min = self.chan_min[cols[i]]
                self.channel8.schedule = self.schedule[cols[i]]

            if i == 5:
                self.channel8.name = cols[i]
                self.channel8.data_hour = self.chan_hours[cols[i]]
                self.channel8.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel8.data_min = self.chan_min[cols[i]]
                self.channel8.schedule = self.schedule[cols[i]]

            if i == 6:
                self.channel10.name = cols[i]
                self.channel10.data_hour = self.chan_hours[cols[i]]
                self.channel10.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel10.data_min = self.chan_min[cols[i]]
                self.channel10.schedule = self.schedule[cols[i]]

            if i == 7:
                self.channel11.name = cols[i]
                self.channel11.data_hour = self.chan_hours[cols[i]]
                self.channel11.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel11.data_min = self.chan_min[cols[i]]
                self.channel11.schedule = self.schedule[cols[i]]

            if i == 8:
                self.channel12.name = cols[i]
                self.channel12.data_hour = self.chan_hours[cols[i]]
                self.channel12.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel12.data_min = self.chan_min[cols[i]]
                self.channel12.schedule = self.schedule[cols[i]]
            
            if i == 9:
                self.channel13.name = cols[i]
                self.channel13.data_hour = self.chan_hours[cols[i]]
                self.channel13.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel13.data_min = self.chan_min[cols[i]]
                self.channel13.schedule = self.schedule[cols[i]]

            if i == 10:
                self.channel14.name = cols[i]
                self.channel14.data_hour = self.chan_hours[cols[i]]
                self.channel14.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel14.data_min = self.chan_min[cols[i]]
                self.channel14.schedule = self.schedule[cols[i]]

            if i == 11:
                self.channel15.name = cols[i]
                self.channel15.data_hour = self.chan_hours[cols[i]]
                self.channel15.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel15.data_min = self.chan_min[cols[i]]
                self.channel15.schedule = self.schedule[cols[i]]
            
            if i == 12:
                self.channel16.name = cols[i]
                self.channel16.data_hour = self.chan_hours[cols[i]]
                self.channel16.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel16.data_min = self.chan_min[cols[i]]
                self.channel16.schedule = self.schedule[cols[i]]

            if i == 13:
                self.channel17.name = cols[i]
                self.channel17.data_hour = self.chan_hours[cols[i]]
                self.channel17.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel17.data_min = self.chan_min[cols[i]]
                self.channel17.schedule = self.schedule[cols[i]]

            if i == 14:
                self.channel18.name = cols[i]
                self.channel18.data_hour = self.chan_hours[cols[i]]
                self.channel18.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel18.data_min = self.chan_min[cols[i]]
                self.channel18.schedule = self.schedule[cols[i]]
            
            if i == 15:
                self.channel19.name = cols[i]
                self.channel19.data_hour = self.chan_hours[cols[i]]
                self.channel19.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel19.data_min = self.chan_min[cols[i]]
                self.channel19.schedule = self.schedule[cols[i]]

            if i == 16:
                self.channel20.name = cols[i]
                self.channel20.data_hour = self.chan_hours[cols[i]]
                self.channel20.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel20.data_min = self.chan_min[cols[i]]
                self.channel20.schedule = self.schedule[cols[i]]

            if i == 17:
                self.channel21.name = cols[i]
                self.channel21.data_hour = self.chan_hours[cols[i]]
                self.channel21.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel21.data_min = self.chan_min[cols[i]]
                self.channel21.schedule = self.schedule[cols[i]]

            if i == 18:
                self.channel22.name = cols[i]
                self.channel22.data_hour = self.chan_hours[cols[i]]
                self.channel22.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel22.data_min = self.chan_min[cols[i]]
                self.channel22.schedule = self.schedule[cols[i]]

            if i == 19:
                self.channel23.name = cols[i]
                self.channel23.data_hour = self.chan_hours[cols[i]]
                self.channel23.data_fivmin = self.chan_fivmin[cols[i]]
                self.channel23.data_min = self.chan_min[cols[i]]
                self.channel23.schedule = self.schedule[cols[i]]
        return 


