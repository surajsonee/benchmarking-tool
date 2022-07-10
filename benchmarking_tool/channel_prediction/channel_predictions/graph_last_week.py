# graph and show the last week usage and predicted usage 
import numpy as np
import matplotlib.pyplot as plt

def graph_last_week(last_week_usage, predicted_dict):
    channel_names = predicted_dict.keys()
    last_week_cnames = last_week_usage.keys()

    if channel_names != last_week_cnames:
        looper_list = list(set(channel_names).intersection(last_week_cnames))
    else:
        looper_list = channel_names

    # have to take the last week usage and make it a single list 

    for key in looper_list:
        x = np.array(range(168))

        real = [] # number of hours in a week
        for day in last_week_usage[key]:
            real = np.append(real,last_week_usage[key][day])
        
        if len(real) > 168:
            real = real[0:168]

        pred = predicted_dict[key]['week_line']
        er = predicted_dict[key]['Error']

        if len(pred) > 168:
            pred = pred[0:168]


        plt.title(f'channel: {key}, accuracy percentage: {round(er,4)}')
        plt.plot(x, real, color = 'green',label='last week usage')
        plt.plot(x, pred,color='blue', label='predicted')
        plt.legend(loc="upper left")
        plt.xlabel('hours')
        plt.ylabel('Kwh')
        plt.show()
        
        
    return 
