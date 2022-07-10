# helper function to get average and standard deviation 

def ave_channel_usage(channels_hours):
    #gpchan = channels_hours.groupby('hour', as_index = False).mean()
    #stdchan = channels_hours.groupby('hour', as_index = False).std()

    

    try:
        gpchan = channels_hours.drop(['year','month','day','minute'], axis=1)
        stdchan = channels_hours.drop(['year','month','day','minute'], axis=1)
    except:
        gpchan = channels_hours
        stdchan = channels_hours
        
    gpchan = gpchan.mean()
    stdchan = stdchan.std()


    return gpchan, stdchan