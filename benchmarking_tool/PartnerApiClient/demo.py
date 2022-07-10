from Emporia_Customer import Emporia_Customer
import matplotlib.pyplot as plt
import pandas as pd

serial_number = 'A2108A04B4AC67B2F6A400'

#A2107A04B4B8F009A6CEC4, A2107A04B4AC67B2F76F18, A2108A04B4AC67B2F6A400
d1 = 1

# new way of using the new data
customer = Emporia_Customer(serial_number)

customer.get_data(days= d1)
customer.get_schedule()

#update the txt file before calling this function
# this is a hourly update 
d = customer.get_price_per_channel(0.75)

print(d)
print('d')

#print(customer.channel_names)
#print(customer.chan_min)

customer.save_channels()

serial_number2 = 'A2108A04B4AC67B2F6A400'


customer2 = Emporia_Customer(serial_number2)

customer2.get_data(days= d1)
customer2.get_schedule()

# this is the new function \
# make sure that the data is updated right befor this function is called to get the latest time 
# the final column in this might better be displayed as cents per hour rather then dollars as the numbers are very small 
d2 = customer2.percent_usage_minute_update(0.90)

print(d2)