# plot the weekday data per channel
# this will take in one channel name dict from weekday_organizaiton and will plot all 7 days 
import pandas as pd

def df_weekday_data(channel_data): 

    monday_df = pd.DataFrame(channel_data[0], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    tuesday_df = pd.DataFrame(channel_data[1], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    wednesday_df = pd.DataFrame(channel_data[2], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    thursday_df = pd.DataFrame(channel_data[3], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    friday_df = pd.DataFrame(channel_data[4], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    saturday_df = pd.DataFrame(channel_data[5], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    sunday_df = pd.DataFrame(channel_data[6], columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    
    
    
    return monday_df, tuesday_df, wednesday_df, thursday_df, friday_df, saturday_df, sunday_df