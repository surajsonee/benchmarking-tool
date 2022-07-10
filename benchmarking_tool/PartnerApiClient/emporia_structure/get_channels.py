# this will take out the 3 first channels and get the mains 
import pandas as pd
from .Channel import Channel 
def get_channels(data, channel_names):
    list_of_series = []
    try: 
        data = data.drop(['date','time'], axis = 1)
    except:
        pass
    total = pd.Series(0,index=range(len(data)),dtype='float64')
    cols = data.columns.tolist()

    main_names = channel_names[:3]

    #total = np.array(len(data))
    for i in cols:
        #if i == 'channel 1' or i == 'channel 2' or i == 'channel 3':
        if i in main_names:
            t = data[i]
            total = total.add(t)
        else:
            channy = Channel()
            channy.data = data[i]
            list_of_series.append(channy)

    t = Channel()
    t.data = total

    return [t, list_of_series]