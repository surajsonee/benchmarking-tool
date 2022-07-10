import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import string
import io
import os
path = os.path.join(os.path.expanduser('~'), 'local', 'benchmarking_tool', 'benchmarking_tool', 'Output.txt')
path2 = os.path.join(os.path.expanduser('~'), 'local', 'benchmarking_tool', 'emporia_api_maven', 'target', 'emporiaenergy-client-1.0-SNAPSHOT.jar')
def get_data(serial_number, days):
    usage = ['1MIN','15MIN','1H']
    # first thing to do is call api and update the Output.txt file 
    # no api takes in a serial number and number of days to get past data. 
    # line_list = call_api(serial_number, days)
    
    subprocess.call(['java', '-jar', 'emporia_api_maven/target/emporiaenergy-client-1.0-SNAPSHOT.jar'])
    line_list = call_file('Output.txt')
    line_list.pop()

    sn = get_serial_list(line_list)
    
    channel_names1 = get_channel_names(line_list, serial_number)  

    usage_list1 = get_usage(line_list, usage[0], serial_number)
    usage_list2 = get_usage(line_list, usage[1], serial_number)
    usage_list3 = get_usage(line_list, usage[2], serial_number)

    data1 = make_df(usage_list1,channel_names1,serial_number)
    data2 = make_df(usage_list2,channel_names1,serial_number)
    data3 = make_df(usage_list3,channel_names1,serial_number)

    return [data1,data2,data3], channel_names1

#getting date time and usage. 
# emporia app login
# phart@sustainergy.ca
# psswrd: 66hello77

def call_file(file_name):
    with open(file_name, "r") as f:
        list_of_lines = [line.strip() for line in f]
    return list_of_lines


def call_api(serial_number, days ):
    # this is a test call to the api
    #output = subprocess.run('ls')
    #date_proc = subprocess.Popen(['date'], stdout=subprocess.PIPE)
    # this runs on the command line to run the EmporiaEnergyApiClient.java 
    # this file is compiled in the mains folder 
    str_days = str(days)
    string1 = "java -cp lib\*;. mains.EmporiaEnergyApiClient phart@sustainergy.ca P4iJBNrkx3BQ "+serial_number+" "+str_days+" partner-api.emporiaenergy.com"
    output = subprocess.Popen(string1, shell=True,stdout=subprocess.PIPE)
    #date_proc.stdout.close()

   
    st, s = output.communicate()
    # the returned sting is a long single string that is 
    slip = str(st)
    slip = slip.replace('\\n','\n')
    slip = slip.replace('\\t','\t')


    with open("Output.txt", "w") as text_file:
        for line in slip:
            
            text_file.write(line)
    with open("Output.txt", "r") as f:
        list_of_lines = [line.strip() for line in f]

    return list_of_lines





# this function returns a list of lists that is the usage of the device with the serial number given and in the format of 
# 1MIN 15MIN and 1H 
def get_usage(line_list, usage, serial_number):
    r = []
    channel_names = {}
    c = []
    for i in range(len(line_list)):
        s_list = line_list[i].split(' ')    
                  
        try:
            if s_list[0] == 'Usage:' and s_list[4].strip('\n') == usage and s_list[1] == serial_number:
                r.append(s_list)
                for j in line_list[i+1:]:
                    s2_list = j.split(' ')
                    if s2_list[0] == 'Usage:' or s2_list[0] == "'":
                        break
                    else:
                        r.append(s2_list)
        except:
            continue
    return r

