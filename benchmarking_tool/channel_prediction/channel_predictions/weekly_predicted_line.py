# input the data then return a predicted line for the whole week
from sklearn.metrics import mean_squared_error
import numpy as np 
from .clean_dataframe import clean_dataframe
from .regressor import regressor
from .df_weekday_data import df_weekday_data
# channel_dict comes from channel_dict, dates = weekday_organization(data)
def weekly_predicted_line(channel_dict, last_week_usage):

    channel_names = channel_dict.keys()
    #print(channel_names)
    last_week_cnames = last_week_usage.keys()
    #print(last_week_cnames)
    
    if channel_names != last_week_cnames: 
        print('not all channel names are in last_week_cnames and channel names ')
        looper_list = list(set(channel_names).intersection(last_week_cnames))
    else:
        looper_list = channel_names

    # we need to clean each channel of data 
    errors_dict = {}
   
    return_dict = {}

    for c_name in looper_list:
        if c_name not in errors_dict.keys():
            #print(f'{c_name} this was not in the error dict')
                    
            errors_dict[c_name] = []

                
        monday_df, tuesday_df, wednesday_df, thursday_df, friday_df, saturday_df, sunday_df = df_weekday_data(channel_dict[c_name])

        clean_monday = clean_dataframe(monday_df)

        mon_reggressor, mon_pred = regressor(clean_monday)

        clean_tuesday = clean_dataframe(tuesday_df)

        tue_reggressor, tue_pred = regressor(clean_tuesday)

        clean_wednesday = clean_dataframe(wednesday_df)

        wed_reggressor, wed_pred = regressor(clean_wednesday)

        clean_thursday = clean_dataframe(thursday_df)

        thur_reggressor, thur_pred = regressor(clean_thursday)

        clean_friday = clean_dataframe(friday_df)

        fri_reggressor, fri_pred = regressor(clean_friday)

        clean_saturday = clean_dataframe(saturday_df)

        sat_reggressor, sat_pred = regressor(clean_saturday)

        clean_sunday = clean_dataframe(sunday_df)

        sun_reggressor, sun_pred = regressor(clean_sunday)

        w_line = np.append(mon_pred, tue_pred)

        e = [wed_pred, thur_pred, fri_pred, sat_pred, sun_pred]

        for j in e:
            w_line = np.append(w_line,j)

        # get the errors
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][0][0],mon_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][1][0],tue_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][2][0],wed_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][3][0],thur_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][4][0],fri_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][5][0],sat_pred))
        errors_dict[c_name].append(mean_squared_error(last_week_usage[c_name][6][0],sun_pred))

        error_ave = np.average(errors_dict[c_name])

        if error_ave < 0.01:
            error_ave = 0.01

        return_dict[c_name] = {'week_line': w_line, 'Error': error_ave}

    return return_dict


