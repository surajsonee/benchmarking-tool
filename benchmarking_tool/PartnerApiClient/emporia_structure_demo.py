# this is a file to display what the emporia_structure package can do 

from emporia_structure import ave_channel_usage, Channel, clean_data,get_channels,on_off_usage,UTC_MTN

from get_data import get_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#other serial numbers 
# these are 
# A2107A04B4AC67B2F76F18
# A2108A04B4AC67B2F6A400

serial_number = 'A2107A04B4AC67B2F76F18'

l = get_data(serial_number, 5)

mint = l[0]
fivmin = l[1]
hour = l[2]

mains, chan = clean_data(hour)