def get_channel_names(line_list,serial_number):
    channel_names = {}
    
    for i in range(len(line_list)):
        s_list = line_list[i].split(' ')    
        try:
            if s_list[1] == 'devices:':
                number_of_devices = int(s_list[0])
                for d in range(number_of_devices):
                    
                    channel_line = line_list[i+(d+1)].split(';')
                    #channel_line = line_list[i+(d+1)]
                    # there is spances between the channel lines in the s3 so have to make a work around 
                    ll = 1 
                    count = 0
                    while ll == 1: 
                        if channel_line[0] == serial_number:
                            ll = 0
                            #channel_line = line_list[i+(d+1)].split(';')
                            #channel_line = line_list[i+(d+1)]
                            serial_n = channel_line[0]
                            serial_n = serial_n.replace(']', '')
                            serial_n = serial_n.replace('[', '')
                            serial_n = serial_n.replace(';', '')
                            channel_string = channel_line[8]
                            channel_string = channel_string.replace('Channels:', '')
                            channel_string = channel_string.replace(']','')
                            channel_string = channel_string.replace('[','')
                            channel_list = channel_string.split(',')
                    
                            for s in  range(len(channel_list)): 
                                channel_list[s] = channel_list[s].strip()
                            
                            channel_names[serial_n] = channel_list   

                        else:
                            channel_line = line_list[i+(d+1)+count].split(';')
                            count += 1
                            if count > 100000000:
                                return   
        except:
            pass 
    return channel_names


#this function take in a list from get_usage and makes it into a usabel pandas data frame 

def make_df(usage_list, channel_names,serial_number):
    time_list = []
    date_list = []
    channel_dict = {}
    
    for i in usage_list: 
        if i[0] == 'Usage:':
            serial_number = i[1]
            scale = i[4]
        else:
            # make the time formate better 
            time1 = i[0].strip('\t')
            time1 = time1.replace('T',' ')
            time1 = time1.replace('Z:', '')
            t = time1.split(' ')
            date = t[0]
            time = t[1]
            time_list.append(time)
            date_list.append(date)
            # get the number of channels 
            num_channel = int((len(i)-1)/3)

            
           
            # init the channel dict 
            if channel_dict == {}:
                key_duplicate_number = 0
                for e in range(num_channel):
                    e+=1
                    number = i[(e*3 - 1)]
                    number = number.strip('(')
                    number = number.strip(')')
                    #channel_string ='channel ' + number
                    channel_string = channel_names[serial_number][int(number) - 1]

                    # this is for repeat names 
                    # a dict cannot store duplicate names so it will add a number to the string
                    if channel_string in channel_dict:
                        channel_string = channel_string + ' ' + str(key_duplicate_number)
                        channel_names[serial_number][int(number) - 1] = channel_string
                        key_duplicate_number += 1 
                    channel_dict[channel_string] = []

            #[sherwood 2_1, sherwood 2_2, sherwood 2_3, paint booth lights, paint booth air dryers, paint booth air dryers, counter receptacle, counter receptacle, microwave , vacuum, vacuum, vacuum, vacuum, vacuum, vacuum, water heater , mezzanine receptacle , water softener and DHW, lunch room lights]
            for c in range(num_channel):
                c+=1
                number = i[(c*3 - 1)]
                number = number.strip('(')
                number = number.strip(')')
                #channel_string = 'channel ' + number
                channel_string = channel_names[serial_number][int(number) - 1]
                
                d = i[c*3].strip('\n')
                d = d.strip(';')
                channel_dict[channel_string].append(float(d))

    

    df = pd.DataFrame(channel_dict)
    df.insert(0, "date", date_list)
    df.insert(1,"time", time_list)
    
    # this line shows a basic plot of the data frame 
    #df.plot.line()
    #plt.show()

    # if want to return a data frame just comment out this line. 
    #dd = df.to_dict()
    #dd = df.values.tolist()
    return df

def get_serial_list(line_list):
    r = []
    channels = {}
    c = []
    for i in line_list:
        spit = i.split(' ')
        try:
            if spit[1] == 'devices:':
                for j in spit[2:]:
                    s_number = j
                    s_number = s_number.replace(']', '')
                    s_number = s_number.replace('[', '')
                    s_number = s_number.replace('\n', '')
                    r.append(s_number)
                                    
        except:
            continue

    return r


# this takes in the line list and then outputs the token ID
def get_token_id(l):
    token = l[1].split(' ')

    token_id = token[6].rstrip()

    return token_id






