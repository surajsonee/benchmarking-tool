# need a function that cleans up all the data
# this data is right from get_data call
import pandas as pd
import numpy as np
from .UTC_MTN import UTC_MTN
from .get_channels import get_channels
def clean_data(data,channel_names):
    c = get_channels(data, channel_names)
    c_mains = c[0]
    channels = c[1]
    t = data['time']
    d = data['date']

    date_time = []
    
    for i in range(len(t)): 
        date_time.append(d[i] + ' ' + t[i])
    
    local_time = UTC_MTN(date_time)
    

    t = []
    d = []
    m = []
    y = []
    mi = []
    for i in local_time['datetime']:
        t.append(i.hour)
        d.append(i.day)
        m.append(i.month)
        y.append(i.year)
        mi.append(i.minute)

    
    t = pd.Series(t)
    d = pd.Series(d)
    m = pd.Series(m)
    y = pd.Series(y)
    mi = pd.Series(mi)
    inp = [y,m,d,t,mi]
    mains = inp.copy()
    mains.append(c_mains.data)

    for i in channels:
        inp.append(i.data)

    mains_df = pd.concat(mains,axis=1)
    mains_df = mains_df.rename(columns={0:'year'})
    mains_df = mains_df.rename(columns={1:'month'})
    mains_df = mains_df.rename(columns={2:'day'})
    mains_df = mains_df.rename(columns={3:'hour'})
    mains_df = mains_df.rename(columns={4:'minute'})
    mains_df = mains_df.rename(columns={5:'mains'})

    chan = pd.concat(inp,axis=1)
    chan = chan.rename(columns={0:'year'})
    chan = chan.rename(columns={1:'month'})
    chan = chan.rename(columns={2:'day'})
    chan = chan.rename(columns={3:'hour'})
    chan = chan.rename(columns={4:'minute'})

    
    chan = chan.apply(pd.to_numeric)
    

    

    return [mains_df, chan]