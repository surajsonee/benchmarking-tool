from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import flask_excel as excel
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from sqlalchemy.orm import load_only
import time
import hashlib

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, FileField, SelectField, IntegerField


#docx templating shit
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage

from flask import Flask, send_file




from docx import Document
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage



from docx import Document
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage


import math
from sqlalchemy import desc
from flask import Blueprint,render_template,request,redirect,url_for,flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from ..models import *
from pathlib import Path
import requests
from benchmarking_tool.helper import *
from benchmarking_tool.forms import *
from benchmarking_tool.decorators import *
from benchmarking_tool.functions import *
import secrets
from PIL import Image
from difflib import get_close_matches
from benchmarking_tool.furnace_detect import *
from benchmarking_tool.pvc_steel_detect import *
from benchmarking_tool.image_reckognition.aws_rek import *
from benchmarking_tool.image_reckognition.bill_detection import *
from benchmarking_tool.methods import *
from datetime import datetime,timedelta
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
from sqlalchemy import delete
from flask_mobility.decorators import mobile_template, mobilized
from flask_mobility import Mobility
from flask import session
import csv
import operator
import boto3
import sys
import os
import pandas as pd
from flask_mail import Mail, Message
from benchmarking_tool.PartnerApiClient import *
import matplotlib.pyplot as plt
import pandas as pd
from benchmarking_tool.PartnerApiClient.Emporia_Customer import Emporia_Customer
from benchmarking_tool.report_functions import calendar_init, calendar_update, calendar_pull, calendar_edit, operating_hours
from benchmarking_tool.report_functions.edit_weekday_calendar import edit_weekday_calendar
from benchmarking_tool.channel_prediction.channel_predictions import *
from flaskext.mysql import MySQL
import mysql.connector
from collections import Counter, defaultdict
from calendar import monthrange
import calendar
import json  
import base64 
from random import randint
import urllib.request
import pdfkit
from weasyprint import HTML
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import make_response, send_from_directory
#for photo upload
commercial = Blueprint('commercial',__name__,template_folder='templates')
app_root = Path(__file__).parents[1]
root_path = os.path.dirname(os.path.abspath(__file__))


@commercial.route('/download', methods=['GET', 'POST'])
def download():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()

    if "iphone" in user_agent:
        return render_template('downloadmobile.html')
    
    else:
        return render_template('download.html')


@commercial.route('/sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='sw.js'))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response

@commercial.route('/testapi', methods=['GET', 'POST'])
@login_required
def testapi():
    bucket = "trialset"
    org = "33fb425a6047cad9"
    token = "UUH6z-JPugsamGgl6DvZm4W-7Gr3GGABGFulHKdPI-AbObSQVNta_FRlqFswKP7zPkWB5xboRznsaSJqGf5C0A=="
    # Store the URL of your InfluxDB instance
    url="https://us-east-1-1.aws.cloud2.influxdata.com"
    client = influxdb_client.InfluxDBClient(
       url=url,
       token=token,
       org=org
    )
    query_api = client.query_api()
    query = ' from(bucket:"trialset")\
        |> range(start: -30d)\
        |> filter(fn:(r) => r._measurement == "power1")\
        |> filter(fn: (r) => r._field == "value")'
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
      for record in table.records:
        results.append((record.get_field(), record.get_value(),record.get_time()))

    print(results)
    print('---------------')
    
    return render_template('testapi.html')



@commercial.route('/uploadpanels/<building_id>', methods=['GET', 'POST'])
@login_required
def uploadpanels(building_id):
    if(current_user.is_authenticated and current_user.is_admin()):
        form = UtilityForm()
        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="admin",
          password="rvqb2JymBB5CaNn",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        building_id = building_id
        error = False
        
        if request.method == "POST":
            file = request.files['file']
            filename = secure_filename(file.filename)
            print(filename)
            file.save(filename)
            xl_file = pd.ExcelFile(filename)
            dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
            panels = list(dfs.keys())
            for panel in panels:
                panelid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                sql = "INSERT INTO panel_data (panel_id, building_id, panel_name) VALUES (%s, %s, %s)"
                val = (panelid, building_id, panel)
                mycursor.execute(sql, val)


            for panel in panels:
                error = False
                sql = "SELECT panel_id FROM panel_data WHERE panel_name = %s AND building_id = %s"
                mycursor.execute(sql,(panel,building_id))
                myresult = mycursor.fetchall()
                try:
                    result = str(myresult[0])
                except:
                    continue
                result = result.replace('(','')
                result = result.replace(')','')
                result = result.replace(',','')
                result = result.replace("'",'')

                try:
                    row_number = list(dfs[panel]['Unnamed: 0'])
                except:
                    error = True
                if error:
                    try:
                        print(dfs[panel].keys())
                        row_number = list(dfs[panel][panel])
                    except:
                        row_number = list(dfs[panel][panel + " "])
                circuit_name = list(dfs[panel]['Unnamed: 1'])
                circuit_category = list(dfs[panel]['Unnamed: 2'])
                circuit_amps = list(dfs[panel]['Unnamed: 3'])
                try:
                    row_number.remove('row_number ')
                    circuit_name.remove('Circuit Name ')
                    circuit_category.remove('Circuit Category ')
                    circuit_amps.remove('Circuit Amps ')
                except:
                    error = 1
                for i in range(0,len(circuit_name)):
                    if str(circuit_name[i]) == 'nan' and str(circuit_category[i]) == 'nan' and str(circuit_amps[i]) == 'nan' and str(row_number[i]) == 'nan':
                        error = True
                    else:
                        circuitid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                        sql = "INSERT INTO circuit_data (id, panel_id, circuit_name, circuit_category, circuit_amps, row_numbers) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (circuitid, str(result), str(circuit_name[i]), str(circuit_category[i]),str(circuit_amps[i]), str(row_number[i]))
                        mycursor.execute(sql, val)
            mydb.commit()

        return render_template('uploadpanels.html', form = form)
    else:
        abort(403)



def strip_dict(d):
    """
    Strip all leading and trailing whitespace in dictionary keys and values.
    """
    return dict((k.strip(), v.strip()) for k, v in d.items())


@commercial.route('/usageday', methods=['GET', 'POST'])
@login_required
def usageday():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        print(customer.channel5.data_hour)
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-hours.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)

@commercial.route('/usageweek', methods=['GET', 'POST'])
@login_required
def usageweek():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-week.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)
@commercial.route('/usagemonth', methods=['GET', 'POST'])
@login_required
def usagemonth():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-month.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)
@commercial.route('/usagedayline', methods=['GET', 'POST'])
@login_required
def usagedayline():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        print(customer.channel7.data_hour)
        print(customer.channel8.data_hour)
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-hours-line.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)

@commercial.route('/usageweekline', methods=['GET', 'POST'])
@login_required
def usageweekline():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        print('hours')
        print(customer.chan_hours)
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-week-line.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)
@commercial.route('/usagemonthline', methods=['GET', 'POST'])
@login_required
def usagemonthline():
    if(current_user.is_authenticated and current_user.is_admin()):
        serial_number = 'A2107A04B4B8F009A6CEC4'
        customer = Emporia_Customer(serial_number)

        customer.get_data(days= 1)
        customer.get_schedule()

        customer.save_channels()
        exteriorwalls =[]
        roofs = []
        rooffinishs = []
        foundations = []
        home_upgrades = customer.channel7.data_hour
        home_upgrades1 = customer.channel8.data_hour
        home_upgrades3 = customer.channel6.data_hour
        home_upgrades4 = customer.channel10.data_hour
        home_upgrades5 = customer.channel5.data_hour
        home_upgrades6 = customer.channel8.data_hour
        user_home = [60, 50]
        average_home = [75,62]
        return render_template('usage-day-on-month-line.html',home_upgrades3 = home_upgrades3,home_upgrades4 = home_upgrades4,home_upgrades5 = home_upgrades5,home_upgrades6 = home_upgrades6,home_upgrades1 = home_upgrades1,user_home = user_home, average_home = average_home,home_upgrades = home_upgrades, roofs = roofs, exteriorwalls = exteriorwalls, rooffinishs = rooffinishs, foundations = foundations)
    else:
        abort(403)

@commercial.route('/energycost', methods=['GET', 'POST'])
@login_required
def energycost():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycost.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)
@commercial.route('/energycostlighting', methods=['GET', 'POST'])
@login_required
def energycostlighting():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycostlighting.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)

@commercial.route('/energycosthighbays', methods=['GET', 'POST'])
@login_required
def energycosthighbays():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycosthighbays.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)
@commercial.route('/energycostlinears', methods=['GET', 'POST'])
@login_required
def energycostlinears():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycostlinears.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)
@commercial.route('/energycosttroffers1x4', methods=['GET', 'POST'])
@login_required
def energycosttroffers1x4():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycosttroffers1x4.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)

@commercial.route('/energycosttroffers2x4', methods=['GET', 'POST'])
@login_required
def energycosttroffers2x4():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycosttroffers2x4.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)
@commercial.route('/energycostspotlights', methods=['GET', 'POST'])
@login_required
def energycostspotlights():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('energycostspotlights.html',light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)
@commercial.route('/facilitylist', methods=['GET', 'POST'])
@login_required
def facilitylist():
    if(current_user.is_authenticated and current_user.is_admin()):
        heating_usage = 40
        current_regress = 0
        light_usage = 20
        appliance_usage = 10
        ventilation_usage = 50
        dhw_usage = 30
        buildings = Building.query.filter_by(client_id = 1).all() 
        total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        return render_template('facilitylist.html',buildings = buildings,light_usage=light_usage,dhw_usage=dhw_usage, heating_usage = heating_usage,
        ventilation_usage = ventilation_usage,appliance_usage = appliance_usage,total = total)
    else:
        abort(403)

import numpy as np
import pandas as pd
import random 
import datetime


def get_seconds(minute, channel_names,serial_number):
    
    minutes = minute
    seconds = 60

    # need to init the column names 

    col_names = ['emporia_id',
        'emporia_building_id',
        'emporia_pannel_id',
        'date',
        'day',
        'hour',
        'minute',
        'second',
        'serial_number',
        'main1_name',
        'main1_usage',
        'main2_name',
        'main2_usage',
        'main3_name',
        'main3_usage',
        'channel4_name',
        'channel4_usage',
        'channel5_name',
        'channel5_usage',
        'channel6_name',
        'channel6_usage',
        'channel7_name',
        'channel7_usage',
        'channel8_name',
        'channel8_usage',
        'channel9_name',
        'channel9_usage',
        'channel10_name',
        'channel10_usage',
        'channel11_name',
        'channel11_usage',
        'channel12_name',
        'channel12_usage',
        'channel13_name',
        'channel13_usage',
        'channel14_name',
        'channel14_usage',
        'channel15_name',
        'channel15_usage',
        'channel16_name',
        'channel16_usage',
        'channel17_name',
        'channel17_usage',
        'channel18_name',
        'channel18_usage',
        'channel19_name',
        'channel19_usage']


    seconds_df = pd.DataFrame(columns=col_names)

    sec_dict = seconds_df.to_dict()

    single_row = sec_dict
    emporia_id = str(random.randrange(1000,9000))
    emporia_building_id = str(random.randrange(1000,9000))
    emporia_pannel_id = str(random.randrange(1000,9000))

    for m in range(minutes):
        for s in range(seconds):
            single_row['emporia_id'] = emporia_id
            single_row['emporia_building_id'] = emporia_building_id
            single_row['emporia_pannel_id'] = emporia_pannel_id
            date = datetime.datetime.now()
            single_row['date'] = str(date.year) + '-' + str(date.month)
            single_row['day'] = date.day
            single_row['hour'] = date.hour
            single_row['minute'] = m
            single_row['second'] = s
            single_row['serial_number'] = serial_number
            # now we have to do usage and channel names 
            channel_col = list(sec_dict.keys())
            channel_col = channel_col[9:]
            counter_n = 0
            counter_s = 0
            
            u = []
            for i in range(16):
                #gets a new usage list for every list 
                usage = float(random.randrange(0,2000))/100
                u.append(usage)


            for c in channel_col:
                
                # is it going to be a name or is it usage?
                if 'name' in c:
                    single_row[c] = channel_names[counter_n]
                    counter_n += 1
                if 'usage' in c:
                    #get a random number between 1 - 20
                    if 'main' in c:
                        # get the main 
                        single_row[c] = round(sum(u)/3,2)
                    else:
                        single_row[c] = u[counter_s]
                        counter_s += 1

            seconds_df = seconds_df.append(single_row,ignore_index=True)

            # comment this line out to not make a csv file 
            #seconds_df.to_csv('seconds_data.csv')

    return seconds_df

@commercial.route('/demo', methods=['GET', 'POST'])
@login_required
def demo():
    if(current_user.is_authenticated and current_user.is_admin()):
        return render_template('demo.html')
    else:
        abort(403)


@commercial.route('/facilityoverview/<building_id>', methods=['GET', 'POST'])
@login_required
def facilityoverview(building_id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client_id = current_user.phone_number
        building_id = building_id

        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            building_address = result[0]
            buidling_description = result[1]

        # mycursor = mydb.cursor()
        # sql = "SELECT emporia_meter_sn_1 FROM electrical_panel WHERE panel_client_id = %s AND building_id = %s"
        # mycursor.execute(sql,(client_id,building_id))
        # myresult = mycursor.fetchall()
        # for x in myresult:
        #     serial_numbers = ','.join(x)

        # total = 0
        # totalprice = 0
        # last = []
        # pricelast = []
        # paneltotal = []
        # panelpercent = []
        # circuitcount = []
        # panelcircuits =  pd.DataFrame()

        # serial_list = serial_numbers.split()
        # d = 1
        # customer = Emporia_Customer(serial_list[0])
        # customer.get_data(days= d)
        # customer.get_schedule()
        # customer.get_price_per_channel_hour(0.09)
        # price = customer.channel_cost_hour
        # h1, cat1, dat1 = customer.hour_category_usage()
        # price['panel name'] = 'Panel 1-A'
        # paneltotal.append(price['price per hour'].sum())
        # panelcircuits['Panel 1'] = price['circuit name']
        # circuitcount.append(len(price.index))

        # if(len(serial_list) > 1):    
        #     for i in range(1, len(serial_list)): 
        #         serial_number = serial_list[i]
        #         customer = Emporia_Customer(serial_list[i])
        #         customer.get_data(days= d)
        #         customer.get_schedule()
        #         customer.get_price_per_channel_hour(0.09)
        #         h2, cat2, dat2 = customer.hour_category_usage()
        #         appendprice = customer.channel_cost_hour
        #         appendprice['panel name'] = 'Panel 1-B'
        #         panelcircuits['Panel 2'] = appendprice['circuit name']
        #         paneltotal.append(appendprice['price per hour'].sum())
        #         price = price.append(appendprice, ignore_index = True)
        #         circuitcount.append(len(appendprice.index))
        # price = price.sort_values(by=['price per hour'], ascending=False)
        # home_upgrades = price.copy()
        # home_upgrades['price per hour'] = home_upgrades['price per hour']/(0.09*60*0.000017)
        # for i in range(len(paneltotal)):
        #     paneltotal[i] = paneltotal[i]/(0.09*60*0.000017)
        
        # h1 = Counter(h1)
        # h2 = Counter(h2)
        # categoryusage = h1 + h2
        # channel_names = home_upgrades['circuit name']
        # categories = []
        # for name in channel_names:
            
        #     # make everything lowercase 
        #     name_l = name.lower()
        #     if 'light' in name_l or 'lights' in name_l or 'lighting' in name_l:
        #         categories.append('lighting')

        #     elif 'hot water' in name_l or 'dhw' in name_l or 'water' in name_l or 'water heater' in name_l:
        #         categories.append('hotwater')

        #     elif 'fan' in name_l or 'heat' in name_l or 'hvac' in name_l or 'cooling' in name_l:
        #         categories.append('hvac')

        #     elif 'motor' in name_l or 'pump' in name_l or 'compressor' in name_l or 'vacuum' in name_l or 'dryer' in name_l:
        #         categories.append('equipment')
            
        #     elif 'plug' in name_l or 'plugs' in name_l or 'receptacle' in name_l or 'receptacle' in name_l:
        #         categories.append('plugload')
            
        #     else:
        #         categories.append('other')
        # home_upgrades['Category'] = categories
        # price["Category"] = categories
        # lighttotal = 0
        # watertotal = 0
        # hvactotal = 0
        # equipmenttotal = 0
        # plugtotal = 0
        # othertotal = 0
        # lightprice = 0
        # waterprice = 0
        # hvacprice = 0
        # equipmentprice = 0
        # plugprice = 0
        # otherprice = 0
        # home_upgrades['price per hour'] = home_upgrades['price per hour'].round(2)
        # categorytotals = home_upgrades.copy()
        # pricecategorytotals = price.copy()
        # for i in range(0,len(categorytotals.index)):
            
        #     # make everything lowercase 
        #     name_l = name.lower()
        #     if categorytotals.iloc[i][5] == 'lighting':
        #         lighttotal += categorytotals.iloc[i][2]

        #     elif categorytotals.iloc[i][5] == 'hotwater':
        #         watertotal += categorytotals.iloc[i][2]

        #     elif categorytotals.iloc[i][5] == 'hvac':
        #         hvactotal += categorytotals.iloc[i][2]

        #     elif categorytotals.iloc[i][5] == 'equipment':
        #         equipmenttotal += categorytotals.iloc[i][2]
            
        #     elif categorytotals.iloc[i][5] == 'plugload':
        #         plugtotal += categorytotals.iloc[i][2]
            
        #     else:
        #         othertotal += categorytotals.iloc[i][2]

        # for i in range(0,len(pricecategorytotals.index)):
            
        #     # make everything lowercase 
        #     name_l = name.lower()
        #     if pricecategorytotals.iloc[i][5] == 'lighting':
        #         lightprice += pricecategorytotals.iloc[i][2]

        #     elif pricecategorytotals.iloc[i][5] == 'hotwater':
        #         waterprice += pricecategorytotals.iloc[i][2]

        #     elif pricecategorytotals.iloc[i][5] == 'hvac':
        #         hvacprice += pricecategorytotals.iloc[i][2]

        #     elif pricecategorytotals.iloc[i][5] == 'equipment':
        #         equipmentprice += pricecategorytotals.iloc[i][2]
            
        #     elif pricecategorytotals.iloc[i][5] == 'plugload':
        #         plugprice += pricecategorytotals.iloc[i][2]
            
        #     else:
        #         otherprice += pricecategorytotals.iloc[i][2]


        # for total in paneltotal:
        #     num = (total/sum(paneltotal)) * 100
        #     num = round(num, 2)
        #     panelpercent.append(num)


        # percenttotal = home_upgrades['price per hour'].sum()
        # lightpercent = (lighttotal/percenttotal) * 100
        # waterpercent = (watertotal/percenttotal) * 100
        # hvacpercent = (hvactotal/percenttotal) * 100
        # equipmentpercent = (equipmenttotal/percenttotal) * 100
        # plugpercent = (plugtotal/percenttotal) * 100
        # otherpercent = (othertotal/percenttotal) * 100
        # total = home_upgrades['price per hour'].sum()
        # totalprice = price['price per hour'].sum()
        # colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']
        # numpanels = home_upgrades['panel name'].nunique()
        # panelnames = home_upgrades['panel name'].unique()
        # panelnames = sorted(panelnames)
        # categoriesdf = {'Name':['Lighting','Hot Water','HVAC','Equipment','Plug Load','Other'],'Totals':[lighttotal,watertotal,hvactotal,equipmenttotal,plugtotal,othertotal], 'Colors':['#3649A8','#A6D06D','#EE5937','#3BCDEE','#EE8F37','#DBE2F3'], 'Prices':[lightprice,waterprice,hvacprice,equipmentprice,plugprice,otherprice], 'Charts':['chartLight','chartWater','chartHVAC','chartEquipment','chartPlug','chartOther']}
        # categoriesdf = pd.DataFrame(data=categoriesdf)
        # categoriesdf = categoriesdf.sort_values(by=['Totals'], ascending=False)
        # categoriesdf = categoriesdf.round(2)
        # for i in range(len(paneltotal)):
        #    paneltotal[i] = round(paneltotal[i],2)
        #    panelpercent[i] = round(panelpercent[i],2)
        # print(home_upgrades)

        panel_ids = []
        panel_names = []
        circuit_names = []
        circuit_categories = []
        circuit_name_groups = []
        circuit_category_groups =[]
        panel_name_ids =[]

        sql = "SELECT panel_id, panel_name FROM panel_data WHERE building_id = %s"
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            panel_ids.append(result[0])
            panel_names.append(result[1])

        for panel in panel_ids:
            sql = "SELECT circuit_name, circuit_category FROM circuit_data WHERE panel_id = %s"
            mycursor.execute(sql,(panel,))
            myresult = mycursor.fetchall()
            current_panel = []
            current_category = []
            for result in myresult:
                circuit_names.append(result[0])
                current_panel.append(result[0])
                circuit_categories.append(result[1])
                current_category.append(result[1])

            circuit_name_groups.append(current_panel)
            circuit_category_groups.append(current_category)


        bucket = "trialset"
        org = "33fb425a6047cad9"
        token = "UUH6z-JPugsamGgl6DvZm4W-7Gr3GGABGFulHKdPI-AbObSQVNta_FRlqFswKP7zPkWB5xboRznsaSJqGf5C0A=="
        # Store the URL of your InfluxDB instance
        url="https://us-east-1-1.aws.cloud2.influxdata.com"
        client = influxdb_client.InfluxDBClient(
           url=url,
           token=token,
           org=org
        )
        query_api = client.query_api()
        query = ' from(bucket:"trialset")\
            |> range(start: -7d)\
            |> sort(columns: ["_time"])\
            |> top(n:1)\
            |> filter(fn:(r) => r._measurement == "power")\
            |> filter(fn: (r) => r._field == "value")'
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
          for record in table.records:
            results.append(record.get_value())

        query_api = client.query_api()
        query = ' from(bucket:"trialset")\
            |> range(start: -7d)\
            |> sort(columns: ["_time"])\
            |> top(n:1)\
            |> filter(fn:(r) => r._measurement == "power1")\
            |> filter(fn: (r) => r._field == "value")'
        result = query_api.query(org=org, query=query)
        for table in result:
          for record in table.records:
            results.append(record.get_value())

        query_api = client.query_api()
        query = ' from(bucket:"trialset")\
            |> range(start: -7d)\
            |> sort(columns: ["_time"])\
            |> top(n:1)\
            |> filter(fn:(r) => r._measurement == "power2")\
            |> filter(fn: (r) => r._field == "value")'
        result = query_api.query(org=org, query=query)
        for table in result:
          for record in table.records:
            results.append(record.get_value())

        names = ['power', 'power1', 'power2']
        total = sum(results)

        for panel in panel_names:
            newpanel = panel
            newpanel = newpanel.replace(' ', '')
            newpanel = newpanel.replace('"', '')
            newpanel = newpanel.replace("'", '')
            newpanel = newpanel.replace("(", '')
            newpanel = newpanel.replace(")", '')
            panel_name_ids.append(newpanel)
        user_agent = request.headers.get('User-Agent')
        user_agent = user_agent.lower()
        if "iphone" in user_agent or "android" in user_agent:
            return render_template('facilityoverviewmobile.html',panel_name_ids=panel_name_ids,circuit_name_groups=circuit_name_groups,circuit_category_groups=circuit_category_groups,circuit_categories=circuit_categories,circuit_names=circuit_names,panel_names=panel_names,total = total,results=results,names=names,building_address = building_address, buidling_description = buidling_description, building_id = building_id) #,categoriesdf = categoriesdf,panelpercent = panelpercent, panelcircuits = panelcircuits,circuitcount = circuitcount,paneltotal = paneltotal,panelnames = panelnames,numpanels = numpanels,colours = colours,lightpercent = lightpercent,waterpercent = waterpercent,hvacpercent = hvacpercent,equipmentpercent = equipmentpercent,plugpercent = plugpercent,otherpercent = otherpercent,lightprice = lightprice,waterprice = waterprice,hvacprice = hvacprice,equipmentprice = equipmentprice,plugprice = plugprice,otherprice = otherprice,lighttotal = lighttotal,watertotal = watertotal,hvactotal = hvactotal,equipmenttotal = equipmenttotal,plugtotal = plugtotal,othertotal = othertotal,categoryusage = categoryusage, pricelength = len(price.index),totalprice = totalprice, price = price,channellength = len(channel_name), lasts = len(last),last = last, len = len(home_upgrades.index), home_upgrades = home_upgrades,channel_name = channel_name,total = total)
        else:
            return render_template('facilityoverview.html',panel_name_ids=panel_name_ids,circuit_name_groups=circuit_name_groups,circuit_category_groups=circuit_category_groups,circuit_categories=circuit_categories,circuit_names=circuit_names,panel_names=panel_names,total = total,results=results,names=names,building_address = building_address, buidling_description = buidling_description, building_id = building_id) #,categoriesdf = categoriesdf,panelpercent = panelpercent, panelcircuits = panelcircuits,circuitcount = circuitcount,paneltotal = paneltotal,panelnames = panelnames,numpanels = numpanels,colours = colours,lightpercent = lightpercent,waterpercent = waterpercent,hvacpercent = hvacpercent,equipmentpercent = equipmentpercent,plugpercent = plugpercent,otherpercent = otherpercent,lightprice = lightprice,waterprice = waterprice,hvacprice = hvacprice,equipmentprice = equipmentprice,plugprice = plugprice,otherprice = otherprice,lighttotal = lighttotal,watertotal = watertotal,hvactotal = hvactotal,equipmenttotal = equipmenttotal,plugtotal = plugtotal,othertotal = othertotal,categoryusage = categoryusage, pricelength = len(price.index),totalprice = totalprice, price = price,channellength = len(channel_name), lasts = len(last),last = last, len = len(home_upgrades.index), home_upgrades = home_upgrades,channel_name = channel_name,total = total)
    else:
        abort(403)
     
@commercial.route('/liveusage/<building_id>', methods=['GET', 'POST'])
@login_required
def liveusage(building_id):
    if(current_user.is_authenticated and current_user.is_admin()):
        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            building_address = result[0]
            buidling_description = result[1]

        weather_list = []
        url = "http://api.weatherapi.com/v1/forecast.json?key=237335d4c72f474a85a202934220902&q=Edgerton&days=1&aqi=no&alerts=no"
        file = urllib.request.urlopen(url)

        for line in file:
            weather_list.append(line.decode("utf-8"))
        
        data = json.loads(weather_list[0])
        now = datetime.datetime.now()
        temp = data['forecast']['forecastday'][0]['hour'][now.hour]["temp_c"]
        return render_template('liveusage.html',temp = temp,building_address = building_address, buidling_description = buidling_description, building_id = building_id)
    else:
        abort(403)



@commercial.route('/energymanagement/<building_id>', methods=['GET', 'POST'])
@login_required
def energymanagement(building_id):
    if(current_user.is_authenticated and current_user.is_admin()):
        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            building_address = result[0]
            buidling_description = result[1]


        return render_template('energymanagement.html',building_address = building_address, buidling_description = buidling_description, building_id = building_id)
    else:
        abort(403)


@commercial.route('/energycalendar/<building_id>', methods=['GET', 'POST'])
@login_required
def energycalendar(building_id):
    form = EnergyCalendarForm()
    building_id = building_id
    paneltotal = []
    panelpercent = []
    scheduledata = []
    channelNames = []
    lightingTotal =[]
    hvacTotal = []
    dhwTotal = []
    equipmentTotal = []
    plugloadTotal = []
    otherTotal = []
    currentLight = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentHvac = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentDhw = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentPlug = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentEquipment = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentOther = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    day = datetime.datetime.now().day
    cal_month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    building_ids = 12
    error = None
    newMonth = 'Jan'
    userYear = 2022

    if(current_user.is_authenticated and current_user.is_admin()):
        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            building_address = result[0]
            buidling_description = result[1]

        client_id = current_user.phone_number
        panel_building_id = building_id
        mycursor = mydb.cursor()
        sql = "SELECT emporia_meter_sn_1 FROM electrical_panel WHERE panel_client_id = %s AND building_id = %s"
        mycursor.execute(sql,(client_id,panel_building_id))
        myresult = mycursor.fetchall()
        for x in myresult:
            serial_numbers = ','.join(x)
        serial_list = serial_numbers.split()

        date_list = []
        start_date = datetime.date(2022, 1, 1)
        number_of_days = 31
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        daystart = 6
        realdaystart = 6
        dayend = 32
        if request.method == "POST":
            userMonth = request.form['month']
            newMonth = userMonth
            userYear = request.form['year']
            print(userYear)
            for i in range(0, len(months)):
                if months[i] == userMonth:
                    userMonth = i + 1
            start_date = start_date.replace(year = int(userYear), month = userMonth)
            first_weekday, number_of_days = calendar.monthrange(int(userYear), userMonth)
            realdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
            for i in range(0, len(realdays)):
                if realdays[i] == calendar.day_name[first_weekday]:
                    daystart = i
                    realdaystart = i
                    dayend = number_of_days + 1
        print(number_of_days)
        for day in range(number_of_days):
          a_date = (start_date + datetime.timedelta(days = day)).isoformat()
          date_list.append(a_date + ' 00:00:00')
        totallist = []
        for day in date_list:
            currentTotal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for serialNumber in serial_list:
                string = ''
                sql = "SELECT channel4_schedule, channel5_schedule, channel6_schedule, channel7_schedule, channel8_schedule, channel9_schedule, channel10_schedule, channel11_schedule, channel12_schedule, channel13_schedule, channel14_schedule, channel15_schedule, channel16_schedule, channel17_schedule, channel18_schedule, channel19_schedule FROM emporia_data WHERE date LIKE %s AND serial_number = %s"   
                mycursor.execute(sql, (day, serialNumber))
                myresult = mycursor.fetchall()
                for x in myresult:
                    string = "', '".join(x)
                    scheduledata = string.split("', '")

                    for data in scheduledata:
                        data = data.replace("[","")
                        data = data.replace("]","")
                        dataList = data.split(',')
                        for i in range(0, len(dataList)):
                            try:
                                currentTotal[i] += float(dataList[i])
                            except:
                                currentTotal[i] += 0
                    
                channelNames = []
                sql = "SELECT channel4_name,channel5_name,channel6_name,channel7_name,channel8_name,channel9_name,channel10_name,channel11_name,channel12_name,channel13_name,channel14_name,channel15_name,channel16_name,channel17_name,channel18_name,channel19_name FROM emporia_data WHERE date LIKE %s AND serial_number = %s"
                    
                mycursor.execute(sql, (day, serialNumber))
                myresult = mycursor.fetchall()
                for x in myresult:
                    string = str(x)
                    string = string.replace("(","")
                    string = string.replace(")","")
                    string = string.split(',')
                    for i in range(0, len(string)):
                        channelNames.append(string[i])
                for i in range(0,len(channelNames)):
                
                    name_l = channelNames[i].lower()

                    if 'light' in name_l or 'lights' in name_l or 'lighting' in name_l:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentLight[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentLight[i] += 0
                    elif 'hot water' in name_l or 'dhw' in name_l or 'water' in name_l or 'water heater' in name_l:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentDhw[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentDhw[i] += 0

                    elif 'fan' in name_l or 'heat' in name_l or 'hvac' in name_l or 'cooling' in name_l:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentHvac[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentHvac[i] += 0
                        

                    elif 'motor' in name_l or 'pump' in name_l or 'compressor' in name_l or 'vacuum' in name_l or 'dryer' in name_l:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentEquipment[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentEquipment[k] += 0
                    
                    elif 'plug' in name_l or 'plugs' in name_l or 'receptacle' in name_l or 'receptacle' in name_l:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentPlug[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentPlug[k] += 0
                    
                    else:
                        scheduledata[i] = scheduledata[i].replace("[","")
                        scheduledata[i] = scheduledata[i].replace("]","")
                        for k in range(0, len(scheduledata[i].split(','))):
                            try:
                                currentOther[k] += float((scheduledata[i].split(','))[k])
                            except:
                                currentOther[k] += 0
            lightingTotal.append(currentLight)
            hvacTotal.append(currentHvac)
            dhwTotal.append(currentDhw)
            equipmentTotal.append(currentEquipment)
            plugloadTotal.append(currentPlug)
            otherTotal.append(currentOther)
            totallist.append(currentTotal)
            currentLight = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            currentHvac = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            currentDhw = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            currentPlug = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            currentEquipment = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            currentOther = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        startTime = 9
        endTime = 17
        a_file =  open('benchmarking_tool/static/scripts/data-calender.json', 'r')
        json_object = json.load(a_file)
        a_file.close()
       
        weeks = ['firstweek' , 'secondweek', 'thirdWeek' , 'fourthweek', 'fifthweek']
        days = ['sunday','monday','tuesday','wednsday','thursday','friday','saturday']

        for alist in totallist:
            for i in range(0,len(alist)):
                if math.isnan(alist[i]) == True:
                    alist[i] = 0
                else:
                    alist[i] = alist[i]/1000
        i = 0
        numday = 1
        print(totallist[22])
        for thing in json_object:
            for j in range(0, daystart):
                thing[weeks[i]][days[j]]['value'] = ''
                thing[weeks[i]][days[j]]['totalValue'] = ''
                thing[weeks[i]][days[j]]['numDay'] = ''
            
            for k in range(daystart,len(days)):
                try:
                    thing[weeks[i]][days[k]]['value'] = totallist[numday - 1]
                    thing[weeks[i]][days[k]]['totalValue'] = "{:.2f}".format(sum(totallist[numday - 1]))
                    thing[weeks[i]][days[k]]['numDay'] = numday

                
                except:
                    thing[weeks[i]][days[k]]['value'] = ''
                    thing[weeks[i]][days[k]]['totalValue'] = ''
                    thing[weeks[i]][days[k]]['numDay'] = ''
                numday += 1

            daystart = 0
            i += 1
        with open('benchmarking_tool/static/scripts/data-calender.json', 'w') as f:
            json.dump(json_object, f)
        costTotal = []
        costList = []
        for data in totallist:
            currentCost = []
            for i in range(0, len(data)):
                currentCost.append((data[i] * 0.09))

            costTotal.append(round(sum(currentCost), 2))
            costList.append(currentCost)

        energyTotal = []
        currentEnergy = []
        for data in totallist:
            currentEnergy = []
            for i in range(0, len(data)):
                currentEnergy.append((data[i]))


            energyTotal.append(round(sum(currentEnergy), 2))

        lightTotals = []
        lightCost = []
        for data in lightingTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            lightTotals.append(round(sum(currentLight)/1000, 2))
            lightCost.append(round(sum(currentCost)/1000, 2))
        hvacTotals = []
        hvacCost = []
        for data in hvacTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            hvacTotals.append(round(sum(currentLight)/1000, 2))
            hvacCost.append(round(sum(currentCost)/1000, 2))
        dhwTotals = []
        dhwCost = []
        for data in dhwTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            dhwTotals.append(round(sum(currentLight)/1000, 2))
            dhwCost.append(round(sum(currentCost)/1000, 2))
        plugTotals = []
        plugCost = []
        
        for data in plugloadTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            plugTotals.append(round(sum(currentLight)/1000, 2))
            plugCost.append(round(sum(currentCost)/1000, 2))
        equipmentTotals = []
        equipmentCost = []
        
        for data in equipmentTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            equipmentTotals.append(round(sum(currentLight)/1000, 2))
            equipmentCost.append(round(sum(currentCost)/1000, 2))
        otherTotals = []
        otherCost = []
        for data in otherTotal:
            currentLight = []
            currentCost = []
            for i in range(0, len(data)):
                if data[i] != data[i]:
                    data[i] = 0
                currentLight.append((data[i]))
                currentCost.append((data[i] * 0.09))

            otherTotals.append(round(sum(currentLight)/1000, 2))
            otherCost.append(round(sum(currentCost)/1000, 2))

        totalEnergy = round(sum(energyTotal), 2)
        totalCost = round(sum(costTotal), 2)
        totalLights = round(sum(lightTotals), 2)
        totalHVAC = round(sum(hvacTotals), 2)
        totalDHW = round(sum(dhwTotals), 2)
        totalEquipment = round(sum(equipmentTotals), 2)
        totalPlug = round(sum(plugTotals), 2)
        totalOther = round(sum(otherTotals), 2)

        onTotal = []
        onCost = []
        currentOn = []
        onTotalEnergy = 0
        onTotalCost = 0
        for data in totallist:
            currentOn = []
            for i in range(0, len(data)):
                if i >= startTime and i < endTime:
                    currentOn.append((data[i]))


            onTotal.append(round(sum(currentOn), 2))
            onCost.append(round((sum(currentOn) * 0.09), 2))
        onTotalEnergy = round(sum(onTotal), 2)
        onTotalCost = round(sum(onCost), 2)

        offTotal = []
        offCost = []
        currentOff = []
        offTotalEnergy = 0
        offTotalCost = 0
        for data in totallist:
            currentOff = []
            for i in range(0, len(data)):
                if i < startTime or i >= endTime:
                    currentOff.append((data[i]))


            offTotal.append(round(sum(currentOff), 2))
            offCost.append(round((sum(currentOff) * 0.09), 2))
        offTotalEnergy = round(sum(offTotal), 2)
        offTotalCost = round(sum(offCost), 2)

        return render_template('energycalendar.html',onTotalEnergy = onTotalEnergy, offTotalEnergy = offTotalEnergy, offTotalCost = offTotalCost, onTotalCost = onTotalCost, onCost = onCost, offCost = offCost, offTotal = offTotal, onTotal = onTotal, userYear = userYear, newMonth = newMonth, form = form, totalCost=totalCost,totalLights=totalLights,totalHVAC=totalHVAC,totalDHW=totalDHW,totalEquipment=totalEquipment,totalPlug=totalPlug,totalOther=totalOther,totalEnergy=totalEnergy,lightCost = lightCost, equipmentCost = equipmentCost, dhwCost = dhwCost, hvacCost = hvacCost, otherCost = otherCost,plugCost = plugCost, otherTotal=otherTotal,plugloadTotal=plugloadTotal,equipmentTotal=equipmentTotal,dhwTotal=dhwTotal,hvacTotal=hvacTotal,lightingTotal=lightingTotal,currentLight=currentLight,lightTotals = lightTotals,hvacTotals=hvacTotals,otherTotals=otherTotals,equipmentTotals=equipmentTotals,plugTotals=plugTotals,dhwTotals=dhwTotals,startTime = startTime, endTime = endTime, costList=costList,totallist = totallist,energyTotal = energyTotal,dayend = dayend, realdaystart = realdaystart, costTotal = costTotal, building_address = building_address, buidling_description = buidling_description,building_id = building_id)
    else:
        abort(403)

@commercial.route('/facilityoverviewbubble', methods=['GET', 'POST'])
@login_required
def facilityoverviewbubble():
    if(current_user.is_authenticated and current_user.is_admin()):
        # if(current_user.id == 1):
        #     prine('1')
        #     channel_name = ['main sherwood 1_1', 'main sherwood 1_2', 'main sherwood 1_3', 'Dryer', 'Dryer', 'washer', 'car wash GFI Receptacle', 'Exterior receptacle' , 'Tube Heaters', 'Carwash GFI Receptacle', 'exterior receptacle' , 'SAPRE to car wash', 'wash bay door and heat' , 'wash bay door and heat' , 'wash bay door and heat' , 'wash bay receptacle' , 'car wash exhaust fan', 'exterior receptacle' , 'wash bay receptacle' ]
        #     serial_number = 'A2107A04B4AC67B2F76F18'
        # else:
        #     print('else')
        #     channel_name = ['main sherwood 2_1', 'main sherwood 2_2', 'main sherwood 2_3', 'paint booth lights', 'paint booth air dryers', 'paint booth air dryers', 'counter receptacle', 'counter receptacle', 'microwave' , 'vacuum', 'vacuum', 'vacuum', 'vacuum', 'vacuum', 'vacuum', 'water heater' , 'mezzanine receptacle' , 'water softener and DHW', 'lunch room lights']
        #     serial_number = 'A2108A04B4AC67B2F6A400'

        # #df_usage1 = get_seconds(2, channel_names1, serial_number1)
        # serial_number = 'A2107A04B4B8F009A6CEC4'
        # d = 5

        # # new way of using the new data
        # customer = Emporia_Customer(serial_number)

        # customer.get_data(days= d)
        # home_upgrades = customer.chan_min
        # home_upgrades1 = customer.channel2.data_min
        # home_upgrades3 = customer.channel4.data_min
        # home_upgrades4 = customer.channel7.data_min
        # home_upgrades5 = customer.channel8.data_min
        # home_upgrades6 = customer.channel9.data_min
        # df_usage = get_seconds(2, channel_name, serial_number)
        # heating_usage = 40
        # current_regress = 0
        # light_usage = 20
        # appliance_usage = 10
        # ventilation_usage = 50
        # dhw_usage = 30
        # buildings = Building.query.filter_by(client_id = 1).all() 
        # total = heating_usage + light_usage + appliance_usage + ventilation_usage + dhw_usage
        # heating_percent = int(heating_usage / total * 100)
        # light_percent = int(light_usage / total * 100)
        # appliance_percent = int(appliance_usage / total * 100)
        # ventilation_percent = int(ventilation_usage / total * 100)
        # dhw_percent = int(dhw_usage / total * 100)
        return render_template('facilityoverviewbubble.html')
    else:
        abort(403)


@commercial.route('/', methods=['GET', 'POST'])
@commercial.route('/switchfacilities', methods=['GET', 'POST'])
@login_required
def switchfacilities():
    client_id = current_user.phone_number
    buildingIds = []
    buildingAddresses = []
    buildingDescriptions = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )

    mycursor = mydb.cursor()
    # sql = "SELECT idbuildings, address, description FROM buildings WHERE client_id = %s"
        
    # mycursor.execute(sql,(client_id,))
    # myresult = mycursor.fetchall()
    # for result in myresult:
    #     buildingIds.append(result[0])
    #     buildingAddresses.append(result[1])
    #     buildingDescriptions.append(result[2])
    sql = "SELECT idbuildings, address, description FROM buildings WHERE client_id = %s"
        
    mycursor.execute(sql,('f165de5b',))
    myresult = mycursor.fetchall()
    for result in myresult:
        buildingIds.append(result[0])
        buildingAddresses.append(result[1])
        buildingDescriptions.append(result[2])
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    if "iphone" in user_agent or "android" in user_agent:
        return render_template('switchfacilitiesmobile.html', buildingIds = buildingIds, buildingAddresses = buildingAddresses, buildingDescriptions = buildingDescriptions, numBuildings = len(buildingIds))
    else:
        return render_template('switchfacilities.html', buildingIds = buildingIds, buildingAddresses = buildingAddresses, buildingDescriptions = buildingDescriptions, numBuildings = len(buildingIds))

@commercial.route('/gaspage/<building_id>', methods=['GET', 'POST'])
@login_required
def gaspage(building_id):
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]

    return render_template('gaspage.html',building_address = building_address, buidling_description = buidling_description, building_id = building_id)

@commercial.route('/electricalpage/<building_id>', methods=['GET', 'POST'])
@login_required
def electricalpage(building_id):
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]


    return render_template('electricalpage.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id)

@commercial.route('/electricalgraph/<building_id>', methods=['GET', 'POST'])
@login_required
def electricalgraph(building_id):
    form = UtilityForm()
    path = '/uploads/'
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT yearlyGas FROM utilities WHERE id = 1"
        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    gasdata = tempstring.split(',')

    mycursor = mydb.cursor()
    sql = "SELECT yearlyElectrical FROM utilities WHERE year = 2017"
        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    electricaldata = tempstring.split(',')


    if request.method == "POST":
        electricaldata = []
        gasdata = []
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(filename)
        xl_file = pd.ExcelFile(filename)

        dfs = {sheet_name: xl_file.parse(sheet_name) 
                  for sheet_name in xl_file.sheet_names}
        electricdf = dfs['Electricity']
        electricdf = electricdf.fillna('nan')
        electricaldata2 = electricdf.iloc[:, 8].to_list()
        print(electricdf)
        for i in range(len(electricaldata2)):
            if electricaldata2[i] != 'nan' and electricaldata2[i] != 'Total':
                electricaldata.append(electricaldata2[i])
        
        naturalgasdf = dfs['Natural Gas']
        naturalgasdf = naturalgasdf.fillna('nan')
        gasdata2 = naturalgasdf.iloc[:, -1].to_list()
        for i in range(len(gasdata2)):
            if gasdata2[i] != 'nan' and gasdata2[i] != 'Total':
                gasdata.append(gasdata2[i])

        for i in range(len(electricaldata) - 12):
            electricaldata.pop()
        for i in range(len(gasdata) - 12):
            gasdata.pop()


        for i in range(len(gasdata)):
            electricaldata[i] = str(electricaldata[i])
            gasdata[i] = str(gasdata[i])

        gasstring = ','.join(gasdata)
        electricalstring = ','.join(electricaldata)
        year  = (electricdf.columns.to_list())[0]
        sql = "UPDATE utilities SET yearlyElectrical = %s, yearlyGas = %s WHERE id = 1"
        val = (electricalstring, gasstring)
        mycursor.execute(sql, val)

        mydb.commit()

    return render_template('Electrical-Histroy.html',building_address = building_address, buidling_description = buidling_description, building_id=building_id,form = form, electricaldata = electricaldata, gasdata= gasdata)



@commercial.route('/solarpage/<building_id>', methods=['GET', 'POST'])
@login_required
def solarpage(building_id):
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]

    return render_template('solarpage.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id)

@commercial.route('/solarspecs/<building_id>', methods=['GET', 'POST'])
@login_required
def solarspecs(building_id):
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT number_of_panels, watts_per_panel,panel_type,panel_loss FROM solar_data WHERE building_id = %s"
    val = (building_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        number_of_panels = result[0]
        watts_per_panel = result[1]
        panel_type = result[2]
        panel_loss = result[3]
    panel_loss = panel_loss.split(',')
    print(number_of_panels)
    

    return render_template('solarspecs.html',building_address = building_address, buidling_description = buidling_description,panel_loss=panel_loss,number_of_panels=int(number_of_panels),watts_per_panel=int(watts_per_panel),panel_type=panel_type,building_id=building_id)

@commercial.route('/solarproduction/<building_id>', methods=['GET', 'POST'])
@login_required
def solarproduction(building_id):

    square_footage = 209040
    panel_sqft = 19.5
    solar_pannel_wattage = 400
    hours_of_sunlight = randint(3, 18)
    kwh_price = 0.09
    weather_list = []
    url = "http://api.weatherapi.com/v1/forecast.json?key=237335d4c72f474a85a202934220902&q=Edgerton&days=1&aqi=no&alerts=no"
    file = urllib.request.urlopen(url)

    for line in file:
        weather_list.append(line.decode("utf-8"))
    
    data = json.loads(weather_list[0])
    


    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]

    mycursor = mydb.cursor()
    sql = "SELECT number_of_panels, panel_width, panel_height FROM solar_data WHERE building_id = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        numPanels = result[0]
        width = result[1]
        height = result[2]



    print(numPanels)
    a_file =  open('benchmarking_tool/static/scripts/solardata.json', 'r')
    json_object = json.load(a_file)
    a_file.close()

    hourslist = ['twlveAM','oneAM','twoAM','threeAM','fourAM','fiveAM','sixAM','sevenAM','eightAM','nineAM','tenAM','elevenPM','twlvePM','onePM','twoPM','threePM','fourPM','fivePM','sixPM','sevenPM','eightPM','ninePM','tenPM','elevnPM']
    hournumberlist = ['12am', '1am', '2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']

    k = 0
    over12 = False
    for i in range(0,len(hourslist)):
        for thing in json_object[hourslist[i]]:
            hours_of_sunlight = randint(1, k + 1)
            energy = 104*(data['forecast']['forecastday'][0]['hour'][i]['uv']) - 18.365
            icon = data['forecast']['forecastday'][0]['hour'][i]['condition']['icon']
            temp = data['forecast']['forecastday'][0]['hour'][i]["temp_c"]
            solarenergy = (energy * (float(width) * float(height))) * float(numPanels)
            thing['dataWeather'] = {"hour":hournumberlist[i],"degree" : temp,"kwh":"{:.2f}".format(solarenergy/1000),"icon":"<img src=" + icon + ">","value":"{:.2f}".format(solarenergy/5000)}
            if k > 12:
                k -= 1
                over12 = True
            elif k <= 12 and over12 == False:
                k += 1
            else:
                k -= 1
            thing['consumption'] = {'value': solarenergy/5000, 'status': 'ON'}
    a_file = open('benchmarking_tool/static/scripts/solardata.json', "w")
    json.dump(json_object, a_file)
    a_file.close()

    return render_template('solarproduction.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id)





def solar_calc(square_footage, panel_sqft, solar_pannel_wattage, hours_of_sunlight, kwh_price):

        '''
        average number of sunny days in alberta is here: https://www.currentresults.com/Weather/Canada/Alberta/sunshine-annual-average.php
        sunny days in alberta = 330ish and average sunny hours is 2400

        also need average price of a pannel in alberta 

        average size of solar pannel is 19.5 square feet: https://www.paradisesolarenergy.com/blog/how-many-solar-panels-do-i-need


        graph of solar capacity for price: https://kubyenergy.ca/blog/the-cost-of-solar-panels
        uing the economic of solar energy graph but treat it as a linear function we get 
        cost = 2000(solar capacity kW) + 1500
        '''

        if square_footage == None:
            return None
        
        # need to get solar capacity 

        number_of_pannels = square_footage // panel_sqft # sqrfootage of a solar pannel 

        # average solar pannel generates around 400W of power https://kubyenergy.ca/blog/the-complete-guide-to-installing-solar-panels-in-alberta#:~:text=The%20average%20home%20in%20Alberta,cover%20their%20annual%20energy%20needs.

        solar_capacity_kw = (number_of_pannels * solar_pannel_wattage)/ 1000

        price = 2000 * solar_capacity_kw + 1500 

        power_generated_year = solar_capacity_kw * hours_of_sunlight

        power_savings = power_generated_year * kwh_price

        roi = price / power_generated_year * kwh_price

        r = {}

        r['solar capacity'] = solar_capacity_kw
        r['power generated'] = power_generated_year
        r['savings'] = power_savings
        r['roi'] = roi
        
        return r


@commercial.route('/lighting/<building_id>', methods=['GET', 'POST'])
@login_required
def lighting(building_id):
    buildingid = 'ce736d20'
    numHighBays = 0
    num1x4 = 0
    num2x4 = 0
    numWallPack = 0
    numSpotLights = 0
    numLinears = 0
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        if 'High Bay' in result[1]:
            numHighBays += int(result[0])
        if '1x4' in result[1]:
            num1x4 += int(result[0])  
        if '2x4' in result[1]:
            num2x4 += int(result[0])  
        if 'Wall Pack' in result[1]:
            numWallPack += int(result[0])  
        if 'Spotlight' in result[1]:
            numSpotLights += int(result[0])  
        if 'Linear' in result[1]:
            numLinears += int(result[0])  
  

    return render_template('lighting.html' ,building_address = building_address, buidling_description = buidling_description,building_id=building_id, numHighBays = numHighBays, num1x4=num1x4,num2x4=num2x4,numWallPack=numWallPack,numSpotLights=numSpotLights,numLinears=numLinears)


@commercial.route('/troffer2x4/<building_id>', methods=['GET', 'POST'])
@login_required
def troffer2x4(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and '2x4' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    


    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('troffer2x4.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList,percentSum = percentSum, equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/troffer1x4/<building_id>', methods=['GET', 'POST'])
@login_required
def troffer1x4(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and '1x4' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    


    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('troffer1x4.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList,percentSum = percentSum, equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/highbay/<building_id>', methods=['GET', 'POST'])
@login_required
def highbay(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'High Bay' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    


    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('highbay.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList,percentSum = percentSum, equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/wallpack/<building_id>', methods=['GET', 'POST'])
@login_required
def wallpack(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Wall Pack' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    


    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('wallpack.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList,percentSum = percentSum, equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/linear/<building_id>', methods=['GET', 'POST'])
@login_required
def linear(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Linear' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    


    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('linear.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList,percentSum = percentSum, equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/spotlight/<building_id>', methods=['GET', 'POST'])
@login_required
def spotlight(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Spot Light' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('spotlight.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)





@commercial.route('/hvac/<building_id>', methods=['GET', 'POST'])
@login_required
def hvac(building_id):
    buildingid = 'ce736d20'
    numUnitHeaters = 0
    numInfraredHeaters = 0
    numRTUS = 0
    numFurnaces = 0
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type FROM Items WHERE items_building_id = %s AND items_subtype = 'Heathing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        if 'Unit' in result[1]:
            numUnitHeaters += int(result[0])
        if 'Infared' in result[1] or "Infrared" in result[1]:
            numInfraredHeaters += int(result[0])  
        if 'RTU' in result[1]:
            numRTUS += int(result[0])  
        if 'Furnace' in result[1]:
            numFurnaces += int(result[0])  
  

    return render_template('hvac.html' ,building_address = building_address, buidling_description = buidling_description, building_id=building_id,numFurnaces = numFurnaces, numRTUS = numRTUS, numUnitHeaters = numUnitHeaters, numInfraredHeaters = numInfraredHeaters)


@commercial.route('/furnace/<building_id>', methods=['GET', 'POST'])
@login_required
def furnace(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Spot Light' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('furnace.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/lennox69/<building_id>', methods=['GET', 'POST'])
@login_required
def lennox69(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Spot Light' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('lennox69.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/carrier/<building_id>', methods=['GET', 'POST'])
@login_required
def carrier(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Spot Light' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('carrier.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/lennox140/<building_id>', methods=['GET', 'POST'])
@login_required
def lennox140(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Spot Light' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('lennox140.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)


@commercial.route('/unitheater/<building_id>', methods=['GET', 'POST'])
@login_required
def unitheater(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND items_subtype = 'Heathing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and 'Unit' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('unitheater.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)

@commercial.route('/infrared/<building_id>', methods=['GET', 'POST'])
@login_required
def infrared(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND items_subtype = 'Heathing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and  'Infared' or 'Infrared' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('infrared.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)


@commercial.route('/rtu/<building_id>', methods=['GET', 'POST'])
@login_required
def rtu(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND items_subtype = 'Heathing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)
    for result in myresult:
        for i in range(0,len(areaIds)):
            if result[2] == equipmentDf.iloc[i][0] and  'RTU' in result[1]:
                equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('rtu.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)


@commercial.route('/pump/<building_id>', methods=['GET', 'POST'])
@login_required
def pump(building_id):
    buildingid = 'ce736d20'
    numPump = 0
    numMotor = 0
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type FROM Items WHERE items_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        if 'Pump' in result[1]:
            numPump += int(result[0])
        if 'Motor' in result[1]:
            numMotor += int(result[0])   
  

    return render_template('pump.html' ,building_address = building_address, buidling_description = buidling_description,building_id=building_id,numPump=numPump, numMotor=numMotor)

@commercial.route('/chiller/<building_id>', methods=['GET', 'POST'])
@login_required
def chiller(building_id):
    buildingid = 'ce736d20'
    numChiller = 0
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type FROM Items WHERE items_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        if 'Chiller' in result[1]:
            numChiller += int(result[0]) 
  

    return render_template('chiller.html' ,building_address = building_address, buidling_description = buidling_description,building_id=building_id,numChiller=numChiller)


@commercial.route('/dhw/<building_id>', methods=['GET', 'POST'])
@login_required
def dhw(building_id):
    buildingid = 'ce736d20'
    numChiller = 0
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type FROM Items WHERE items_building_id = %s AND items_subtype = 'DHW'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        if 'Chiller' in result[1]:
            numChiller += int(result[0]) 
  

    return render_template('dhw.html' ,building_address = building_address, buidling_description = buidling_description,building_id=building_id,numChiller=numChiller)


@commercial.route('/aosmith/<building_id>', methods=['GET', 'POST'])
@login_required
def aosmith(building_id):
    buildingid = 'ce736d20'
    areaIds = []
    areaNames = []
    areaCount = []
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT area_id, area_desctription FROM area WHERE area_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for result in myresult:
        areaIds.append(result[0])
        areaNames.append(result[1])
        areaCount.append(0)

    equipmentDf = pd.DataFrame({'Area Id': areaIds, 'Area Name': areaNames, 'Area Count': areaCount})
    sql = "SELECT items_st_quantity, items_st_consolidate_sub_type, items_area_id FROM Items WHERE items_building_id = %s AND items_subtype = 'DHW'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)
    for result in myresult:
        for i in range(0,len(areaIds)):
            equipmentDf.loc[i, 'Area Count'] += int(result[0])
    equipmentDf = equipmentDf.sort_values(by = ['Area Count'], ascending=False)
    areaCount = equipmentDf['Area Count'].tolist()
    areaList = equipmentDf['Area Name'].tolist()
    totalLights = sum(areaCount)
    percentSum = totalLights
    colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']

    for i in range(0,len(areaCount)):
        if len(colours) < len(areaCount):
            colours.append("#" + "%06x" % random.randint(0, 0xFFFFFF))
    
    if len(areaCount) == 0:
        areaCount.append(0)
    if percentSum == 0:
        percentSum = 1
    return render_template('aosmith.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,areaList=areaList, percentSum = percentSum,equipmentDf = equipmentDf, areaCount = areaCount, totalLights = totalLights, numAreas = len(areaCount), colours = colours)


@commercial.route('/inventory/<building_id>', methods=['GET', 'POST'])
@login_required
def inventory(building_id):
    buildingid = 'ce736d20'
    numLights = 0
    totalWatts = 0
    BTUTotal = 0
    ChillerTons = 0
    DHWTons = 0
    PlugTons = 0
    numHvac = 0
    numPlugs = 0
    numDHW = 0

    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]
    mycursor = mydb.cursor()
    sql = "SELECT items_st_quantity FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    lightlist = []
    for result in myresult:
        lightlist.append(result[0])
    for light in lightlist:
        numLights += int(light)  

    sql = "SELECT items_id FROM Items WHERE items_building_id = %s AND Items_type = 'Lighthing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    itemidlist = []
    for result in myresult:
        itemidlist.append(result[0])

    format_strings = ','.join(['%s'] * len(itemidlist))
    sql = "SELECT watts_per_lamp FROM lighting WHERE item_id IN (%s)" % format_strings, tuple(itemidlist)
    mycursor.execute("SELECT watts_per_lamp,item_id FROM lighting WHERE item_id IN (%s)" % format_strings, tuple(itemidlist))
    myresult = mycursor.fetchall()
    print(myresult)
    lightingwatts = []
    lightingid = []
    for result in myresult:
        lightingwatts.append(result[0])
        lightingid.append(result[1])
    for i in range(0,len(itemidlist)):
        lightingid.append(0)

    for i in range(0, len(lightlist)):
        if itemidlist[i] == lightingid[i]:
            totalWatts += float(lightlist[i]) * float(lightingwatts[i])
        else:
            totalWatts += float(lightlist[i]) * 57
    

    sql = "SELECT items_st_quantity FROM Items WHERE items_building_id = %s AND items_subtype = 'Heathing'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    hvacList = []
    for result in myresult:
        hvacList.append(result[0])
    for light in hvacList:
        if light == None:
            light = 0
        numHvac += int(light) 

    for hvac in hvacList:
        if hvac == None:
            hvac = 0
        BTUTotal += float(hvac) * 120000

    sql = "SELECT items_st_quantity FROM Items WHERE items_building_id = %s AND items_subtype = 'Plug Loads'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    plugList = []
    for result in myresult:
        plugList.append(result[0])
    for light in plugList:
        if light == None:
            light = 0
        numPlugs += int(light) 

    sql = "SELECT items_st_quantity FROM Items WHERE items_building_id = %s AND items_subtype = 'DHW'"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    DHWList = []
    for result in myresult:
        DHWList.append(result[0])
    for light in DHWList:
        if light == None:
            light = 0
        numDHW += int(light) 

    sql = "SELECT cooling_unit_output FROM cooling WHERE cooling_building_id = %s"
    val = (buildingid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    numChiller = len(myresult)

    return render_template('inventory.html',building_address = building_address, buidling_description = buidling_description,building_id=building_id,PlugTons = PlugTons,DHWTons=DHWTons,ChillerTons = ChillerTons,BTUTotal = BTUTotal, numLights = numLights, numHvac = numHvac , numPlugs = numPlugs, numDHW = numDHW, numChiller = numChiller, totalWatts = totalWatts)



@commercial.route('/datastream/<building_id>', methods=['GET', 'POST'])
@login_required
def datastream(building_id):

    building_id = building_id
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]


    return render_template('datastream.html',building_address = building_address, buidling_description = buidling_description,building_id = building_id)




@commercial.route('/utilities/<building_id>', methods=['GET', 'POST'])
@login_required
def utilities(building_id):
    form = UtilityForm()
    path = '/uploads/'
    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]

    mycursor = mydb.cursor()
    sql = "SELECT yearlyGas FROM utilities WHERE id = 1"
        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    gasdata = tempstring.split(',')

    mycursor = mydb.cursor()
    sql = "SELECT yearlyElectrical FROM utilities WHERE year = 2017"
        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    electricaldata = tempstring.split(',')


    if request.method == "POST":
        electricaldata = []
        gasdata = []
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(filename)
        xl_file = pd.ExcelFile(filename)

        dfs = {sheet_name: xl_file.parse(sheet_name) 
                  for sheet_name in xl_file.sheet_names}
        electricdf = dfs['Electricity']
        electricdf = electricdf.fillna('nan')
        electricaldata2 = electricdf.iloc[:, 8].to_list()
        print(electricdf)
        for i in range(len(electricaldata2)):
            if electricaldata2[i] != 'nan' and electricaldata2[i] != 'Total':
                electricaldata.append(electricaldata2[i])
        
        naturalgasdf = dfs['Natural Gas']
        naturalgasdf = naturalgasdf.fillna('nan')
        gasdata2 = naturalgasdf.iloc[:, -1].to_list()
        for i in range(len(gasdata2)):
            if gasdata2[i] != 'nan' and gasdata2[i] != 'Total':
                gasdata.append(gasdata2[i])

        for i in range(len(electricaldata) - 12):
            electricaldata.pop()
        for i in range(len(gasdata) - 12):
            gasdata.pop()


        for i in range(len(gasdata)):
            electricaldata[i] = str(electricaldata[i])
            gasdata[i] = str(gasdata[i])

        gasstring = ','.join(gasdata)
        electricalstring = ','.join(electricaldata)
        year  = (electricdf.columns.to_list())[0]
        sql = "UPDATE utilities SET yearlyElectrical = %s, yearlyGas = %s WHERE id = 1"
        val = (electricalstring, gasstring)
        mycursor.execute(sql, val)

        mydb.commit()

    return render_template('utilities.html',building_address = building_address, buidling_description = buidling_description, building_id = building_id,form = form, electricaldata = electricaldata, gasdata= gasdata)


@commercial.route('/generatereport/<building_id>', methods=['GET', 'POST'])
def generatereport(building_id):
    form = OperatingHoursForm()
    building_id = building_id
    building_ids = 12
    year = 2021
    days_per_week = 5
    start_hour = 8
    end_hour = 17
    starthours = []
    endhours = []
    startam = []
    endam = []
    startminutes = []
    endminutes = []
    month = 10
    changed = ''
    mydb = mysql.connector.connect(
      host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
      user="readOnly",
      password="JSfB55vpSL",
      database="db_mysql_sustainergy_alldata"
    )
    mycursor = mydb.cursor()
    sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()
    for result in myresult:
        building_address = result[0]
        buidling_description = result[1]

    # calendar_init(building_id, year, days_per_week, start_hour, end_hour)
    if request.method == "POST":
        month = request.form['month']
        starthours = []
        endhours = []
        startam = []
        endam = []
        changed = request.form.get('changed')
        datenumber = request.form.get('datenumber')
        bulk = request.form.get('bulk')


    month = int(month)
    cal_month = month + 1
    cal_db = calendar_pull(building_ids,year, cal_month)
    if changed == "true":
        if bulk == "single":
            newstart = request.form.get('newstart')
            newend = request.form.get('newend')
            datenumber = int(datenumber)
            startmins = request.form.get('startmins')
            endmins = request.form.get('endmins')
            starttime = newstart + ':' + startmins
            endtime = newend + ':' + endmins
            datechange = datetime.date(year,cal_month,datenumber)
            cal_db = calendar_edit(cal_db,datechange,starttime,endtime)
            calendar_update(building_ids, year,cal_db)
        if bulk == "weekday":
            newstart = request.form.get('newstart')
            newend = request.form.get('newend')
            datenumber = int(datenumber)
            startmins = request.form.get('startmins')
            endmins = request.form.get('endmins')
            starttime = newstart + ':' + startmins
            endtime = newend + ':' + endmins
            datechange = datetime.datetime(year,cal_month,datenumber)
            datechange = datechange.weekday()
            cal_db = edit_weekday_calendar(cal_db,datechange,starttime,endtime)
            calendar_update(building_ids, year,cal_db)

        if bulk == "everyday":
            newstart = request.form.get('newstart')
            newend = request.form.get('newend')
            datenumber = int(datenumber)
            startmins = request.form.get('startmins')
            endmins = request.form.get('endmins')
            starttime = newstart + ':' + startmins
            endtime = newend + ':' + endmins
            for i in range(0,6):
                cal_db = edit_weekday_calendar(cal_db,i,starttime,endtime)
                calendar_update(building_ids, year,cal_db)

        if bulk == "everyweekday":
            newstart = request.form.get('newstart')
            newend = request.form.get('newend')
            datenumber = int(datenumber)
            startmins = request.form.get('startmins')
            endmins = request.form.get('endmins')
            starttime = newstart + ':' + startmins
            endtime = newend + ':' + endmins
            for i in range(0,5):
                cal_db = edit_weekday_calendar(cal_db,i,starttime,endtime)
                calendar_update(building_ids, year,cal_db)
    for date in cal_db:
        string = date
        starthours.append(string['start_hours'])
        endhours.append(string['end_hours'])
    d = datetime.datetime(2021, cal_month, 1)
    offset = d.weekday()
    offset += 1
    starthours = rotate(starthours,offset)
    endhours = rotate(endhours,offset)

    i = 0
    for hour in starthours:
        if type(hour) == str and hour[1] == ':':
            starthours[i] = hour[0]
            starthours[i] = int(starthours[i])
            startminutes.append(hour[2] + hour[3])
        elif type(hour) == str and hour[1] != ':':
            starthours[i] = hour[0] + hour[1]
            starthours[i] = int(starthours[i])
            startminutes.append(hour[3] + hour[4])
        else:
            startminutes.append('00')
        i += 1

    i = 0
    for hour in endhours:
        if type(hour) == str and hour[1] == ':':
            endhours[i] = hour[0]
            endhours[i] = int(endhours[i])
            endminutes.append(hour[2] + hour[3])
        elif type(hour) == str and hour[1] != ':':
            endhours[i] = hour[0] + hour[1]
            endhours[i] = int(endhours[i])
            endminutes.append(hour[3] + hour[4])
        else:
            endminutes.append('00')
        i += 1 

    for i in range(len(starthours)):
        if starthours[i] is not None and starthours[i] < 13:
            startam.append("am")
        if starthours[i] is not None and starthours[i] >= 13:
            startam.append("pm")
            starthours[i] = starthours[i] - 12
        if starthours[i] is None:
            startam.append(endhours[i])

        if endhours[i] is not None and endhours[i] < 13:
            endam.append("am")
        if endhours[i] is not None and endhours[i] >= 13:
            endam.append("pm")
            endhours[i] = endhours[i] - 12
        if endhours[i] is None:
            endam.append(endhours[i])

    sql = "SELECT yearlyGas FROM utilities WHERE year = 2017"
    
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    gasdata = tempstring.split(',')

    mycursor = mydb.cursor()
    sql = "SELECT yearlyElectrical FROM utilities WHERE year = 2017"
        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        tempstring = ','.join(x)
    electricaldata = tempstring.split(',')

    electrialusage = float(electricaldata[month])
    electricalrate = 0.071
    electricalcost = "{:.2f}".format(electrialusage * electricalrate)
    electrialusage = "{:.2f}".format(electrialusage)

    gasuage = float(gasdata[month])
    gasrate = 4.35
    gascost = "{:.2f}".format(gasuage * gasrate)
    gasuage = "{:.2f}".format(gasuage)
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    monthname = months[month]

    sql = "SELECT panel_id, panel_name, panel_voltage,panel_type FROM panel_data WHERE building_id = %s"
            
    mycursor.execute(sql,(building_id,))
    myresult = mycursor.fetchall()

    panel_name_list = []
    voltage_list = []
    type_list = []
    circuit_name_list = []
    panel_name_ids = []
    category_list = []
    lighting_count = []
    hvac_count = []
    dhw_count = []
    plug_count = []
    other_count = []
    boiler_count = []
    spare_count = []
    energy_meter_cost = '449.50'
    misc_cost = '94.55'
    lead_cost = '45.66'
    circuit_cost = '15.78'
    electrical_cost = '94.55'
    comissioning_cost = '94.55'

    mcc_meter_price = '1600'
    mcc_clamp_price = '748.56'
    mcc_misc_price = '94.55'
    mccc_electrical_price = '294.55'
    mcc_commissioning_price = '94.55'

    cost_list = []
    panel_cost_list = []
    panel_mains_cost_list = []


    sql = "SELECT meter_price, misc_price, lead_price, circuit_price, electrical_price, commission_price FROM panel_price WHERE building_id = %s"            
    mycursor.execute(sql,(building_id,))
    prices = mycursor.fetchall()

    for price in prices:
        if price[0] == '':
            nochange = True
        else:
            energy_meter_cost = price[0]
            misc_cost = price[1]
            lead_cost = price[2]
            circuit_cost = price[3]
            electrical_cost = price[4]
            comissioning_cost = price[5]



    for result in myresult:
        panel_id = result[0]
        panel_name = result[1]
        panel_voltage = result[2]
        panel_type = result[3]

        sql = "SELECT circuit_name, circuit_category FROM circuit_data WHERE panel_id = %s ORDER BY CAST(row_numbers AS UNSIGNED) asc"
                
        mycursor.execute(sql,(panel_id,))
        circuitresult = mycursor.fetchall()
        circuitlist = []
        circuit_category = []
        for circuit in circuitresult:
            circuitlist.append(circuit[0])
            circuit_category.append(circuit[1])

        category_list.append(circuit_category)
        
        lighting = 0
        hvac = 0
        dhw = 0
        plugload = 0
        other = 0
        spare = 0
        boiler = 0
        for category in circuit_category:
            if category == 'Lighting' or category == 'Lighting ':
                lighting += 1
            elif category == 'HVAC' or category == 'HVAC ':
                hvac += 1
            elif category == 'DHW':
                dhw += 1
            elif category == 'Plug-Load' or category == 'Plug-Load ':
                plugload += 1
            elif category == 'Spare/Inactive' or category == 'Space' or category == 'Spare/ In-active' or category == 'nan'  or category == 'Spare/in-active '  or category == 'Spare/in-active':
                spare += 1
            elif category == 'Boiler / DHW' or category == 'Boiler/DHW':
                boiler += 1
            else:
                other += 1

        num_circuits = len(circuit_category) - spare

        

        if num_circuits == 0:
            current_panel_cost = 0
            current_mains_cost = 0

        else:
            if panel_type != 'MCC Unit':
                num_energy_meters = (((num_circuits + 3)) / 14)
                num_energy_meters = math.ceil(num_energy_meters)
                current_panel_cost = (float(num_energy_meters) * float(energy_meter_cost)) + float(misc_cost) + (float(lead_cost) * 3) + (float(circuit_cost) * float(num_circuits)) + (float(electrical_cost)) + float(comissioning_cost)
                current_mains_cost = (float(1) * float(energy_meter_cost)) + float(misc_cost) + (float(lead_cost) * 3) + float(electrical_cost) + float(comissioning_cost)
            else:
                num_energy_meters = int(math.ceil((num_circuits + 3)) / 14)
                print(num_energy_meters)  
                current_panel_cost = (float(num_energy_meters) * float(mcc_meter_price)) + float(mcc_misc_price) + (float(mcc_clamp_price) * float(num_circuits)) + (float(mccc_electrical_price)) + float(mcc_commissioning_price)
                current_mains_cost = 0

        panel_cost_list.append("{:.2f}".format(current_panel_cost))
        panel_mains_cost_list.append("{:.2f}".format(current_mains_cost))


        lighting_count.append(lighting)
        hvac_count.append(hvac)
        dhw_count.append(dhw)
        plug_count.append(plugload)
        other_count.append(other)
        spare_count.append(spare)
        boiler_count.append(boiler)
        panel_name_list.append(panel_name)
        voltage_list.append(panel_voltage)
        type_list.append(panel_type)
        circuit_name_list.append(circuitlist)

    for panelname in panel_name_list:
        panelname = panelname.replace(' ','_')
        panel_name_ids.append(panelname)

    mains_total = 0
    mcc_mains_total = 0
    i = 0
    for panel in panel_mains_cost_list:
        if type_list[i] != 'MCC Unit':
            mains_total += float(panel)
        elif type_list[i] == 'MCC Unit':
            mcc_mains_total += float(panel)
        i += 1

    circuits_total = 0
    mcc_circuits_total = 0
    i = 0
    for panel in panel_cost_list:
        if type_list[i] != 'MCC Unit':
            circuits_total += float(panel)
        elif type_list[i] == 'MCC Unit':
            mcc_circuits_total += float(panel)
        i += 1


    num_panels = len(panel_name_list)
    total_num_circuits_panels = 0
    total_num_circuits_mcc = 0
    for i in range(0,len(circuit_name_list)):
        if type_list[i] != 'MCC Unit':
            total_num_circuits_panels += len(circuit_name_list[i])
        elif type_list[i] == 'MCC Unit':
            total_num_circuits_mcc += len(circuit_name_list[i])

    mains_total = "{:.2f}".format(mains_total)
    circuits_total = "{:.2f}".format(circuits_total)
    mcc_circuits_total = "{:.2f}".format(mcc_circuits_total)
    mcc_mains_total = "{:.2f}".format(mcc_mains_total)


    num_standard_panels = 0
    num_mcc_panels = 0
    for i in range(0,len(panel_name_list)):
        if type_list[i] != 'MCC Unit':
            num_standard_panels += 1
        elif type_list[i] == 'MCC Unit':
            num_mcc_panels += 1
    print(type_list)
    return render_template('generatereport.html',pageNumber = 7, num_mcc_panels=num_mcc_panels,num_standard_panels=num_standard_panels,mcc_mains_total=mcc_mains_total,mcc_circuits_total=mcc_circuits_total,type_list=type_list,energy_meter_cost=energy_meter_cost,misc_cost=misc_cost,lead_cost=lead_cost,circuit_cost=circuit_cost,electrical_cost=electrical_cost,comissioning_cost=comissioning_cost,num_panels=num_panels,total_num_circuits_mcc = total_num_circuits_mcc, total_num_circuits_panels=total_num_circuits_panels,circuits_total=circuits_total,mains_total=mains_total,panel_mains_cost_list=panel_mains_cost_list,panel_cost_list = panel_cost_list, boiler_count=boiler_count,spare_count=spare_count,sorted_categories = [],category_list=category_list,other_count=other_count,plug_count=plug_count,dhw_count=dhw_count,hvac_count=hvac_count,lighting_count=lighting_count,panel_name_ids=panel_name_ids,circuit_name_list = circuit_name_list, voltage_list = voltage_list, panel_name_list = panel_name_list,panel_voltage = panel_voltage, len = len(panel_name_list), panel_name = panel_name, circuitlist = circuitlist,monthname=monthname,gascost = gascost, gasrate = gasrate, gasuage = gasuage, electricalcost = electricalcost, electricalrate = electricalrate, electrialusage = electrialusage, building_address = building_address, buidling_description = buidling_description,building_id = building_id,startminutes = startminutes, endminutes = endminutes, form = form,month = month,starthours = starthours, endhours = endhours, startam = startam, endam = endam)

@commercial.route('/clientlist', methods=['GET', 'POST'])
@login_required
def clientlist():
    form = OperatingHoursForm()
    if(current_user.is_authenticated and current_user.is_admin()):

        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT name, clientID FROM client"
                
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        clients = []
        clientids = []
        for result in myresult:
            clients.append(result[0])
            clientids.append(result[1])

        return render_template('clientlist.html',clients=clients,clientids=clientids, len = len(clients))
    else:
        abort(403)


@commercial.route('/building_list/<client_id>', methods=['GET', 'POST'])
def building_list(client_id):
    client_id = client_id

    mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
    mycursor = mydb.cursor()
    sql = "SELECT description, idbuildings FROM buildings WHERE client_id = %s"
    mycursor.execute(sql,(client_id,))
    myresult = mycursor.fetchall()
    building_ids = []
    descriptions = []
    for result in myresult:
        descriptions.append(result[0])
        building_ids.append(result[1])

    return render_template('building_list.html',building_ids=building_ids,descriptions=descriptions, len = len(descriptions))


@commercial.route('/historicalusage/<building_id>', methods=['GET', 'POST'])
@login_required
def historicalusage(building_id):
        building_id = building_id
        usage = []
        price = []
        percent = []
        channel_names = []
        panels = []
        categories = []
        strippedPanels = []
        strippedNames = []
        scheduledata = []
        day = datetime.datetime.now().day
        cal_month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        totalUsage = 0
        totalPrice = 0
        error = None
        building_ids = 12
        lighttotal = 0
        equipmenttotal = 0
        hvactotal = 0
        plugtotal = 0
        watertotal = 0
        othertotal =0
        daysDifference = 1
        form = HistoricalUsageForm()

        if(current_user.is_authenticated and current_user.is_admin()):
            mydb = mysql.connector.connect(
              host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
              user="readOnly",
              password="JSfB55vpSL",
              database="db_mysql_sustainergy_alldata"
            )
            mycursor = mydb.cursor()

            sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
                    
            mycursor.execute(sql,(building_id,))
            myresult = mycursor.fetchall()

            for result in myresult:
                building_address = result[0]
                buidling_description = result[1]

            today = date.today()
            userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
            correctdate = 'Mon, 21 Mar 2022'
            client_id = current_user.phone_number
            panel_building_id = building_id

            sql = "SELECT emporia_meter_sn_1 FROM electrical_panel WHERE building_id = %s"
            mycursor.execute(sql,(panel_building_id,))
            myresult = mycursor.fetchall()
            for x in myresult:
                serial_numbers = ','.join(x)
            serial_list = serial_numbers.split()

            if request.method == "POST":
                correctdate = request.form['datepicker']
                userdate = request.form['datepicker']
                n = 5
                userdate = userdate[n:]
                userdate = userdate.split(' ')
                months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                for i in range(0,len(months)):
                    if userdate[1] == months[i]:
                        if i < 10:
                            userdate[1] = '0' + str(i + 1)
                        else:
                            userdate[1] = str(i + 1)
                if int(userdate[0]) < 10:
                    userdate[0] = '0' + userdate[0]
                userdate = userdate[2] + '-' + userdate[1] + '-' + userdate[0]

                cal_month = str(userdate)[5] + str(userdate)[6]
                day = str(userdate)[8] + str(userdate)[9]
                daysDifference = (datetime.datetime.today() - datetime.datetime.strptime(userdate, '%Y-%m-%d')).days

                if datetime.datetime.strptime(userdate, '%Y-%m-%d') >= datetime.datetime.today():
                    userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
                    cal_month = str(userdate)[5] + str(userdate)[6]
                    day = str(userdate)[8] + str(userdate)[9]
                    year = datetime.datetime.now().year
                    error = 'Cannot select future dates'
                    daysDifference = 1
                userdate = userdate + '%'

            i = 1
            for number in serial_list:
                sql = "SELECT channel4_name, channel4_usage,channel5_name, channel5_usage,channel6_name, channel6_usage,channel7_name, channel7_usage,channel8_name, channel8_usage,channel9_name, channel9_usage,channel10_name, channel10_usage,channel11_name, channel11_usage,channel12_name, channel12_usage,channel13_name, channel13_usage,channel14_name, channel14_usage,channel15_name, channel15_usage,channel16_name, channel16_usage,channel17_name, channel17_usage,channel18_name, channel18_usage,channel19_name, channel19_usage FROM emporia_data WHERE date LIKE %s AND serial_number = %s"    
                mycursor.execute(sql, (userdate, number))
                myresult = mycursor.fetchall()
                if myresult == []:
                    userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
                    cal_month = str(userdate)[5] + str(userdate)[6]
                    day = str(userdate)[8] + str(userdate)[9]
                    year = datetime.datetime.now().year
                    error = 'No data for selected date'
                    daysDifference = 1
                    number = serial_list[0]
                    sql = "SELECT channel4_name, channel4_usage,channel5_name, channel5_usage,channel6_name, channel6_usage,channel7_name, channel7_usage,channel8_name, channel8_usage,channel9_name, channel9_usage,channel10_name, channel10_usage,channel11_name, channel11_usage,channel12_name, channel12_usage,channel13_name, channel13_usage,channel14_name, channel14_usage,channel15_name, channel15_usage,channel16_name, channel16_usage,channel17_name, channel17_usage,channel18_name, channel18_usage,channel19_name, channel19_usage FROM emporia_data WHERE date LIKE %s AND serial_number = %s"    
                    mycursor.execute(sql, (userdate, number))
                    myresult = mycursor.fetchall()
                for x in myresult:
                    tempstring = ','.join(x)

                stringlist = tempstring.split(',')
                for k in range(0,int(len(stringlist)/2)):
                    channel_names.append(stringlist[::2][k])
                    usage.append(float(stringlist[1::2][k]))
                for k in range(0, int(len(stringlist)/2)):
                    panels.append('Panel ' + str(i))
                i += 1

            for name in channel_names:
                name_l = name.lower()
                if 'light' in name_l or 'lights' in name_l or 'lighting' in name_l:
                    categories.append('lighting')

                elif 'hot water' in name_l or 'dhw' in name_l or 'water' in name_l or 'water heater' in name_l:
                    categories.append('dhw')

                elif 'fan' in name_l or 'heat' in name_l or 'hvac' in name_l or 'cooling' in name_l:
                    categories.append('hvac')

                elif 'motor' in name_l or 'pump' in name_l or 'compressor' in name_l or 'vacuum' in name_l or 'dryer' in name_l:
                    categories.append('equipment')
                
                elif 'plug' in name_l or 'plugs' in name_l or 'receptacle' in name_l or 'receptacle' in name_l:
                    categories.append('plugload')
                
                else:
                    categories.append('other')

            for energy in usage:
                price.append(energy * 0.09)
                percent.append((energy / sum(usage)) * 100)

            for serialNumber in serial_list:
                string = ''
                sql = "SELECT channel4_schedule, channel5_schedule, channel6_schedule, channel7_schedule, channel8_schedule, channel9_schedule, channel10_schedule, channel11_schedule, channel12_schedule, channel13_schedule, channel14_schedule, channel15_schedule, channel16_schedule, channel17_schedule, channel18_schedule, channel19_schedule FROM emporia_data WHERE date LIKE %s AND serial_number = %s"   
                mycursor.execute(sql, (userdate, serialNumber))
                myresult = mycursor.fetchall()
                for x in myresult:
                    string = "'".join(x)
                scheduledata.extend(string.split("'"))

            historicalusage = pd.DataFrame({'Channel Names': channel_names, "Usage": usage, "Price":price, "Percent":percent, "Panel Names": panels, "Category": categories,"Schedule": scheduledata})
            historicalusage = historicalusage.sort_values(by=['Usage'], ascending=False)
            channel_names = historicalusage['Channel Names'].tolist()
            usage = historicalusage['Usage'].tolist()
            price = historicalusage['Price'].tolist()
            panels = historicalusage['Panel Names'].tolist()
            percent = historicalusage['Percent'].tolist()
            categories = historicalusage['Category'].tolist()
            scheduledata = historicalusage['Schedule'].tolist()

            for i in range(0, len(usage)):
                usage[i] = float("{:.2f}".format(usage[i]/1000))
                price[i] = float("{:.2f}".format(price[i]/1000))
                percent[i] = float("{:.2f}".format(percent[i]))
                strippedPanels.append(panels[i].replace(" ",""))
                totalUsage += usage[i]
                totalPrice += price[i]

                if(categories[i] == "lighting"):
                    lighttotal += usage[i]
                if(categories[i] == "equipment"):
                    equipmenttotal += usage[i]
                if(categories[i] == "hvac"):
                    hvactotal += usage[i]
                if(categories[i] == "plugload"):
                    plugtotal += usage[i]
                if(categories[i] == "dhw"):
                    watertotal += usage[i]
                if(categories[i] == "other"):
                    othertotal += usage[i]
            
            colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']
            panelchart = historicalusage.groupby(["Panel Names"]).sum()['Usage'].tolist()

            numpanels = len(np.unique(panels))
            panelnames = np.unique(panels).tolist()
            categorynames = ['Lighting', 'Equipment', 'HVAC','Plug Load','DHW','Other']
            backendnames = ['lighting', 'equipment', 'hvac','plugload','dhw','other']
            for panel in panelnames:
                strippedNames.append(panel.replace(" ",""))

            totalUsage = float("{:.2f}".format(totalUsage))
            totalPrice = float("{:.2f}".format(totalPrice))
            totalEmmissions = float("{:.2f}".format(totalUsage * 0.82))

            lighttotal = float("{:.2f}".format(((lighttotal) / (totalUsage)) * 100))
            equipmenttotal = float("{:.2f}".format(((equipmenttotal) / (totalUsage)) * 100))
            hvactotal = float("{:.2f}".format(((hvactotal) / (totalUsage)) * 100))
            plugtotal = float("{:.2f}".format(((plugtotal) / (totalUsage)) * 100))
            watertotal = float("{:.2f}".format(((watertotal) / (totalUsage)) * 100))
            othertotal = float("{:.2f}".format(((othertotal) / (totalUsage)) * 100))

            categorytotals =[lighttotal, equipmenttotal,hvactotal,plugtotal,watertotal,othertotal]
            for i in range(0,len(panelchart)):
                panelchart[i] = float("{:.2f}".format(((panelchart[i]/1000) / totalUsage) * 100))
            categoriesdf = pd.DataFrame({'Category Names': categorynames, "Total": categorytotals, "Colors": colours, "Back End": backendnames})
            categoriesdf = categoriesdf.sort_values(by=['Total'], ascending=False)
            panelcolours = []
            for i in range(0,numpanels):
                panelcolours.append(colours[i])

            panelsdf = pd.DataFrame({'Panel Names': panelnames, "Total": panelchart, "Colors": panelcolours})

            cal_db = calendar_pull(building_ids,2021, int(cal_month))
            hours = cal_db[int(day) - 1]
            starthours = hours['start_hours']
            endhours = hours['end_hours']
            starthours = str(starthours).split(':')
            starthours = starthours[0]
            endhours = str(endhours).split(':')
            endhours = endhours[0]

            if starthours == 'None':
                starthours = 24
                endhours = 0

            data = scheduledata
            totalset = []
            string = data[0]
            string = string.replace('[', '')
            string = string.replace(']', '')
            datalist = string.split(",")
            totalset = [0] * len(datalist);
            offhours = [0] * len(datalist)
            for i in range(0, len(datalist)):
                string = data[i]
                string = string.replace('[', '')
                string = string.replace(']', '')
                datalist = string.split(",")
                floatlist = []
                try:
                    for item in datalist:
                        floatlist.append(float(item))
                except:
                    whoops = 0
                for k in range(int(starthours) - 1, int(endhours) + 1):
                    totalset[k] += float(datalist[k])
                for k in range(0, len(datalist)):
                    if ((k >= int(starthours) and k <= int(endhours)) == False):
                        offhours[k] += float(datalist[k])
            for i in range(0,len(offhours)):
                if(str(offhours[i]) == 'nan'):
                    offhours[i] = 0
            for i in range(0,len(totalset)):
                if(str(totalset[i]) == 'nan'):
                    totalset[i] = 0
            onHours = float("{:.2f}".format(((sum(totalset)) / (totalUsage * 1000) * 100)))
            offHours = float("{:.2f}".format(((sum(offhours)) / (totalUsage * 1000) * 100)))
            alwaysOn = "{:.2f}".format(100 - (onHours + offHours))
            if float(alwaysOn) < 0:
                alwaysOn = 0

            timeloads = {'Name':['On-Hours','Off-Hours','Always-On'], 'Percents':[onHours,offHours,alwaysOn],'Colors':['#22B14C','#7F7F7F','#EE8F37']}
            timeloads = pd.DataFrame(data = timeloads)
            timeloadscolours = ['#22B14C','#7F7F7F','#EE8F37']

            predicted_line = {}
            last_week_full = {}
            for i in range(0,len(serial_list)):
                data = get_weekly_data(serial_list[i],30)
                channel_dict, dates = weekday_organization(data)
                last_week_cd, last_week_dp = last_week_usage(data)
                try:
                    predicted_line.update(weekly_predicted_line(channel_dict, last_week_cd))
                except:
                    whoops = 0
                last_week_full.update(last_week_cd)
            weeklabels = ['M']
            weeklabels += ([''] * 23)
            weeklabels.append('T')
            weeklabels += ([''] * 23)
            weeklabels.append('W')
            weeklabels += ([''] * 23)
            weeklabels.append('T')
            weeklabels += ([''] * 23)
            weeklabels.append('F')
            weeklabels += ([''] * 23)
            weeklabels.append('S')
            weeklabels += ([''] * 23)
            weeklabels.append('S')
            weeklabels += ([''] * 23)
            kwhgraph = []
            data = scheduledata
            string = data[0]
            string = string.replace('[', '')
            string = string.replace(']', '')
            kwhgraphlist = string.split(",")
            kwhgraph = [0] * len(kwhgraphlist)
            for i in range(0,len(kwhgraphlist)):
                string = data[i];
                string = string.replace('[', '')
                string = string.replace(']', '')
                kwhgraphlist = string.split(",")
                for k in range(0,len(kwhgraphlist)):
                    kwhgraph[k] += float(kwhgraphlist[k])

            pricegraph = []
            for i in range(0,len(kwhgraph)):
                pricegraph.append(round((kwhgraph[i]/1000) * 0.09,2))
                kwhgraph[i] = round((kwhgraph[i] / 1000),2)
            hourslist = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
            
            period = []
            typegraph = []
            jsondictionary = {}

            for i in range(0,24):
                if i < int(starthours):
                    typegraph.append('off-hrs')
                    period.append('morning')
                elif i > int(endhours):
                    typegraph.append('off-hrs')
                    period.append('night')
                else:
                    typegraph.append('on-hrs')
                    period.append('afternoon')
            jsondictionarylist = []

            for i in range(0,24):
                if str(kwhgraph[i]) == 'nan':
                    kwhgraph[i] = 0
                if str(pricegraph[i]) == 'nan':
                    pricegraph[i] = 0
                jsondictionary = {
                    "value": kwhgraph[i],
                    "hours": hourslist[i],
                    "price": pricegraph[i],
                    "type": typegraph[i],
                    "period": period[i]
                }
                jsondictionarylist.append(jsondictionary)
            with open('benchmarking_tool/static/scripts/data.json', 'w') as f:
                json.dump(jsondictionarylist, f)
            chart_colours = ['#E6E9EF'] * 24

            cal_db = calendar_pull(building_ids,2021, int(cal_month))
            hours = cal_db[int(day) - 1]
            starthours = hours['start_hours']
            endhours = hours['end_hours']
            starthours = str(starthours).split(':')
            starthours = starthours[0]
            endhours = str(endhours).split(':')
            endhours = endhours[0]

            if starthours == 'None':
                starthours = 24
                endhours = 0

            for i in range(int(starthours), int(endhours)):
                chart_colours[i] = '#FFFFFF'


            panel_ids = []
            panel_names = []
            circuit_names = []
            circuit_categories = []
            circuit_name_groups = []
            circuit_category_groups =[]
            panel_name_ids =[]

            sql = "SELECT panel_id, panel_name FROM panel_data WHERE building_id = %s"
            mycursor.execute(sql,(building_id,))
            myresult = mycursor.fetchall()
            for result in myresult:
                panel_ids.append(result[0])
                panel_names.append(result[1])

            for panel in panel_ids:
                sql = "SELECT circuit_name, circuit_category FROM circuit_data WHERE panel_id = %s"
                mycursor.execute(sql,(panel,))
                myresult = mycursor.fetchall()
                current_panel = []
                current_category = []
                for result in myresult:
                    circuit_names.append(result[0])
                    current_panel.append(result[0])
                    circuit_categories.append(result[1])
                    current_category.append(result[1])

                circuit_name_groups.append(current_panel)
                circuit_category_groups.append(current_category)


            bucket = "trialset"
            org = "33fb425a6047cad9"
            token = "UUH6z-JPugsamGgl6DvZm4W-7Gr3GGABGFulHKdPI-AbObSQVNta_FRlqFswKP7zPkWB5xboRznsaSJqGf5C0A=="
            # Store the URL of your InfluxDB instance
            url="https://us-east-1-1.aws.cloud2.influxdata.com"
            client = influxdb_client.InfluxDBClient(
               url=url,
               token=token,
               org=org
            )
            query_api = client.query_api()
            query = ' from(bucket:"trialset")\
                |> range(start: -7d)\
                |> sort(columns: ["_time"])\
                |> top(n:1)\
                |> filter(fn:(r) => r._measurement == "power")\
                |> filter(fn: (r) => r._field == "value")'
            result = query_api.query(org=org, query=query)
            results = []
            for table in result:
              for record in table.records:
                results.append(record.get_value())

            query_api = client.query_api()
            query = ' from(bucket:"trialset")\
                |> range(start: -7d)\
                |> sort(columns: ["_time"])\
                |> top(n:1)\
                |> filter(fn:(r) => r._measurement == "power1")\
                |> filter(fn: (r) => r._field == "value")'
            result = query_api.query(org=org, query=query)
            for table in result:
              for record in table.records:
                results.append(record.get_value())

            query_api = client.query_api()
            query = ' from(bucket:"trialset")\
                |> range(start: -7d)\
                |> sort(columns: ["_time"])\
                |> top(n:1)\
                |> filter(fn:(r) => r._measurement == "power2")\
                |> filter(fn: (r) => r._field == "value")'
            result = query_api.query(org=org, query=query)
            for table in result:
              for record in table.records:
                results.append(record.get_value())

            names = ['power', 'power1', 'power2']
            total = sum(results)

            for panel in panel_names:
                newpanel = panel
                newpanel = newpanel.replace(' ', '')
                newpanel = newpanel.replace('"', '')
                newpanel = newpanel.replace("'", '')
                newpanel = newpanel.replace("(", '')
                newpanel = newpanel.replace(")", '')
                panel_name_ids.append(newpanel)
                user_agent = request.headers.get('User-Agent')
                user_agent = user_agent.lower()

            if "iphone" in user_agent or "android" in user_agent:
                return render_template('mobilehistorical.html',panel_name_ids=panel_name_ids,circuit_name_groups=circuit_name_groups,circuit_category_groups=circuit_category_groups,circuit_categories=circuit_categories,circuit_names=circuit_names,panel_names=panel_names,total = total,results=results,names=names,error = error,daysDifference = daysDifference,  chart_colours = chart_colours,endhours = endhours,last_week_cd=last_week_full,predicted_line=predicted_line,schedule = scheduledata,timeloads = timeloads,panelsdf = panelsdf,categoriesdf = categoriesdf, onHours = onHours,offHours = offHours,alwaysOn = alwaysOn,weeklabels = weeklabels, panelchart = panelchart,lighttotal = lighttotal, equipmenttotal=  equipmenttotal, hvactotal = hvactotal, plugtotal = plugtotal, watertotal= watertotal, othertotal = othertotal, correctdate=correctdate,totalEmmissions = totalEmmissions, totalPrice =  totalPrice, totalUsage = totalUsage,categorynames = categorynames,strippedNames=strippedNames,strippedPanels=strippedPanels,panelnames=panelnames ,colours = colours, numpanels = numpanels, numcircuits = len(channel_names), categories = categories, panels = panels, percent = percent, price = price, usage = usage, channel_names = channel_names, building_id = building_id, buidling_description = buidling_description, building_address = building_address, form = form)
            else:
                return render_template('historicalusage.html',error = error,daysDifference = daysDifference,  chart_colours = chart_colours,endhours = endhours,last_week_cd=last_week_full,predicted_line=predicted_line,schedule = scheduledata,timeloads = timeloads,panelsdf = panelsdf,categoriesdf = categoriesdf, onHours = onHours,offHours = offHours,alwaysOn = alwaysOn,weeklabels = weeklabels, panelchart = panelchart,lighttotal = lighttotal, equipmenttotal=  equipmenttotal, hvactotal = hvactotal, plugtotal = plugtotal, watertotal= watertotal, othertotal = othertotal, correctdate=correctdate,totalEmmissions = totalEmmissions, totalPrice =  totalPrice, totalUsage = totalUsage,categorynames = categorynames,strippedNames=strippedNames,strippedPanels=strippedPanels,panelnames=panelnames ,colours = colours, numpanels = numpanels, numcircuits = len(channel_names), categories = categories, panels = panels, percent = percent, price = price, usage = usage, channel_names = channel_names, building_id = building_id, buidling_description = buidling_description, building_address = building_address, form = form)
        else:
            abort(403)



@commercial.route('/mobilehistorical/<building_id>', methods=['GET', 'POST'])
@login_required
def mobilehistorical(building_id):
        building_id = building_id
        usage = []
        price = []
        percent = []
        channel_names = []
        panels = []
        categories = []
        strippedPanels = []
        strippedNames = []
        scheduledata = []
        day = datetime.datetime.now().day
        cal_month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        totalUsage = 0
        totalPrice = 0
        error = None
        building_ids = 12
        lighttotal = 0
        equipmenttotal = 0
        hvactotal = 0
        plugtotal = 0
        watertotal = 0
        othertotal =0
        daysDifference = 1
        form = HistoricalUsageForm()

        if(current_user.is_authenticated and current_user.is_admin()):
            mydb = mysql.connector.connect(
              host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
              user="readOnly",
              password="JSfB55vpSL",
              database="db_mysql_sustainergy_alldata"
            )
            mycursor = mydb.cursor()

            sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
                    
            mycursor.execute(sql,(building_id,))
            myresult = mycursor.fetchall()

            for result in myresult:
                building_address = result[0]
                buidling_description = result[1]

            today = date.today()
            userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
            correctdate = 'Mon, 21 Mar 2022'
            client_id = current_user.phone_number
            panel_building_id = building_id

            sql = "SELECT emporia_meter_sn_1 FROM electrical_panel WHERE panel_client_id = %s AND building_id = %s"
            mycursor.execute(sql,(client_id,panel_building_id))
            myresult = mycursor.fetchall()
            for x in myresult:
                serial_numbers = ','.join(x)
            serial_list = serial_numbers.split()

            if request.method == "POST":
                correctdate = request.form['datepicker']
                userdate = request.form['datepicker']
                n = 5
                userdate = userdate[n:]
                userdate = userdate.split(' ')
                months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                for i in range(0,len(months)):
                    if userdate[1] == months[i]:
                        if i < 10:
                            userdate[1] = '0' + str(i + 1)
                        else:
                            userdate[1] = str(i + 1)
                if int(userdate[0]) < 10:
                    userdate[0] = '0' + userdate[0]
                userdate = userdate[2] + '-' + userdate[1] + '-' + userdate[0]

                cal_month = str(userdate)[5] + str(userdate)[6]
                day = str(userdate)[8] + str(userdate)[9]
                daysDifference = (datetime.datetime.today() - datetime.datetime.strptime(userdate, '%Y-%m-%d')).days

                if datetime.datetime.strptime(userdate, '%Y-%m-%d') >= datetime.datetime.today():
                    userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
                    cal_month = str(userdate)[5] + str(userdate)[6]
                    day = str(userdate)[8] + str(userdate)[9]
                    year = datetime.datetime.now().year
                    error = 'Cannot select future dates'
                    daysDifference = 1
                userdate = userdate + '%'

            i = 1
            for number in serial_list:
                sql = "SELECT channel4_name, channel4_usage,channel5_name, channel5_usage,channel6_name, channel6_usage,channel7_name, channel7_usage,channel8_name, channel8_usage,channel9_name, channel9_usage,channel10_name, channel10_usage,channel11_name, channel11_usage,channel12_name, channel12_usage,channel13_name, channel13_usage,channel14_name, channel14_usage,channel15_name, channel15_usage,channel16_name, channel16_usage,channel17_name, channel17_usage,channel18_name, channel18_usage,channel19_name, channel19_usage FROM emporia_data WHERE date LIKE %s AND serial_number = %s"    
                mycursor.execute(sql, (userdate, number))
                myresult = mycursor.fetchall()
                if myresult == []:
                    userdate = (today - timedelta(days = 1)).strftime('%Y-%m-%d') + '%'
                    cal_month = str(userdate)[5] + str(userdate)[6]
                    day = str(userdate)[8] + str(userdate)[9]
                    year = datetime.datetime.now().year
                    error = 'No data for selected date'
                    daysDifference = 1
                    number = serial_list[0]
                    sql = "SELECT channel4_name, channel4_usage,channel5_name, channel5_usage,channel6_name, channel6_usage,channel7_name, channel7_usage,channel8_name, channel8_usage,channel9_name, channel9_usage,channel10_name, channel10_usage,channel11_name, channel11_usage,channel12_name, channel12_usage,channel13_name, channel13_usage,channel14_name, channel14_usage,channel15_name, channel15_usage,channel16_name, channel16_usage,channel17_name, channel17_usage,channel18_name, channel18_usage,channel19_name, channel19_usage FROM emporia_data WHERE date LIKE %s AND serial_number = %s"    
                    mycursor.execute(sql, (userdate, number))
                    myresult = mycursor.fetchall()
                for x in myresult:
                    tempstring = ','.join(x)

                stringlist = tempstring.split(',')
                for k in range(0,int(len(stringlist)/2)):
                    channel_names.append(stringlist[::2][k])
                    usage.append(float(stringlist[1::2][k]))
                for k in range(0, int(len(stringlist)/2)):
                    panels.append('Panel ' + str(i))
                i += 1

            for name in channel_names:
                name_l = name.lower()
                if 'light' in name_l or 'lights' in name_l or 'lighting' in name_l:
                    categories.append('lighting')

                elif 'hot water' in name_l or 'dhw' in name_l or 'water' in name_l or 'water heater' in name_l:
                    categories.append('dhw')

                elif 'fan' in name_l or 'heat' in name_l or 'hvac' in name_l or 'cooling' in name_l:
                    categories.append('hvac')

                elif 'motor' in name_l or 'pump' in name_l or 'compressor' in name_l or 'vacuum' in name_l or 'dryer' in name_l:
                    categories.append('equipment')
                
                elif 'plug' in name_l or 'plugs' in name_l or 'receptacle' in name_l or 'receptacle' in name_l:
                    categories.append('plugload')
                
                else:
                    categories.append('other')

            for energy in usage:
                price.append(energy * 0.09)
                percent.append((energy / sum(usage)) * 100)

            for serialNumber in serial_list:
                string = ''
                sql = "SELECT channel4_schedule, channel5_schedule, channel6_schedule, channel7_schedule, channel8_schedule, channel9_schedule, channel10_schedule, channel11_schedule, channel12_schedule, channel13_schedule, channel14_schedule, channel15_schedule, channel16_schedule, channel17_schedule, channel18_schedule, channel19_schedule FROM emporia_data WHERE date LIKE %s AND serial_number = %s"   
                mycursor.execute(sql, (userdate, serialNumber))
                myresult = mycursor.fetchall()
                for x in myresult:
                    string = "'".join(x)
                scheduledata.extend(string.split("'"))

            historicalusage = pd.DataFrame({'Channel Names': channel_names, "Usage": usage, "Price":price, "Percent":percent, "Panel Names": panels, "Category": categories,"Schedule": scheduledata})
            historicalusage = historicalusage.sort_values(by=['Usage'], ascending=False)
            channel_names = historicalusage['Channel Names'].tolist()
            usage = historicalusage['Usage'].tolist()
            price = historicalusage['Price'].tolist()
            panels = historicalusage['Panel Names'].tolist()
            percent = historicalusage['Percent'].tolist()
            categories = historicalusage['Category'].tolist()
            scheduledata = historicalusage['Schedule'].tolist()

            for i in range(0, len(usage)):
                usage[i] = float("{:.2f}".format(usage[i]/1000))
                price[i] = float("{:.2f}".format(price[i]/1000))
                percent[i] = float("{:.2f}".format(percent[i]))
                strippedPanels.append(panels[i].replace(" ",""))
                totalUsage += usage[i]
                totalPrice += price[i]

                if(categories[i] == "lighting"):
                    lighttotal += usage[i]
                if(categories[i] == "equipment"):
                    equipmenttotal += usage[i]
                if(categories[i] == "hvac"):
                    hvactotal += usage[i]
                if(categories[i] == "plugload"):
                    plugtotal += usage[i]
                if(categories[i] == "dhw"):
                    watertotal += usage[i]
                if(categories[i] == "other"):
                    othertotal += usage[i]
            
            colours = ['#3649A8','#3BCDEE','#EE5937', '#EE8F37','#90C449','#DBE2F3']
            panelchart = historicalusage.groupby(["Panel Names"]).sum()['Usage'].tolist()

            numpanels = len(np.unique(panels))
            panelnames = np.unique(panels).tolist()
            categorynames = ['Lighting', 'Equipment', 'HVAC','Plug Load','DHW','Other']
            backendnames = ['lighting', 'equipment', 'hvac','plugload','dhw','other']
            for panel in panelnames:
                strippedNames.append(panel.replace(" ",""))

            totalUsage = float("{:.2f}".format(totalUsage))
            totalPrice = float("{:.2f}".format(totalPrice))
            totalEmmissions = float("{:.2f}".format(totalUsage * 0.82))

            lighttotal = float("{:.2f}".format(((lighttotal) / (totalUsage)) * 100))
            equipmenttotal = float("{:.2f}".format(((equipmenttotal) / (totalUsage)) * 100))
            hvactotal = float("{:.2f}".format(((hvactotal) / (totalUsage)) * 100))
            plugtotal = float("{:.2f}".format(((plugtotal) / (totalUsage)) * 100))
            watertotal = float("{:.2f}".format(((watertotal) / (totalUsage)) * 100))
            othertotal = float("{:.2f}".format(((othertotal) / (totalUsage)) * 100))

            categorytotals =[lighttotal, equipmenttotal,hvactotal,plugtotal,watertotal,othertotal]
            for i in range(0,len(panelchart)):
                panelchart[i] = float("{:.2f}".format(((panelchart[i]/1000) / totalUsage) * 100))
            categoriesdf = pd.DataFrame({'Category Names': categorynames, "Total": categorytotals, "Colors": colours, "Back End": backendnames})
            categoriesdf = categoriesdf.sort_values(by=['Total'], ascending=False)
            panelcolours = []
            for i in range(0,numpanels):
                panelcolours.append(colours[i])

            panelsdf = pd.DataFrame({'Panel Names': panelnames, "Total": panelchart, "Colors": panelcolours})

            cal_db = calendar_pull(building_ids,2021, int(cal_month))
            hours = cal_db[int(day) - 1]
            starthours = hours['start_hours']
            endhours = hours['end_hours']
            starthours = str(starthours).split(':')
            starthours = starthours[0]
            endhours = str(endhours).split(':')
            endhours = endhours[0]

            if starthours == 'None':
                starthours = 24
                endhours = 0

            data = scheduledata
            totalset = []
            string = data[0]
            string = string.replace('[', '')
            string = string.replace(']', '')
            datalist = string.split(",")
            totalset = [0] * len(datalist);
            offhours = [0] * len(datalist)
            for i in range(0, len(datalist)):
                string = data[i]
                string = string.replace('[', '')
                string = string.replace(']', '')
                datalist = string.split(",")
                floatlist = []
                try:
                    for item in datalist:
                        floatlist.append(float(item))
                except:
                    whoops = 0
                for k in range(int(starthours) - 1, int(endhours) + 1):
                    totalset[k] += float(datalist[k])
                for k in range(0, len(datalist)):
                    if ((k >= int(starthours) and k <= int(endhours)) == False):
                        offhours[k] += float(datalist[k])
            for i in range(0,len(offhours)):
                if(str(offhours[i]) == 'nan'):
                    offhours[i] = 0
            for i in range(0,len(totalset)):
                if(str(totalset[i]) == 'nan'):
                    totalset[i] = 0
            onHours = float("{:.2f}".format(((sum(totalset)) / (totalUsage * 1000) * 100)))
            offHours = float("{:.2f}".format(((sum(offhours)) / (totalUsage * 1000) * 100)))
            alwaysOn = "{:.2f}".format(100 - (onHours + offHours))
            if float(alwaysOn) < 0:
                alwaysOn = 0

            timeloads = {'Name':['On-Hours','Off-Hours','Always-On'], 'Percents':[onHours,offHours,alwaysOn],'Colors':['#22B14C','#7F7F7F','#EE8F37']}
            timeloads = pd.DataFrame(data = timeloads)
            timeloadscolours = ['#22B14C','#7F7F7F','#EE8F37']

            predicted_line = {}
            last_week_full = {}
            for i in range(0,len(serial_list)):
                data = get_weekly_data(serial_list[i],30)
                channel_dict, dates = weekday_organization(data)
                last_week_cd, last_week_dp = last_week_usage(data)
                try:
                    predicted_line.update(weekly_predicted_line(channel_dict, last_week_cd))
                except:
                    whoops = 0
                last_week_full.update(last_week_cd)
            weeklabels = ['M']
            weeklabels += ([''] * 23)
            weeklabels.append('T')
            weeklabels += ([''] * 23)
            weeklabels.append('W')
            weeklabels += ([''] * 23)
            weeklabels.append('T')
            weeklabels += ([''] * 23)
            weeklabels.append('F')
            weeklabels += ([''] * 23)
            weeklabels.append('S')
            weeklabels += ([''] * 23)
            weeklabels.append('S')
            weeklabels += ([''] * 23)
            kwhgraph = []
            data = scheduledata
            string = data[0]
            string = string.replace('[', '')
            string = string.replace(']', '')
            kwhgraphlist = string.split(",")
            kwhgraph = [0] * len(kwhgraphlist)
            for i in range(0,len(kwhgraphlist)):
                string = data[i];
                string = string.replace('[', '')
                string = string.replace(']', '')
                kwhgraphlist = string.split(",")
                for k in range(0,len(kwhgraphlist)):
                    kwhgraph[k] += float(kwhgraphlist[k])

            pricegraph = []
            for i in range(0,len(kwhgraph)):
                pricegraph.append(round((kwhgraph[i]/1000) * 0.09,2))
                kwhgraph[i] = round((kwhgraph[i] / 1000),2)
            hourslist = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
            
            period = []
            typegraph = []
            jsondictionary = {}

            for i in range(0,24):
                if i < int(starthours):
                    typegraph.append('off-hrs')
                    period.append('morning')
                elif i > int(endhours):
                    typegraph.append('off-hrs')
                    period.append('night')
                else:
                    typegraph.append('on-hrs')
                    period.append('afternoon')
            jsondictionarylist = []

            for i in range(0,24):
                if str(kwhgraph[i]) == 'nan':
                    kwhgraph[i] = 0
                if str(pricegraph[i]) == 'nan':
                    pricegraph[i] = 0
                jsondictionary = {
                    "value": kwhgraph[i],
                    "hours": hourslist[i],
                    "price": pricegraph[i],
                    "type": typegraph[i],
                    "period": period[i]
                }
                jsondictionarylist.append(jsondictionary)
            with open('benchmarking_tool/static/scripts/data.json', 'w') as f:
                json.dump(jsondictionarylist, f)
            chart_colours = ['#E6E9EF'] * 24

            cal_db = calendar_pull(building_ids,2021, int(cal_month))
            hours = cal_db[int(day) - 1]
            starthours = hours['start_hours']
            endhours = hours['end_hours']
            starthours = str(starthours).split(':')
            starthours = starthours[0]
            endhours = str(endhours).split(':')
            endhours = endhours[0]

            if starthours == 'None':
                starthours = 24
                endhours = 0

            for i in range(int(starthours), int(endhours)):
                chart_colours[i] = '#FFFFFF'
            return render_template('mobilehistorical.html',error = error,daysDifference = daysDifference,  chart_colours = chart_colours,endhours = endhours,last_week_cd=last_week_full,predicted_line=predicted_line,schedule = scheduledata,timeloads = timeloads,panelsdf = panelsdf,categoriesdf = categoriesdf, onHours = onHours,offHours = offHours,alwaysOn = alwaysOn,weeklabels = weeklabels, panelchart = panelchart,lighttotal = lighttotal, equipmenttotal=  equipmenttotal, hvactotal = hvactotal, plugtotal = plugtotal, watertotal= watertotal, othertotal = othertotal, correctdate=correctdate,totalEmmissions = totalEmmissions, totalPrice =  totalPrice, totalUsage = totalUsage,categorynames = categorynames,strippedNames=strippedNames,strippedPanels=strippedPanels,panelnames=panelnames ,colours = colours, numpanels = numpanels, numcircuits = len(channel_names), categories = categories, panels = panels, percent = percent, price = price, usage = usage, channel_names = channel_names, building_id = building_id, buidling_description = buidling_description, building_address = building_address, form = form)
        else:
            abort(403)



@commercial.route('/operatinghours/<building_id>', methods=['GET', 'POST'])
@login_required
def operatinghours(building_id):
    form = OperatingHoursForm()
    if(current_user.is_authenticated and current_user.is_admin()):
        building_id = building_id
        building_ids = 12
        year = 2021
        days_per_week = 5
        start_hour = 8
        end_hour = 17
        starthours = []
        endhours = []
        startam = []
        endam = []
        startminutes = []
        endminutes = []
        month = 0
        changed = ''
        mydb = mysql.connector.connect(
          host="db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com",
          user="readOnly",
          password="JSfB55vpSL",
          database="db_mysql_sustainergy_alldata"
        )
        mycursor = mydb.cursor()
        sql = "SELECT address, description FROM buildings WHERE idbuildings = %s"
                
        mycursor.execute(sql,(building_id,))
        myresult = mycursor.fetchall()
        for result in myresult:
            building_address = result[0]
            buidling_description = result[1]

        # calendar_init(building_id, year, days_per_week, start_hour, end_hour)
        if request.method == "POST":
            month = request.form['month']
            starthours = []
            endhours = []
            startam = []
            endam = []
            changed = request.form.get('changed')
            datenumber = request.form.get('datenumber')
            bulk = request.form.get('bulk')


        month = int(month)
        cal_month = month + 1
        cal_db = calendar_pull(building_ids,year, cal_month)
        if changed == "true":
            if bulk == "single":
                newstart = request.form.get('newstart')
                newend = request.form.get('newend')
                datenumber = int(datenumber)
                startmins = request.form.get('startmins')
                endmins = request.form.get('endmins')
                starttime = newstart + ':' + startmins
                endtime = newend + ':' + endmins
                datechange = datetime.date(year,cal_month,datenumber)
                cal_db = calendar_edit(cal_db,datechange,starttime,endtime)
                calendar_update(building_ids, year,cal_db)
            if bulk == "weekday":
                newstart = request.form.get('newstart')
                newend = request.form.get('newend')
                datenumber = int(datenumber)
                startmins = request.form.get('startmins')
                endmins = request.form.get('endmins')
                starttime = newstart + ':' + startmins
                endtime = newend + ':' + endmins
                datechange = datetime.datetime(year,cal_month,datenumber)
                datechange = datechange.weekday()
                cal_db = edit_weekday_calendar(cal_db,datechange,starttime,endtime)
                calendar_update(building_ids, year,cal_db)

            if bulk == "everyday":
                newstart = request.form.get('newstart')
                newend = request.form.get('newend')
                datenumber = int(datenumber)
                startmins = request.form.get('startmins')
                endmins = request.form.get('endmins')
                starttime = newstart + ':' + startmins
                endtime = newend + ':' + endmins
                for i in range(0,6):
                    cal_db = edit_weekday_calendar(cal_db,i,starttime,endtime)
                    calendar_update(building_ids, year,cal_db)

            if bulk == "everyweekday":
                newstart = request.form.get('newstart')
                newend = request.form.get('newend')
                datenumber = int(datenumber)
                startmins = request.form.get('startmins')
                endmins = request.form.get('endmins')
                starttime = newstart + ':' + startmins
                endtime = newend + ':' + endmins
                for i in range(0,5):
                    cal_db = edit_weekday_calendar(cal_db,i,starttime,endtime)
                    calendar_update(building_ids, year,cal_db)
        for date in cal_db:
            string = date
            starthours.append(string['start_hours'])
            endhours.append(string['end_hours'])
        d = datetime.datetime(2021, cal_month, 1)
        offset = d.weekday()
        offset += 1
        starthours = rotate(starthours,offset)
        endhours = rotate(endhours,offset)

        i = 0
        for hour in starthours:
            if type(hour) == str and hour[1] == ':':
                starthours[i] = hour[0]
                starthours[i] = int(starthours[i])
                startminutes.append(hour[2] + hour[3])
            elif type(hour) == str and hour[1] != ':':
                starthours[i] = hour[0] + hour[1]
                starthours[i] = int(starthours[i])
                startminutes.append(hour[3] + hour[4])
            else:
                startminutes.append('00')
            i += 1

        i = 0
        for hour in endhours:
            if type(hour) == str and hour[1] == ':':
                endhours[i] = hour[0]
                endhours[i] = int(endhours[i])
                endminutes.append(hour[2] + hour[3])
            elif type(hour) == str and hour[1] != ':':
                endhours[i] = hour[0] + hour[1]
                endhours[i] = int(endhours[i])
                endminutes.append(hour[3] + hour[4])
            else:
                endminutes.append('00')
            i += 1 
        for i in range(len(starthours)):
            if starthours[i] is not None and starthours[i] < 13:
                startam.append("am")
            if starthours[i] is not None and starthours[i] >= 13:
                startam.append("pm")
                starthours[i] = starthours[i] - 12
            if starthours[i] is None:
                startam.append(endhours[i])

            if endhours[i] is not None and endhours[i] < 13:
                endam.append("am")
            if endhours[i] is not None and endhours[i] >= 13:
                endam.append("pm")
                endhours[i] = endhours[i] - 12
            if endhours[i] is None:
                endam.append(endhours[i])
            
        return render_template('operatinghours.html',building_address = building_address, buidling_description = buidling_description,building_id = building_id,startminutes = startminutes, endminutes = endminutes, form = form,month = month,starthours = starthours, endhours = endhours, startam = startam, endam = endam)
    else:
        abort(403)



def rotate(l, n):
    return l[-n:] + l[:-n]

@commercial.route('/clients', methods=['GET', 'POST'])
@login_required
def clients():
    form = ClientForm()
    if(current_user.is_authenticated and current_user.is_admin()):
        clients = Client.query.order_by(Client.created_at).all()
        return render_template('index.html', clients=clients, form = form)
    else:
        abort(403)

@commercial.route('/usage-day-home', methods=['GET', 'POST'])
@login_required
def usagedayhome():
    if(current_user.is_authenticated and current_user.is_admin()):
        clients = Client.query.order_by(Client.created_at).all()
        return render_template('usage-day-home.html')
    else:
        abort(403)
@commercial.route('/buildinglist', methods =['GET', 'POST'])
@login_required
def buildinglist():
    if(current_user.is_authenticated and current_user.is_admin()):
        clients = Client.query.order_by(Client.created_at).all()
        buildings = Building.query.order_by(Building.client_id).all()
        return render_template('buildinglist.html', clients=clients, buildings = buildings)
    else:
        abort(403)

@commercial.route('/arealist', methods =['GET', 'POST'])
@login_required
def arealist():
    if(current_user.is_authenticated and current_user.is_admin()):
        buildings = Building.query.order_by(Building.client_id).all()
        areas = Area.query.order_by(Area.building_id).all()
        return render_template('arealist.html', areas=areas, buildings = buildings)
    else:
        abort(403)

@commercial.route('/addclient', methods=['GET', 'POST'])
@login_required
def addclient():
    if(current_user.is_authenticated and current_user.is_admin()):
        form = ClientForm()
        if request.method == 'POST':
            company = request.form["company"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            address = request.form["address"]
            postal_code = request.form["postal_code"]
            province = request.form["province"]
            customer_id = 1
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_client = Client(photo_id=file_name,customer_id=customer_id,company=company, first_name=first_name, last_name=last_name,
                                email=email, address=address, postal_code=postal_code, province=province)
            
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('commercial.clients'))

        else:
            return render_template('add_client.html', form = form)
    else:
        abort(403)
@commercial.route('/addclient/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updateclient(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client = Client.query.get_or_404(id)
        form = ClientForm()
        if form.validate_on_submit():
            client.company = form.company.data
            client.first_name = form.first_name.data
            client.last_name = form.last_name.data 
            client.email = form.email.data 
            client.address = form.address.data 
            client.postal_code = form.postal_code.data 
            client.province = form.province.data 
            db.session.commit()
            return redirect(url_for('commercial.clients'))

        elif request.method == 'GET':
            form.company.data = client.company
            form.first_name.data = client.first_name
            form.last_name.data = client.last_name
            form.email.data = client.email
            form.address.data = client.address
            form.postal_code.data = client.postal_code
            form.province.data = client.province
        return render_template('add_client.html', form = form)
    else:
        abort(403)

@commercial.route('/addclient/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteclient(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client_id = id
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return redirect(url_for('commercial.clients'))
    else:
        abort(403)

@commercial.route('/buildingindex/<int:id>', methods=['GET', 'POST'])
@login_required
def buildingindex(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client = Client.query.get(id)
        building_id = id
        buildings = Building.query.filter_by(client_id=building_id).all()
        return render_template('buildingindex.html', client=client, buildings=buildings)
    else:
        abort(403)

@commercial.route('/buildingdetails/<int:id>', methods=['GET', 'POST'])
@login_required
def buildingdetails(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building_id = id
        building = Building.query.filter_by(id=building_id).first()
        client = Client.query.filter_by(id=building.client_id).first()
        return render_template('buildingdetails.html', client=client, building=building)
    else:
        abort(403)

@commercial.route('/onsiteaudit/<int:id>', methods=['GET', 'POST'])
@login_required
def onsiteaudit(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client = Client.query.get(id)
        building_id = id
        building = Building.query.filter_by(id=building_id).first()
        return render_template('onsiteaudit.html', client=client, building=building)
    else:
        abort(403)


@commercial.route('/addbuilding/<int:id>', methods=['GET', 'POST'])
@login_required
def addbuilding(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        client = Client.query.get(id)
        form = BuildingForm()
        if request.method == 'POST':
            building_name = request.form["building_name"]
            address = request.form["address"]
            city = request.form["city"]
            province = request.form["province"]
            postal_code = request.form["postal_code"]
            square_footage = request.form["square_footage"]
            building_photo = request.files.get('building_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(building_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_building = Building(photo_id=file_name,name=building_name, address=address, city=city, province=province,
                                    postal_code=postal_code, square_footage=square_footage, client_id=id)
            try:
                db.session.add(new_building)
                db.session.commit()
                building_id = id
                buildings = Building.query.filter_by(client_id=building_id).all()
                return redirect('/commercial/buildingindex/' + str(id))
            except:
                return "There was an error adding building"
        else:
            return render_template('addbuilding.html', client=client,form=form)
    else:
        abort(403)

@commercial.route('/addbuilding/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatebuilding(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get_or_404(id)
        client = building.client_id
        form = BuildingForm()
        if form.validate_on_submit():
            building.name = form.building_name.data
            building.address = form.address.data
            building.city = form.city.data 
            building.province = form.province.data 
            building.postal_code = form.postal_code.data 
            building.square_footage = form.square_footage.data 
            db.session.commit()
            return redirect(url_for('commercial.buildingindex', client = client, id = client))

        elif request.method == 'GET':
            form.building_name.data = building.name
            form.address.data = building.address
            form.city.data = building.city
            form.province.data = building.province
            form.postal_code.data = building.postal_code
            form.square_footage.data = building.square_footage
        return render_template('addbuilding.html', form = form, client = client)
    else:
        abort(403)


@commercial.route('/addbuilding/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletebuilding(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        buidling = Building.query.get_or_404(id)
        area = buidling.client_id
        db.session.delete(buidling)
        db.session.commit()
        return redirect(url_for('commercial.buildingindex',area = area, id = area))
    else:
        abort(403)

@commercial.route('/utilityindex/<int:id>', methods=['GET', 'POST'])
@login_required
def utilityindex(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        meter_id = id
        meters = Meter.query.filter_by(building_id=meter_id).all()
        return render_template('utility_index.html', building=building, meters=meters)
    else:
        abort(403)

@commercial.route('/utilityinfoupload/<int:id>', methods=['GET', 'POST'])
@login_required
def utilityupload(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        meter_id = id
        meters = Meter.query.filter_by(building_id=meter_id).all()
        if request.method == 'POST':
            distributer = request.form["distributer"]
            meter_number = request.form["meter_number"]
            account_number = request.form["account_number"]
            energy_type = request.form["energy_type"]
            new_meter = Meter(distributer=distributer, meter_number=meter_number,
                              account_number=account_number, energy_type=energy_type, building=building)
            db.session.add(new_meter)
            db.session.commit()
            return redirect('/utilityindex/'+str(id))
            # except:
            # return "There was an error adding meter"
        else:
            return render_template("add_meter.html", building=building, meters=meters)
    else:
        abort(403)

@commercial.route('/constructionindex/<int:id>', methods=['GET', 'POST'])
@login_required
def construction(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        construction_id = id
        exteriorwalls = ExteriorWall.query.filter_by(building_id=construction_id).all()
        foundations = Foundation.query.filter_by(building_id=construction_id).all()
        roofs = Roof.query.filter_by(building_id=construction_id).all()
        rooffinishs = RoofFinish.query.filter_by(building_id=construction_id).all()
        return render_template('constructionindex.html', building=building, building_id = id, exteriorwalls=exteriorwalls, foundations=foundations,roofs=roofs,rooffinishs = rooffinishs)
    else:
        abort(403)

@commercial.route('/addconstruction/<int:id>', methods=['GET', 'POST'])
@login_required
def addconstruction(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        construction_id = id
        exteriorwalls = ExteriorWall.query.filter_by(building_id=construction_id).all()
        foundations = Foundation.query.filter_by(building_id=construction_id).all()
        roofs = Roof.query.filter_by(building_id=construction_id).all()
        rooffinishs = RoofFinish.query.filter_by(building_id=construction_id).all()
        return render_template('addconstruction.html', building=building, building_id = id, exteriorwalls=exteriorwalls, foundations=foundations,roofs=roofs,rooffinishs = rooffinishs)
    else:
        abort(403)
@commercial.route('/addexteriorwall/<int:id>', methods=['GET', 'POST'])
@login_required
def addexteriorwall(id): 
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        exteriorwall_id = id
        exteriorwalls = ExteriorWall.query.filter_by(building_id=exteriorwall_id).all()
        form = ExteriorWallForm()
        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_exteriorwall = ExteriorWall(photo_id=file_name,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_exteriorwall)
            db.session.commit()
            return redirect('/commercial/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addexteriorwall.html', building=building, exteriorwalls=exteriorwalls,form=form)
    else:
        abort(403)

@commercial.route('/addexteriorwall/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteexteriorwall(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        exteriorwall = ExteriorWall.query.get_or_404(id)
        buidling = exteriorwall.building_id
        db.session.delete(exteriorwall)
        db.session.commit()
        return redirect(url_for('commercial.construction',buidling = buidling, id = buidling))
    else:
        abort(403)
@commercial.route('/addroof/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteroof(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        roof = Roof.query.get_or_404(id)
        buidling = roof.building_id
        db.session.delete(roof)
        db.session.commit()
        return redirect(url_for('commercial.construction',building = building, id = buidling))
    else:
        abort(403)
@commercial.route('/addrooffinish/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleterooffinish(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        rooffinish = RoofFinish.query.get_or_404(id)
        buidling = rooffinish.building_id
        db.session.delete(rooffinish)
        db.session.commit()
        return redirect(url_for('commercial.construction',buidling = buidling, id = buidling))
    else:
        abort(403)
@commercial.route('/addfoundation/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletefoundation(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        foundation = Foundation.query.get_or_404(id)
        buidling = foundation.building_id
        db.session.delete(foundation)
        db.session.commit()
        return redirect(url_for('commercial.construction',buidling = buidling, id = buidling))
    else:
        abort(403)

@commercial.route('/addexteriorwall/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updateexteriorwall(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        exteriorwall = ExteriorWall.query.get(id)
        buidling = Building.query.filter_by(id=exteriorwall.building_id).first()
        form = ExteriorWallForm()
        if request.method == 'POST':
            exteriorwall.material = form.material.data
            exteriorwall.rvalue = form.rvalue.data
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            exteriorwall.photo_id = file_name
            db.session.commit()
            return redirect(url_for('commercial.construction', buidling = buidling, id = buidling.id))
        elif request.method == 'GET':
                form.material.data = exteriorwall.material
                form.rvalue.data = exteriorwall.rvalue
                return render_template('addexteriorwall.html', form = form, building = building, exteriorwall = exteriorwall)
    else:
        abort(403)
@commercial.route('/addroof/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updateroof(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        roof = Roof.query.get(id)
        buidling = Building.query.filter_by(id=roof.building_id).first()
        form = RoofForm()
        if request.method == 'POST':
            roof.material = form.material.data
            roof.rvalue = form.rvalue.data
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            roof.photo_id = file_name
            db.session.commit()
            return redirect(url_for('commercial.construction', buidling = buidling, id = buidling.id))
        elif request.method == 'GET':
                form.material.data = roof.material
                form.rvalue.data = roof.rvalue
                return render_template('addroof.html', form = form, building = building, roof = roof)
    else:
        abort(403)
@commercial.route('/addrooffinish/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updaterooffinish(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        rooffinish = RoofFinish.query.get(id)
        buidling = Building.query.filter_by(id=rooffinish.building_id).first()
        form = RoofFinishForm()
        if request.method == 'POST':
            rooffinish.material = form.material.data
            rooffinish.rvalue = form.rvalue.data
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            rooffinish.photo_id = file_name
            db.session.commit()
            return redirect(url_for('commercial.construction', buidling = buidling, id = buidling.id))
        elif request.method == 'GET':
                form.material.data = rooffinish.material
                form.rvalue.data = rooffinish.rvalue
                return render_template('addrooffinish.html', form = form, building = building, rooffinish = rooffinish)
          
    else:
        abort(403)
@commercial.route('/addfoundation/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatefoundation(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        foundation = Foundation.query.get(id)
        buidling = Building.query.filter_by(id=foundation.building_id).first()
        form = FoundationForm()
        if request.method == 'POST':
            foundation.material = form.material.data
            foundation.rvalue = form.rvalue.data
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            foundation.photo_id = file_name
            db.session.commit()
            return redirect(url_for('commercial.construction', buidling = buidling, id = buidling.id))
        
        elif request.method == 'GET':
                form.foundation_type.dat = foundation.foundation_type
                form.material.data = foundation.material
                form.rvalue.data = foundation.rvalue
                form.rx.data = foundation.rx
                return render_template('addfoundation.html', form = form, building = building, foundation = foundation)
           
    else:
        abort(403)
@commercial.route('/addroof/<int:id>', methods=['GET', 'POST'])
@login_required
def addroof(id): 
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        roof_id = id
        roofs = Roof.query.filter_by(building_id=buidling_id).all()
        form = RoofForm()
        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_roof = Roof(photo_id=file_name,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_roof)
            db.session.commit()
            return redirect('/commercial/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addroof.html', building=building, roofs=roofs,form=form)
    else:
        abort(403)
@commercial.route('/addrooffinish/<int:id>', methods=['GET', 'POST'])
@login_required
def addrooffinish(id): 
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        rooffinish_id = id
        rooffinishs = RoofFinish.query.filter_by(building_id=rooffinish_id).all()
        form = RoofFinishForm()
        if request.method == 'POST':
            material = request.form["material"]
            rvalue = request.form["rvalue"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_rooffinish = RoofFinish(photo_id=file_name,material=material, rvalue=rvalue, building_id = building.id)
            db.session.add(new_rooffinish)
            db.session.commit()
            return redirect('/commercial/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addrooffinish.html', building=building, rooffinishs=rooffinishs,form=form)
    else:
        abort(403)
@commercial.route('/addfoundation/<int:id>', methods=['GET', 'POST'])
@login_required
def addfoundation(id): 
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        foundation_id = id
        foundations = Foundation.query.filter_by(building_id=foundation_id).all()
        form = FoundationForm()
        if request.method == 'POST':
            foundation_type = request.form["foundation_type"]
            material = request.form["material"]
            rx = request.form["rx"]
            rvalue = request.form["rvalue"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_foundation = Foundation(photo_id=file_name,material=material, rvalue=rvalue, foundationtype = foundation_type, rx=rx, building_id = building.id)
            db.session.add(new_foundation)
            db.session.commit()
            return redirect('/commercial/constructionindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addfoundation.html', building=building, foundations=foundations,form=form)
    else:
        abort(403)


@commercial.route('/areaindex/<int:id>', methods=['GET', 'POST'])
@login_required
def areas(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        area_id = id
        client = Client.query.filter_by(id=building.client_id).first()
        areas = Area.query.filter_by(building_id=area_id).all()
        if request.method == 'POST':
            name = request.form['name']
            new_room = Area(name=name, building=building)
            try:
                db.session.add(new_room)
                db.session.commit()
                building = Building.query.get(id)
                area_id = id
                areas = Area.query.filter_by(building_id=area_id)
                return redirect('/areaindex/'+str(id))
            except:
                "There was an error adding area"
        else:
            return render_template('area_index.html', building=building, areas=areas, client=client)
    else:
        abort(403)

@commercial.route('/areaequipment/<int:id>', methods=['GET', 'POST'])
@login_required
def areaequipment(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area_id = id
        area = Area.query.filter_by(id=area_id).first()
        building = Building.query.filter_by(id = area.building_id).first()
        return render_template('area_equipment.html', building=building, area=area)
    else:
        abort(403)

@commercial.route('/addarea/<int:id>', methods=['GET', 'POST'])
@login_required
def addarea(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        area_id = id
        form = AreaForm()
        areas = Area.query.filter_by(building_id=area_id).all()
        if request.method == 'POST':
            name = request.form['name']
            areaphoto1 = request.files.get('areaphoto1', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(areaphoto1,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            areaphoto2 = request.files.get('areaphoto2', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name2 = save_picture_appliance(areaphoto2,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_room = Area(name=name, building=building, photo_id1 = file_name, photo_id2 = file_name2)
            try:
                db.session.add(new_room)
                db.session.commit()
                building = Building.query.get(id)
                area_id = id
                areas = Area.query.filter_by(building_id=area_id)
                return redirect('/commercial/areaindex/'+str(id))
            except:
                "There was an error adding area"
        else:
            return render_template('addarea.html', building=building, areas=areas, form = form)
    else:
        abort(403)
@commercial.route('/updatearea/<int:id>', methods=['GET', 'POST'])
@login_required
def updatearea(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = AreaForm()
        if form.validate_on_submit():
            area.name = form.name.data
            db.session.commit()
            return redirect(url_for('commercial.areas', building = building, id = building))

        elif request.method == 'GET':
            form.name.data = area.name
        return render_template('addarea.html', form = form, building = building)
    else:
        abort(403)


@commercial.route('/areaindex/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletearea(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area_obj = Area.query.get_or_404(id)
        area = area_obj.building_id
        db.session.delete(area_obj)
        db.session.commit()
        return redirect(url_for('commercial.areas',area = area, id = area))
    else:
        abort(403)  

@commercial.route('/lightindex/<int:id>', methods=['GET', 'POST'])
@login_required
def lightindex(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        light_id = id
        lights = Light.query.filter_by(area_id=light_id).all()
        return render_template('lightindex.html', area=area, lights=lights)
    else:
        abort(403)

@commercial.route('/addlight/<int:id>', methods=['GET', 'POST'])
@login_required
def lights(id):
    if(current_user.is_authenticated and current_user.is_admin()):

        area = Area.query.get(id)
        building = area.building_id
        light_id = id
        lights = Light.query.filter_by(area_id=light_id).all()
        form = LightForm()

        if request.method == 'POST':
            fixture_count = request.form["fixtures"]
            hours = request.form["hours"]
            fixture = request.form["fixture_type"]
            lamp = request.form["lamp_type"]
            wattage = request.form["wattage"]
            lamp_count = request.form["lamp_count"]
            building_photo = request.files.get('building_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(building_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_light = Light(photo_id=file_name,fixture_count=fixture_count, hours=hours, fixture=fixture, lamp=lamp,
                              wattage=wattage, lamp_count=lamp_count, area = area, building_id = building)
            db.session.add(new_light)
            db.session.commit()
            return redirect('/commercial/lightindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('addlight.html', area=area, lights=lights,form=form)
    else:
        abort(403)
@commercial.route('/duplicatelight/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatelight(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        light_id = id
        light = Light.query.get(id)
        form = LightForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_light = Light(photo=light.photo,fixture_count=light.fixture_count, hours=light.hours, fixture=light.fixture, lamp=light.lamp,
                              wattage=light.wattage, lamp_count=light.lamp_count, area = light.area, building_id = light.building_id)
            db.session.add(new_light)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.lightindex', id = light.area_id))
    else:
        abort(403)
@commercial.route('/addlight/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatelight(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        light = Light.query.get(id)
        area = Area.query.filter_by(id=light.area_id).first()
        form = LightForm()
        if form.validate_on_submit():
            light.fixture_count = form.fixtures.data
            light.hours = form.hours.data
            light.fixture = form.fixture_type.data 
            light.lamp = form.lamp_type.data 
            light.wattage = form.wattage.data 
            light.lamp_count = form.lamp_count.data 
            building_photo = request.files.get('building_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(building_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            light.photo_id = file_name
            db.session.commit()
            return redirect(url_for('commercial.lightindex', area = area, id = area.id))

        elif request.method == 'GET':
            form.fixtures.data = light.fixture_count
            form.hours.data = light.hours
            form.fixture_type.data = light.fixture
            form.lamp_type.data = light.lamp
            form.wattage.data = light.wattage
            form.lamp_count.data = light.lamp_count
        return render_template('addlight.html', form = form, area = area, light = light)
    else:
        abort(403)
@commercial.route('/addlight/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletelight(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        light = Light.query.get_or_404(id)
        area = light.area_id
        db.session.delete(light)
        db.session.commit()
        return redirect(url_for('commercial.lightindex',area = area, id = area))
    else:
        abort(403)

@commercial.route('/equipmentindex/<int:id>', methods=['GET', 'POST'])
@login_required
def equipmentindex(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        area_id = id
        appliances = CommercialAppliance.query.filter_by(area_id=area_id).all()
        return render_template('equipmentindex.html', area=area,appliances=appliances)
    else:
        abort(403)

@commercial.route('/dhwindex/<int:id>', methods=['GET', 'POST'])
@login_required
def dhwindex(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        area_id = id
        dhws = CommercialDHW.query.filter_by(area_id=area_id).all()
        return render_template('dhwindex.html', area=area,dhws=dhws)
    else:
        abort(403)

@commercial.route('/hvac_index/<int:id>', methods=['GET', 'POST'])
@login_required
def hvaclist(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        form = FurnaceForm()
        area = Area.query.get(id)
        area_id = id
        furnaces = Furnace.query.filter_by(area_id=area_id).all()
        chillers = Chiller.query.filter_by(area_id=area_id).all()
        pumps = Pump.query.filter_by(area_id=area_id).all()
        motors = Motor.query.filter_by(area_id=area_id).all()
        hydronic_boilers = Hydronic_Boiler.query.filter_by(area_id=area_id).all()
        steam_boilers = Steam_Boiler.query.filter_by(area_id=area_id).all()
        heat_pumps = HeatPump.query.filter_by(area_id=area_id).all()
        ahus = AHU.query.filter_by(area_id=area_id).all()
        gas_fired_heating_coils = GasFiredHeatingCoil.query.filter_by(area_id=area_id).all()
        electric_rest_heating_coils = ElectricRestHeatingCoil.query.filter_by(area_id=area_id).all()
        condensing_unit_systems = CondensingUnitSystem.query.filter_by(area_id=area_id).all()
        window_air_conditioners = WindowAirConditioner.query.filter_by(area_id=area_id).all()

        infrared_heaters = InfraredHeater.query.filter_by(area_id=area_id).all()
        make_up_air_units = MakeUpAirUnit.query.filter_by(area_id=area_id).all()
        mini_split_systems = MiniSplitSystem.query.filter_by(area_id=area_id).all()
        packaged_rtus = PackagedRTU.query.filter_by(area_id=area_id).all()
        packaged_terminal_acs = PackagedTerminalAC.query.filter_by(area_id=area_id).all()
        self_contained_ahus = SelfContainedAHU.query.filter_by(area_id=area_id).all()
        unit_heaters = UnitHeater.query.filter_by(area_id=area_id).all()
        unit_ventilators = UnitVentilator.query.filter_by(area_id=area_id).all()
        return render_template('hvac_index.html',area=area, furnaces=furnaces,chillers=chillers,pumps=pumps,motors=motors,hydronic_boilers=hydronic_boilers,steam_boilers=steam_boilers,
            heat_pumps=heat_pumps,window_air_conditioners=window_air_conditioners,ahus=ahus,gas_fired_heating_coils=gas_fired_heating_coils,electric_rest_heating_coils=electric_rest_heating_coils,condensing_unit_systems=condensing_unit_systems,
            infrared_heaters= infrared_heaters,make_up_air_units=make_up_air_units,mini_split_systems=mini_split_systems,packaged_rtus=packaged_rtus,packaged_terminal_acs=packaged_terminal_acs,
            self_contained_ahus=self_contained_ahus,unit_heaters=unit_heaters,unit_ventilators=unit_ventilators, form = form)
    else:
        abort(403)


@commercial.route('/adddhw/<int:id>', methods=['GET', 'POST'])
@login_required
def adddhw(id):
    if(current_user.is_authenticated and current_user.is_admin()):

        area = Area.query.get(id)
        building = area.building_id
        dhw_id = id
        dhws = CommercialDHW.query.filter_by(area_id=dhw_id).all()
        form = DHWForm()

        if request.method == 'POST':
            equipment_type = request.form["equipment_type"]
            tag = request.form["tag"]
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            input_capacity = request.form["input_capacity"]
            fuel_type = request.form["fuel_type"]
            efficiency = request.form["efficiency"]
            storage_volume = request.form["storage_volume"]
            set_point = request.form["set_point"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_dhw = CommercialDHW(photo_id=file_name, equipment_type=equipment_type, tag=tag, manufacturer=manufacturer, model_number=model_number,
                          serial_number=serial_number, input_capacity=input_capacity, fuel_type=fuel_type, efficiency=efficiency, storage_volume=storage_volume, set_point=set_point, area=area,building_id = building)
            db.session.add(new_dhw)
            db.session.commit()
            return redirect('/commercial/dhwindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('add_dhw_equipment.html', area=area, dhws=dhws, form=form)
    else:
        abort(403)

@commercial.route('/adddhw/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updatedhw(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        dhw = CommercialDHW.query.get(id)
        area = dhw.area_id
        form = DHWForm()
        if form.validate_on_submit():
            dhw.equipment_type = form.equipment_type.data
            dhw.tag = form.tag.data
            dhw.manufacturer = form.manufacturer.data
            dhw.model_number = form.model_number.data
            dhw.serial_number = form.serial_number.data 
            dhw.input_capacity = form.input_capacity.data 
            dhw.fuel_type = form.fuel_type.data 
            dhw.efficiency = form.efficiency.data 
            dhw.storage_volume = form.storage_volume.data 
            dhw.set_point = form.set_point.data 
            db.session.commit()
            return redirect(url_for('commercial.dhwindex', area = area, id = area))

        elif request.method == 'GET':
            form.equipment_type.data = dhw.equipment_type
            form.tag.data = dhw.tag
            form.manufacturer.data = dhw.manufacturer
            form.model_number.data = dhw.model_number
            form.input_capacity.data = dhw.input_capacity
            form.fuel_type.data = dhw.fuel_type
            form.efficiency.data = dhw.efficiency
            form.storage_volume.data = dhw.storage_volume
            form.set_point.data = dhw.set_point
            form.set_point.data = dhw.set_point

        return render_template('add_dhw_equipment.html', form = form, area = area)
    else:
        abort(403)

@commercial.route('/adddhw/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletedhw(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        dhw = CommercialDHW.query.get_or_404(id)
        area = dhw.area_id
        db.session.delete(dhw)
        db.session.commit()
        return redirect(url_for('commercial.dhwindex',area = area, id = area))
    else:
        abort(403)

@commercial.route('/duplicatedhw/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatedhw(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        dhw_id = id
        dhw = CommercialDHW.query.get(id)
        form = DHWForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_dhw = DHW(photo=dhw.photo, equipment_type=dhw.equipment_type, tag=dhw.tag, manufacturer=dhw.manufacturer, model_number=dhw.model_number,
                          serial_number=dhw.serial_number, input_capacity=dhw.input_capacity, fuel_type=dhw.fuel_type, efficiency=dhw.efficiency, storage_volume=dhw.storage_volume, set_point=dhw.set_point, area=dhw.area,building_id = dhw.building)
            db.session.add(new_dhw)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.dhwindex', id = dhw.area_id))
    else:
        abort(403)

@commercial.route('/addappliance/<int:id>', methods=['GET', 'POST'])
@login_required
def appliance(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        appliance_id = id
        appliances = CommercialAppliance.query.filter_by(area_id=appliance_id).all()
        form = ApplianceForm()

        if request.method == 'POST':
            appliance_type = request.form["appliance_type"]
            quantity = request.form["quantity"]
            wattage = request.form["wattage"]
            pump_photo = request.files.get('pump_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(pump_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            new_appliance = CommercialAppliance(photo_id=file_name,
                appliance_type=appliance_type, quantity=quantity, wattage=wattage, area=area, building_id = building)
            db.session.add(new_appliance)
            db.session.commit()
            return redirect('/commercial/equipmentindex/'+str(id))
            # except:
            #   return "There was an error adding light"
        else:
            return render_template('add_appliance_equipment.html', area=area, appliances=appliances, form=form)
    else:
        abort(403)
@commercial.route('/addappliance/<int:id>/update', methods=['GET', 'POST'])
@login_required
def updateappliance(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        appliance = CommercialAppliance.query.get_or_404(id)
        area = Area.query.filter_by(id=appliance.area_id).first()
        form = ApplianceForm()
        if form.validate_on_submit():
           appliance.appliance_type = form.appliance_type.data
           appliance.quantity = form.quantity.data
           appliance.wattage = form.wattage.data 
           pump_photo = request.files.get('pump_photo', None)
           target = os.path.join(app_root, 'static/appliance_photos/img')
           file_name = save_picture_appliance(pump_photo,'appliance_photos/img/')
           destination = '/'.join([target, file_name])
           appliance.photo_id = file_name
           db.session.commit()
           return redirect('/commercial/equipmentindex/'+str(area.id))

        elif request.method == 'GET':
            form.appliance_type.data = appliance.appliance_type   
            form.quantity.data = appliance.quantity
            form.wattage.data = appliance.wattage 
        return render_template('add_appliance_equipment.html', form = form, area = area, appliance = appliance)
    else:
        abort(403)
@commercial.route('/addappliance/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteappliance(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        appliance = CommercialAppliance.query.get_or_404(id)
        area = appliance.area_id
        db.session.delete(appliance)
        db.session.commit()
        return redirect(url_for('commercial.equipmentindex',area = area, id = area))
    else:
        abort(403)

@commercial.route('/duplicateappliance/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateappliance(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        appliance_id = id
        appliance = CommercialAppliance.query.get(id)
        form = ApplianceForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_appliance = Appliance(photo=appliance.photo,
                appliance_type=appliance.appliance_type, quantity=appliance.quantity, wattage=appliance.wattage, building_id = appliance.building,
                          serial_number=appliance.serial_number, input_capacity=appliance.input_capacity, fuel_type=appliance.fuel_type, efficiency=appliance.efficiency, storage_volume=appliance.storage_volume, set_point=appliance.set_point, area=appliance.area)
            db.session.add(new_appliance)
            db.session.commit()
            loop += 1
        return redirect(url_for('commercial.equipmentindex', id = appliance.area_id))
    else:
        abort(403)


@commercial.route('/uploadbills/<int:id>', methods=['GET', 'POST'])
@login_required
def uploadbills(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        meter = Meter.query.get(id)
        meter_number = meter.meter_number
        bill_id=id
        bills = Utility_Bill.query.filter_by(meter_number=meter_number).all()

        if request.method == 'POST':

            def Utility_Bill_init_func(row):
                p = Utility_Bill(row['start_date'],
                                 row['end_date'], row['usage'], row['cost'], meter_number)
                return p

            request.save_to_database(
                field_name='file', session=db.session,
                table=Utility_Bill,
                initializer=Utility_Bill_init_func)

            return redirect('/billindex/'+ str(id))

        return render_template('utility_uploader.html', meter=meter, bills=bills)
    else:
        abort(403)





@commercial.route("/billindex/<int:id>", methods=['GET', 'POST'])
@login_required
def bill(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        meter = Meter.query.get(id)
        meter_number = meter.meter_number
        bill_id=id
        bills = Utility_Bill.query.filter_by(meter_number=meter_number).all()
        def Utility_Bill_init_func(row):
            p = Utility_bill(row['start_date'],
                         row['end_date'], row['usage'], row['cost'], meter_number)
            bills=p.query.filter_by(meter_number=meter_number).all()
    #try swapping def
            return excel.make_response_from_tables(db.session, [p], 'handsontable.html')
        return ""
    else:
        abort(403)


@commercial.route("/add_steam_boiler/<int:id>", methods=['GET', 'POST'])
@login_required
def add_steam_boiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        form = SteamBoilerForm()
        building = area.building_id

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            boiler_type = request.form["boiler_type"]
            pressure = request.form["pressure"]
            area_id = id
            steam_photo = request.files.get('steam_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(steam_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            steam_boiler = Steam_Boiler(building_id = building, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,boiler_type=boiler_type,pressure=pressure,area_id=id,photo_id=file_name)
            db.session.add(steam_boiler)
            db.session.commit()
            return redirect('/commercial/hvac_index/'+str(id))

        else:
            return render_template('add_hvac_equipment.html', add='steam_boiler',area=area,form=form)
    else:
        abort(403)


@commercial.route("/add_steam_boiler/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_steam_boiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        steam_boiler = Steam_Boiler.query.get_or_404(id)
        area = steam_boiler.area_id
        form = SteamBoilerForm()
        if form.validate_on_submit():
           steam_boiler.manufacturer = form.manufacturer.data
           steam_boiler.model_number = form.model_number.data
           steam_boiler.serial_number = form.serial_number.data 
           steam_boiler.year_built = form.year_built.data
           steam_boiler.input_capacity = form.input_capacity.data
           steam_boiler.output_capacity = form.output_capacity.data 
           steam_boiler.effciency = form.heating_eff.data
           steam_boiler.boiler_type = form.boiler_type.data
           steam_boiler.pressure = form.pressure.data 
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = steam_boiler.manufacturer   
            form.model_number.data = steam_boiler.model_number
            form.serial_number.data = steam_boiler.serial_number 
            form.year_built.data = steam_boiler.year_built
            form.input_capacity.data = steam_boiler.input_capacity   
            form.output_capacity.data = steam_boiler.output_capacity
            form.heating_eff.data = steam_boiler.effciency 
            form.boiler_type.data = steam_boiler.boiler_type   
            form.pressure.data = steam_boiler.pressure
        return render_template('add_hvac_equipment.html', add='steam_boiler',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_steam_boiler/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletesteamboiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        steam_boiler = Steam_Boiler.query.get_or_404(id)
        area = steam_boiler.area_id
        db.session.delete(steam_boiler)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicatesteamboiler/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatesteamboiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        steamboiler_id = id
        steamboiler = Steam_Boiler.query.get(id)
        form = SteamBoilerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            steam_boiler = Steam_Boiler(building_id = steamboiler.building, manufacturer=steamboiler.manufacturer,model_number=steamboiler.model_number,serial_number=steamboiler.serial_number,year_built=steamboiler.year_built,input_capacity=steamboiler.input_capacity,output_capacity=steamboiler.output_capacity,effciency=steamboiler.heating_eff,boiler_type=steamboiler.boiler_type,pressure=steamboiler.pressure,area=steamboiler.area,photo=steamboiler.photo)
            db.session.add(steam_boiler)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.hvacindex', id = steamboiler.area_id))
    else:
        abort(403)

@commercial.route("/add_hydronic_boiler/<int:id>", methods=['GET', 'POST'])
@login_required
def add_hydronic_boiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = HydronicBoilerForm()
        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            type_boiler = request.form["boiler_type"]
            lhwt = request.form["lhwt"]
            ehwt = request.form['ehwt']
            hydronic_photo = request.files.get('hydronic_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(hydronic_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            hydronic_boiler = Hydronic_Boiler(building_id = building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,boiler_type=type_boiler,lhwt=lhwt,ehwt=ehwt,area_id=id)
            try:
                db.session.add(hydronic_boiler)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding boiler"
        else:
            return render_template('add_hvac_equipment.html', add='hydronic_boiler',area=area, form=form)
    else:
        abort(403)

@commercial.route("/add_hydronic_boiler/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_hydronic_boiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        hydronic_boiler = Hydronic_Boiler.query.get_or_404(id)
        area = hydronic_boiler.area_id
        form = HydronicBoilerForm()
        if form.validate_on_submit():
           hydronic_boiler.manufacturer = form.manufacturer.data
           hydronic_boiler.model_number = form.model_number.data
           hydronic_boiler.serial_number = form.serial_number.data 
           hydronic_boiler.year_built = form.year_built.data
           hydronic_boiler.input_capacity = form.input_capacity.data
           hydronic_boiler.output_capacity = form.output_capacity.data 
           hydronic_boiler.effciency = form.heating_eff.data
           hydronic_boiler.boiler_type = form.boiler_type.data
           hydronic_boiler.lhwt = form.lhwt.data
           hydronic_boiler.ehwt = form.ehwt.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = hydronic_boiler.manufacturer   
            form.model_number.data = hydronic_boiler.model_number
            form.serial_number.data = hydronic_boiler.serial_number 
            form.year_built.data = hydronic_boiler.year_built
            form.input_capacity.data = hydronic_boiler.input_capacity   
            form.output_capacity.data = hydronic_boiler.output_capacity
            form.heating_eff.data = hydronic_boiler.effciency 
            form.boiler_type.data = hydronic_boiler.boiler_type   
            form.lhwt.data = hydronic_boiler.lhwt
            form.ehwt.data = hydronic_boiler.ehwt
        return render_template('add_hvac_equipment.html', add='hydronic_boiler',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_hydronic_boiler/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletehydronicboiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        hydronic_boiler = Hydronic_Boiler.query.get_or_404(id)
        area = hydronic_boiler.area_id
        db.session.delete(hydronic_boiler)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicatehydronicboiler/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatehydronicboiler(id):
    if(current_user.is_authenticated and current_user.is_admin()):

        hydronicboiler_id = id
        hydronicboiler = Hydronic_Boiler.query.get(id)
        form = HydronicBoilerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            hydronic_boiler = Hydronic_Boiler(building_id = hydronicboiler.building,photo=hydronicboiler.photo, manufacturer=hydronicboiler.manufacturer,model_number=hydronicboiler.model_number,serial_number=hydronicboiler.serial_number,year_built=hydronicboiler.year_built,input_capacity=hydronicboiler.input_capacity,output_capacity=hydronicboiler.output_capacity,effciency=hydronicboiler.heating_eff,boiler_type=hydronicboiler.type_boiler,lhwt=hydronicboiler.lhwt,ehwt=hydronicboiler.ehwt,area=hydronicboiler.area)
            db.session.add(hydronic_boiler)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = hydronicboiler.area_id))
    else:
        abort(403)


@commercial.route("/add_furnace/<int:id>", methods=['GET', 'POST'])
@login_required
def add_furnace(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = FurnaceForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            furnace_photo = request.files.get('furnace_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(furnace_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            furnace = Furnace(building_id = building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,area_id=id)
            try:
                db.session.add(furnace)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding furnace"
        else:
            return render_template('add_hvac_equipment.html', add='furnace',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_furnace/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_furnace(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        furnace = Furnace.query.get_or_404(id)
        area = furnace.area_id
        form = FurnaceForm()
        if form.validate_on_submit():
           furnace.manufacturer = form.manufacturer.data
           furnace.model_number = form.model_number.data
           furnace.serial_number = form.serial_number.data 
           furnace.year_built = form.year_built.data
           furnace.input_capacity = form.input_capacity.data
           furnace.output_capacity = form.output_capacity.data 
           furnace.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = furnace.manufacturer   
            form.model_number.data = furnace.model_number
            form.serial_number.data = furnace.serial_number 
            form.year_built.data = furnace.year_built
            form.input_capacity.data = furnace.input_capacity   
            form.output_capacity.data = furnace.output_capacity
            form.heating_eff.data = furnace.effciency 
        return render_template('add_hvac_equipment.html', add='furnace',area=area,form=form)
    else:
        abort(403)




@commercial.route('/add_furnace/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletefurnace(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        Furnace.query.filter(Furnace.id==id).delete()
        db.session.commit()
        return redirect(url_for('commercial.hvac',id = 1))
    else:
        abort(403)


@commercial.route('/duplicatefurnace/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatefurnace(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        furnace_id = id
        furnace = Furnace.query.get(id)
        form = FurnaceForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_furnace = Furnace(building_id = furnace.building,photo=furnace.photo, manufacturer=furnace.manufacturer,model_number=furnace.model_number,serial_number=furnace.serial_number,year_built=furnace.year_built,input_capacity=furnace.input_capacity,output_capacity=furnace.output_capacity,effciency=furnace.heating_eff,area=furnace.area)
            db.session.add(new_furnace)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = furnace.area_id))
    else:
        abort(403)


@commercial.route("/add_unit_heater/<int:id>", methods=['GET', 'POST'])
@login_required
def add_unit_heater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = UnitHeaterForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            supply_air_temp = request.form["supply_air_temp"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            unit_photo = request.files.get('unit_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(unit_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            unit_heater = UnitHeater(building_id = building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,supply_air_temp=supply_air_temp,area_id=id)
            try:
                db.session.add(unit_heater)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding unit heater"
        else:
            return render_template('add_hvac_equipment.html', add='unit_heater',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_unit_heater/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_unit_heater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        unit_heater = UnitHeater.query.get_or_404(id)
        area = unit_heater.area_id
        form = UnitHeaterForm()
        if form.validate_on_submit():
           unit_heater.manufacturer = form.manufacturer.data
           unit_heater.model_number = form.model_number.data
           unit_heater.serial_number = form.serial_number.data 
           unit_heater.year_built = form.year_built.data
           unit_heater.input_capacity = form.input_capacity.data
           unit_heater.output_capacity = form.output_capacity.data 
           unit_heater.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = unit_heater.manufacturer   
            form.model_number.data = unit_heater.model_number
            form.serial_number.data = unit_heater.serial_number 
            form.year_built.data = unit_heater.year_built
            form.input_capacity.data = unit_heater.input_capacity   
            form.output_capacity.data = unit_heater.output_capacity
            form.heating_eff.data = unit_heater.effciency 
        return render_template('add_hvac_equipment.html', add='unit_heater',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_unit_heater/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteunitheater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        unit_heatern = UnitHeater.query.get_or_404(id)
        area = unit_heatern.area_id
        db.session.delete(unit_heatern)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicateunitheater/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateunitheater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        unitheater_id = id
        unitheater = UnitHeater.query.get(id)
        form = UnitHeaterForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            unit_heater = UnitHeater(building_id = unitheater.building,photo=unitheater.photo, manufacturer=unitheater.manufacturer,model_number=unitheater.model_number,serial_number=unitheater.serial_number,year_built=unitheater.year_built,input_capacity=unitheater.input_capacity,output_capacity=unitheater.output_capacity,effciency=unitheater.heating_eff,supply_air_temp=unitheater.supply_air_temp,area=unitheater.area)
            db.session.add(unit_heater)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = unitheater.area_id))
    else:
        abort(403)

@commercial.route("/add_gas_fired_heating_coil/<int:id>", methods=['GET', 'POST'])
@login_required
def add_gas_fired_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = GasFiredHeatingCoilForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            efficiency = request.form['heating_eff']
            coil_photo = request.files.get('coil_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(coil_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            gas_fired_heating_coil = GasFiredHeatingCoil(building_id = building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=efficiency,area_id=id)
            try:
                db.session.add(gas_fired_heating_coil)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding gas fired heating coil"
        else:
            return render_template('add_hvac_equipment.html', add='gas_fired_heating_coil',area=area,form=form)
    else:
        abort(403)

@commercial.route("/add_gas_fired_heating_coil/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_gas_fired_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        gas_fired_heating_coil = GasFiredHeatingCoil.query.get_or_404(id)
        area = gas_fired_heating_coil.area_id
        form = GasFiredHeatingCoilForm()
        if form.validate_on_submit():
           gas_fired_heating_coil.manufacturer = form.manufacturer.data
           gas_fired_heating_coil.model_number = form.model_number.data
           gas_fired_heating_coil.serial_number = form.serial_number.data 
           gas_fired_heating_coil.year_built = form.year_built.data
           gas_fired_heating_coil.input_capacity = form.input_capacity.data
           gas_fired_heating_coil.output_capacity = form.output_capacity.data 
           gas_fired_heating_coil.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = gas_fired_heating_coil.manufacturer   
            form.model_number.data = gas_fired_heating_coil.model_number
            form.serial_number.data = gas_fired_heating_coil.serial_number 
            form.year_built.data = gas_fired_heating_coil.year_built
            form.input_capacity.data = gas_fired_heating_coil.input_capacity   
            form.output_capacity.data = gas_fired_heating_coil.output_capacity
            form.heating_eff.data = gas_fired_heating_coil.effciency 
        return render_template('add_hvac_equipment.html', add='gas_fired_heating_coil',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_gas_fired_heating_coil/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletegasfiredheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        gas_fired_heating_coil = GasFiredHeatingCoil.query.get_or_404(id)
        area = gas_fired_heating_coil.area_id
        db.session.delete(gas_fired_heating_coil)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicategasfiredheatingcoil/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicategasfiredheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        gasfiredheatingcoil_id = id
        gasfiredheatingcoil = GasFiredHeatingCoil.query.get(id)
        form = GasFiredHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            gas_fired_heating_coil = GasFiredHeatingCoil(building_id = gasfiredheatingcoil.building,photo=gasfiredheatingcoil.photo, manufacturer=gasfiredheatingcoil.manufacturer,model_number=gasfiredheatingcoil.model_number,serial_number=gasfiredheatingcoil.serial_number,year_built=gasfiredheatingcoil.year_built,input_capacity=gasfiredheatingcoil.input_capacity,output_capacity=gasfiredheatingcoil.output_capacity,effciency=gasfiredheatingcoil.efficiency,area=gasfiredheatingcoil.area)
            db.session.add(gas_fired_heating_coil)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = gasfiredheatingcoil.area_id))
    else:
        abort(403)

@commercial.route("/add_heat_pump/<int:id>", methods=['GET', 'POST'])
@login_required
def add_heat_pump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = HeatPumpForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            fuel_type = request.form['fuel_type']
            heat_photo = request.files.get('heat_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(heat_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            heat_pump = HeatPump(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,fuel_type=fuel_type,area_id=id)
            db.session.add(heat_pump)
            db.session.commit()
            area_id = id
            return redirect('/commercial/hvac_index/'+str(id))

        else:
            return render_template('add_hvac_equipment.html', add='heat_pump',area=area,form=form)
    else:
        abort(403)
@commercial.route("/add_heat_pump/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_heat_pump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        heat_pump = HeatPump.query.get_or_404(id)
        area = heat_pump.area_id
        form = HeatPumpForm()
        if form.validate_on_submit():
           heat_pump.manufacturer = form.manufacturer.data
           heat_pump.model_number = form.model_number.data
           heat_pump.serial_number = form.serial_number.data 
           heat_pump.year_built = form.year_built.data
           heat_pump.fuel_type = form.fuel_type.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = heat_pump.manufacturer   
            form.model_number.data = heat_pump.model_number
            form.serial_number.data = heat_pump.serial_number 
            form.year_built.data = heat_pump.year_built
            form.fuel_type.data = heat_pump.fuel_type
        return render_template('add_hvac_equipment.html', add='heat_pump',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_heat_pump/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteheatpump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        heat_pump = HeatPump.query.get_or_404(id)
        area = heat_pump.area_id
        db.session.delete(heat_pump)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicateheatpump/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateheatpump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        heatpump_id = id
        heatpump = HeatPumpForm.query.get(id)
        form = GasFiredHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            heat_pump = HeatPump(building=heatpump.building_id,photo=heatpump.photo, manufacturer=heatpump.manufacturer,model_number=heatpump.model_number,serial_number=heatpump.serial_number,year_built=heatpump.year_built,fuel_type=heatpump.fuel_type,area=heatpump.area)
            db.session.add(heat_pump)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = heatpump.area_id))
    else:
        abort(403)

@commercial.route("/add_electric_rest_heating_coil/<int:id>", methods=['GET', 'POST'])
@login_required
def addelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = ElectricRestHeatingCoilForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            efficiency = request.form['heating_eff']
            coil_photo = request.files.get('coil_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(coil_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            electric_rest_heating_coil = ElectricRestHeatingCoil(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=efficiency,area_id=id)
            try:
                db.session.add(electric_rest_heating_coil)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding electric rest heating coil"
        else:
            return render_template('add_hvac_equipment.html', add='electric_rest_heating_coil',area=area, form=form)
    else:
        abort(403)

@commercial.route("/add_electric_rest_heating_coil/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_electric_rest_heating_coil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        electric_rest_heating_coil = ElectricRestHeatingCoil.query.get_or_404(id)
        area = electric_rest_heating_coil.area_id
        form = ElectricRestHeatingCoilForm()
        if form.validate_on_submit():
           electric_rest_heating_coil.manufacturer = form.manufacturer.data
           electric_rest_heating_coil.model_number = form.model_number.data
           electric_rest_heating_coil.serial_number = form.serial_number.data 
           electric_rest_heating_coil.year_built = form.year_built.data
           electric_rest_heating_coil.input_capacity = form.input_capacity.data
           electric_rest_heating_coil.output_capacity = form.output_capacity.data 
           electric_rest_heating_coil.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = electric_rest_heating_coil.manufacturer   
            form.model_number.data = electric_rest_heating_coil.model_number
            form.serial_number.data = electric_rest_heating_coil.serial_number 
            form.year_built.data = electric_rest_heating_coil.year_built
            form.input_capacity.data = electric_rest_heating_coil.input_capacity   
            form.output_capacity.data = electric_rest_heating_coil.output_capacity
            form.heating_eff.data = electric_rest_heating_coil.effciency 
        return render_template('add_hvac_equipment.html', add='electric_rest_heating_coil',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_electric_rest_heating_coil/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        electric_rest_heating_coil = ElectricRestHeatingCoil.query.get_or_404(id)
        area = electric_rest_heating_coil.area_id
        db.session.delete(electric_rest_heating_coil)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicateelectricrestheatingcoil/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateelectricrestheatingcoil(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        electricrestheatingcoil_id = id
        electricrestheatingcoil = ElectricRestHeatingCoil.query.get(id)
        form = ElectricRestHeatingCoilForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            electric_rest_heating_coil = ElectricRestHeatingCoil(building=electricrestheatingcoil.building_id,photo=electricrestheatingcoil.photo, manufacturer=electricrestheatingcoil.manufacturer,model_number=electricrestheatingcoil.model_number,serial_number=electricrestheatingcoil.serial_number,year_built=electricrestheatingcoil.year_built,input_capacity=electricrestheatingcoil.input_capacity,output_capacity=electricrestheatingcoil.output_capacity,effciency=electricrestheatingcoil.efficiency,area=electricrestheatingcoil.area)
            db.session.add(electric_rest_heating_coil)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = electricrestheatingcoil.area_id))
    else:
        abort(403)



@commercial.route("/add_infrared_heater/<int:id>", methods=['GET', 'POST'])
@login_required
def add_infrared_heater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = InfraredHeaterForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            input_capacity = request.form["input_capacity"]
            output_capacity = request.form["output_capacity"]
            heating_eff = request.form['heating_eff']
            infrared_photo = request.files.get('infrared_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(infrared_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            infrared_heater = InfraredHeater(building_id = building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,input_capacity=input_capacity,output_capacity=output_capacity,effciency=heating_eff,area_id=id)
            try:
                db.session.add(infrared_heater)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding infrared_heater"
        else:
            return render_template('add_hvac_equipment.html', add='infrared_heater',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_infrared_heater/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_infrared_heater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        infrared_heater = InfraredHeater.query.get_or_404(id)
        area = infrared_heater.area_id
        form = InfraredHeaterForm()
        if form.validate_on_submit():
           infrared_heater.manufacturer = form.manufacturer.data
           infrared_heater.model_number = form.model_number.data
           infrared_heater.serial_number = form.serial_number.data 
           infrared_heater.year_built = form.year_built.data
           infrared_heater.input_capacity = form.input_capacity.data
           infrared_heater.output_capacity = form.output_capacity.data 
           infrared_heater.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = infrared_heater.manufacturer   
            form.model_number.data = infrared_heater.model_number
            form.serial_number.data = infrared_heater.serial_number 
            form.year_built.data = infrared_heater.year_built
            form.input_capacity.data = infrared_heater.input_capacity   
            form.output_capacity.data = infrared_heater.output_capacity
            form.heating_eff.data = infrared_heater.effciency 
        return render_template('add_hvac_equipment.html', add='infrared_heater',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_infrared_heater/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteinfraredheater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        infrared_heater = InfraredHeater.query.get_or_404(id)
        area = infrared_heater.area_id
        db.session.delete(infrared_heater)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)


@commercial.route('/duplicateinfraredheater/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateinfraredheater(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        infraredheater_id = id
        infraredheater = InfraredHeater.query.get(id)
        form = InfraredHeaterForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            infrared_heater = InfraredHeater(building_id = infraredheater.building_id,photo=infraredheater.photo, manufacturer=infraredheater.manufacturer,model_number=infraredheater.model_number,serial_number=infraredheater.serial_number,year_built=infraredheater.year_built,input_capacity=infraredheater.input_capacity,output_capacity=infraredheater.output_capacity,effciency=infraredheater.heating_eff,area=infraredheater.area)
            db.session.add(infrared_heater)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = infraredheater.area_id))
    else:
        abort(403)
@commercial.route("/add_make_up_air_unit/<int:id>", methods=['GET', 'POST'])
@login_required
def add_make_up_air_unit(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = MakeUpAirUnitForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            cooling_capacity = request.form["cooling_capacity"]
            cooling_coil_type = request.form["cooling_coil_type"]
            compressor_type = request.form["compressor_type"]
            heating_capacity = request.form["heating_capacity"]
            heating_coil_type = request.form["heating_coil_type"]
            heating_eff = request.form['heating_eff']
            make_up_air_unit = MakeUpAirUnit(building_id=building,photo=photo, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity,cooling_coil_type=cooling_coil_type,heating_capacity=heating_capacity,heating_coil_type=heating_coil_type,effciency=heating_eff,area=area)
            try:
                db.session.add(make_up_air_unit)
                db.session.commit()
                area_id = id
                return redirect('/hvac_index/'+str(id))
            except:
                return "There was an error adding make up air unit"
        else:
            return render_template('add_hvac_equipment.html', add='make_up_air_unit',area=area, form=form)
    else:
        abort(403)

@commercial.route("/add_make_up_air_unit/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_make_up_air_unit(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        make_up_air_unit = MakeUpAirUnit.query.get_or_404(id)
        area = make_up_air_unit.area_id
        form = MakeUpAirUnitForm()
        if form.validate_on_submit():
           make_up_air_unit.manufacturer = form.manufacturer.data
           make_up_air_unit.model_number = form.model_number.data
           make_up_air_unit.serial_number = form.serial_number.data 
           make_up_air_unit.year_built = form.year_built.data
           make_up_air_unit.cooling_capacity = form.cooling_capacity.data
           make_up_air_unit.cooling_coil_type = form.cooling_coil_type.data
           make_up_air_unit.heating_capacity = form.heating_capacity.data
           make_up_air_unit.heating_coil_type = form.heating_coil_type.data
           make_up_air_unit.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = make_up_air_unit.manufacturer   
            form.model_number.data = make_up_air_unit.model_number
            form.serial_number.data = make_up_air_unit.serial_number 
            form.year_built.data = make_up_air_unit.year_built
            form.cooling_capacity.data = make_up_air_unit.cooling_capacity
            form.cooling_coil_type.data = make_up_air_unit.cooling_coil_type 
            form.heating_capacity.data = make_up_air_unit.heating_capacity
            form.heating_coil_type.data = make_up_air_unit.heating_coil_type
            form.heating_eff.data = make_up_air_unit.effciency 
        return render_template('add_hvac_equipment.html', add='make_up_air_unit',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_make_up_air_unit/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletemakeupairunit(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        make_up_air_unit = MakeUpAirUnit.query.get_or_404(id)
        area = make_up_air_unit.area_id
        db.session.delete(make_up_air_unit)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicatemakeupairunit/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatemakeupairunit(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        makeupairunit_id = id
        makeupairunit = MakeUpAirUnit.query.get(id)
        form = MakeUpAirUnitForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            make_up_air_unit = InfraredHeater(building_id = makeupairunit.building_id,photo=makeupairunit.photo, manufacturer=makeupairunit.manufacturer,model_number=makeupairunit.model_number,serial_number=makeupairunit.serial_number,year_built=makeupairunit.year_built,input_capacity=makeupairunit.input_capacity,output_capacity=makeupairunit.output_capacity,effciency=makeupairunit.heating_eff,area=makeupairunit.area)
            db.session.add(make_up_air_unit)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = makeupairunit.area_id))
    else:
        abort(403)

@commercial.route("/add_packaged_rtu/<int:id>", methods=['GET', 'POST'])
@login_required
def add_packaged_rtu(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = PackagedRTUForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            heating_capacity = request.form["heating_capacity"]
            heating_coil_type = request.form["heating_coil_type"]
            heating_eff = request.form['heating_eff']
            packaged_photo = request.files.get('packaged_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(packaged_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            packaged_rtu = PackagedRTU(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity,compressor_type=compressor_type,refridgerant=refridgerant,kwton=kwton,eer=eer,heating_capacity=heating_capacity,heating_coil_type=heating_coil_type,effciency=heating_eff,area_id=id)
            try:
                db.session.add(packaged_rtu)
                db.session.commit()
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding make up air unit"
        else:
            return render_template('add_hvac_equipment.html', add='packaged_rtu',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_packaged_rtu/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_packaged_rtu(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packaged_rtu = PackagedRTU.query.get_or_404(id)
        area = packaged_rtu.area_id
        form = PackagedRTUForm()
        if form.validate_on_submit():
           packaged_rtu.manufacturer = form.manufacturer.data
           packaged_rtu.model_number = form.model_number.data
           packaged_rtu.serial_number = form.serial_number.data 
           packaged_rtu.year_built = form.year_built.data
           packaged_rtu.compressor_type = form.compressor_type.data
           packaged_rtu.cooling_capacity = form.cooling_capacity.data
           packaged_rtu.refridgerant = form.refridgerant.data
           packaged_rtu.kwton = form.kwton.data
           packaged_rtu.eer = form.eer.data
           packaged_rtu.heating_capacity = form.heating_capacity.data
           packaged_rtu.heating_coil_type = form.heating_coil_type.data
           packaged_rtu.effciency = form.heating_eff.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = packaged_rtu.manufacturer   
            form.model_number.data = packaged_rtu.model_number
            form.serial_number.data = packaged_rtu.serial_number 
            form.year_built.data = packaged_rtu.year_built
            form.cooling_capacity.data = packaged_rtu.cooling_capacity
            form.compressor_type.data = packaged_rtu.compressor_type 
            form.refridgerant.data = packaged_rtu.refridgerant
            form.kwton.data = packaged_rtu.kwton
            form.eer.data = packaged_rtu.eer
            form.heating_capacity.data = packaged_rtu.heating_capacity
            form.heating_coil_type.data = packaged_rtu.heating_coil_type
            form.heating_eff.data = packaged_rtu.effciency 
        return render_template('add_hvac_equipment.html', add='packaged_rtu',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_packaged_rtu/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletepackagedrtu(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packaged_rtu = PackagedRTU.query.get_or_404(id)
        area = packaged_rtu.area_id
        db.session.delete(packaged_rtu)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@commercial.route('/duplicatepackagedrtu/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepackagedrtu(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packagedrtu_id = id
        packagedrtu = PackagedRTU.query.get(id)
        form = PackagedRTUForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            packaged_rtu = PackagedRTU(building_id = packagedrtu.building_id,photo=packagedrtu.photo, manufacturer=packagedrtu.manufacturer,model_number=packagedrtu.model_number,serial_number=packagedrtu.serial_number,year_built=packagedrtu.year_built,input_capacity=packagedrtu.input_capacity,output_capacity=packagedrtu.output_capacity,effciency=packagedrtu.heating_eff,area=packagedrtu.area)
            db.session.add(packaged_rtu)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = packagedrtu.area_id))
    else:
        abort(403)

@commercial.route("/add_chiller/<int:id>", methods=['GET', 'POST'])
@login_required
def add_chiller(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = ChillerForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            cooling_capacity = request.form["cooling_capacity"]
            compressor_type = request.form['compressor_type']
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            type_chiller = request.form["chiller_type"]
            chiller_photo = request.files.get('chiller_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(chiller_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            chiller = Chiller(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,cooling_capacity=cooling_capacity, compressor_type=compressor_type,refridgerant=refridgerant,kwton=kwton,eer=eer,type_chiller=type_chiller,area_id=id)
            db.session.add(chiller)
            db.session.commit()
            area_id = id
            return redirect('/commercial/hvac_index/'+str(id))
        else:
            return render_template('add_hvac_equipment.html', add='chiller',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_chiller/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_chiller(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        chiller = Chiller.query.get_or_404(id)
        area = chiller.area_id
        form = ChillerForm()
        if form.validate_on_submit():
           chiller.manufacturer = form.manufacturer.data
           chiller.model_number = form.model_number.data
           chiller.serial_number = form.serial_number.data 
           chiller.year_built = form.year_built.data
           chiller.compressor_type = form.compressor_type.data
           chiller.cooling_capacity = form.cooling_capacity.data
           chiller.refridgerant = form.refridgerant.data
           chiller.kwton = form.kwton.data
           chiller.eer = form.eer.data
           chiller.type_chiller = form.chiller_type.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = chiller.manufacturer   
            form.model_number.data = chiller.model_number
            form.serial_number.data = chiller.serial_number 
            form.year_built.data = chiller.year_built
            form.cooling_capacity.data = chiller.cooling_capacity
            form.compressor_type.data = chiller.compressor_type 
            form.refridgerant.data = chiller.refridgerant
            form.kwton.data = chiller.kwton
            form.eer.data = chiller.eer
            form.chiller_type.data = chiller.type_chiller
        return render_template('add_hvac_equipment.html', add='chiller',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_chiller/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletechiller(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        chiller = Chiller.query.get_or_404(id)
        area = chiller.area_id
        db.session.delete(chiller)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicatechiller/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatechiller(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        chiller_id = id
        chiller = Chiller.query.get(id)
        form = ChillerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_chiller = PackagedRTU(building_id = chiller.building_id,photo=chiller.photo, manufacturer=chiller.manufacturer,model_number=chiller.model_number,serial_number=chiller.serial_number,year_built=chiller.year_built,input_capacity=chiller.input_capacity,output_capacity=chiller.output_capacity,effciency=chiller.heating_eff,area=chiller.area)
            db.session.add(new_chiller)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = chiller.area_id))
    else:
        abort(403)
@commercial.route("/add_mini_split_system/<int:id>", methods=['GET', 'POST'])
@login_required
def add_mini_split_system(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = MiniSplitSystemForm()


        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            type_chiller = request.form["chiller_type"]
            mini_photo = request.files.get('mini_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(mini_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            mini_split_system = MiniSplitSystem(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,
                        year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area_id=id)
            try:
                db.session.add(mini_split_system)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+ str(id))
            except:
                return "There was an error adding mini split system"
        else:
            return render_template('add_hvac_equipment.html', add='mini_split_system',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_mini_split_system/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_mini_split_system(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        mini_split_system = MiniSplitSystem.query.get_or_404(id)
        area = mini_split_system.area_id
        form = MiniSplitSystemForm()
        if form.validate_on_submit():
           mini_split_system.manufacturer = form.manufacturer.data
           mini_split_system.model_number = form.model_number.data
           mini_split_system.serial_number = form.serial_number.data 
           mini_split_system.year_built = form.year_built.data
           mini_split_system.compressor_type = form.compressor_type.data
           mini_split_system.cooling_capacity = form.cooling_capacity.data
           mini_split_system.refridgerant = form.refridgerant.data
           mini_split_system.kwton = form.kwton.data
           mini_split_system.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = mini_split_system.manufacturer   
            form.model_number.data = mini_split_system.model_number
            form.serial_number.data = mini_split_system.serial_number 
            form.year_built.data = mini_split_system.year_built
            form.cooling_capacity.data = mini_split_system.cooling_capacity
            form.compressor_type.data = mini_split_system.compressor_type 
            form.refridgerant.data = mini_split_system.refridgerant
            form.kwton.data = mini_split_system.kwton
            form.eer.data = mini_split_system.eer
        return render_template('add_hvac_equipment.html', add='mini_split_system',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_mini_split_system/<int:id>/delete', methods=['Get','POST'])
@login_required
def deleteminisplitsystem(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        mini_split_system = MiniSplitSystem.query.get_or_404(id)
        area = mini_split_system.area_id
        db.session.delete(mini_split_system)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicateminisplitsystem/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicateminisplitsystem(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        minisplitsystem_id = id
        minisplitsystem = MiniSplitSystem.query.get(id)
        form = MiniSplitSystemForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            mini_split_system = MiniSplitSystem(building_id = minisplitsystem.building_id,photo=minisplitsystem.photo, manufacturer=minisplitsystem.manufacturer,model_number=minisplitsystem.model_number,serial_number=minisplitsystem.serial_number,year_built=minisplitsystem.year_built,input_capacity=minisplitsystem.input_capacity,output_capacity=minisplitsystem.output_capacity,effciency=minisplitsystem.heating_eff,area=minisplitsystem.area)
            db.session.add(mini_split_system)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = minisplitsystem.area_id))
    else:
        abort(403)
@commercial.route("/add_packaged_terminal_ac/<int:id>", methods=['GET', 'POST'])
@login_required
def add_packaged_terminal_ac(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = PackagedTerminalACForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            terminal_photo = request.files.get('terminal_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(terminal_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            packaged_terminal_ac = PackagedTerminalAC(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,
                        year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area_id=id)
            db.session.add(packaged_terminal_ac)
            db.session.commit()
            area_id = id
            return redirect('/commercial/hvac_index/'+str(id))

        else:
            return render_template('add_hvac_equipment.html', add='packaged_terminal_ac',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_packaged_terminal_ac/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_packaged_terminal_ac(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packaged_terminal_ac = PackagedTerminalAC.query.get_or_404(id)
        area = packaged_terminal_ac.area_id
        form = PackagedTerminalACForm()
        if form.validate_on_submit():
           packaged_terminal_ac.manufacturer = form.manufacturer.data
           packaged_terminal_ac.model_number = form.model_number.data
           packaged_terminal_ac.serial_number = form.serial_number.data 
           packaged_terminal_ac.year_built = form.year_built.data
           packaged_terminal_ac.compressor_type = form.compressor_type.data
           packaged_terminal_ac.cooling_capacity = form.cooling_capacity.data
           packaged_terminal_ac.refridgerant = form.refridgerant.data
           packaged_terminal_ac.kwton = form.kwton.data
           packaged_terminal_ac.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = packaged_terminal_ac.manufacturer   
            form.model_number.data = packaged_terminal_ac.model_number
            form.serial_number.data = packaged_terminal_ac.serial_number 
            form.year_built.data = packaged_terminal_ac.year_built
            form.cooling_capacity.data = packaged_terminal_ac.cooling_capacity
            form.compressor_type.data = packaged_terminal_ac.compressor_type 
            form.refridgerant.data = packaged_terminal_ac.refridgerant
            form.kwton.data = packaged_terminal_ac.kwton
            form.eer.data = packaged_terminal_ac.eer
        return render_template('add_hvac_equipment.html', add='packaged_terminal_ac',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_packaged_terminal_ac/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletepackagedterminalac(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packaged_terminal_ac = PackagedTerminalAC.query.get_or_404(id)
        area = packaged_terminal_ac.area_id
        db.session.delete(packaged_terminal_ac)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)
@commercial.route('/duplicatepackagedterminalac/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepackagedterminalac(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        packagedterminalac_id = id
        packagedterminalac = PackagedTerminalAC.query.get(id)
        form = PackagedTerminalACForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            packaged_terminal_ac = PackagedTerminalAC(building_id = packagedterminalac.building_id,photo=packagedterminalac.photo, manufacturer=packagedterminalac.manufacturer,model_number=packagedterminalac.model_number,serial_number=packagedterminalac.serial_number,year_built=packagedterminalac.year_built,input_capacity=packagedterminalac.input_capacity,output_capacity=packagedterminalac.output_capacity,effciency=packagedterminalac.heating_eff,area=packagedterminalac.area)
            db.session.add(packaged_terminal_ac)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = packagedterminalac.area_id))
    else:
        abort(403)

@commercial.route("/add_condensing_unit_system/<int:id>", methods=['GET', 'POST'])
@login_required
def add_condensing_unit_system(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = CondensingUnitSystemForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form["compressor_type"]
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            unit_photo = request.files.get('unit_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(unit_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            condensing_unit_system= CondensingUnitSystem(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,
                        serial_number=serial_number,year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,
                        kwton=kwton,eer=eer,area_id=id)
            try:
                db.session.add(condensing_unit_system)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error condesnsingu unit system"
        else:
            return render_template('add_hvac_equipment.html', add='condensing_unit_system',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_condensing_unit_system/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_condensing_unit_system(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        condensing_unit_system = CondensingUnitSystem.query.get_or_404(id)
        area = condensing_unit_system.area_id
        form = CondensingUnitSystemForm()
        if form.validate_on_submit():
           condensing_unit_system.manufacturer = form.manufacturer.data
           condensing_unit_system.model_number = form.model_number.data
           condensing_unit_system.serial_number = form.serial_number.data 
           condensing_unit_system.year_built = form.year_built.data
           condensing_unit_system.compressor_type = form.compressor_type.data
           condensing_unit_system.cooling_capacity = form.cooling_capacity.data
           condensing_unit_system.refridgerant = form.refridgerant.data
           condensing_unit_system.kwton = form.kwton.data
           condensing_unit_system.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = condensing_unit_system.manufacturer   
            form.model_number.data = condensing_unit_system.model_number
            form.serial_number.data = condensing_unit_system.serial_number 
            form.year_built.data = condensing_unit_system.year_built
            form.cooling_capacity.data = condensing_unit_system.cooling_capacity
            form.compressor_type.data = condensing_unit_system.compressor_type 
            form.refridgerant.data = condensing_unit_system.refridgerant
            form.kwton.data = condensing_unit_system.kwton
            form.eer.data = condensing_unit_system.eer
        return render_template('add_hvac_equipment.html', add='condensing_unit_system',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_condensing_unit_system/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletecondensingunitsystem(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        condensing_unit_system = CondensingUnitSystem.query.get_or_404(id)
        area = condensing_unit_system.area_id
        db.session.delete(condensing_unit_system)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@commercial.route('/duplicatecondensingunitsystem/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatecondensingunitsystem(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        condensingunitsystem_id = id
        condensingunitsystem = CondensingUnitSystem.query.get(id)
        form = CondensingUnitSystemForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            condensing_unit_system = CondensingUnitSystem(building_id = condensingunitsystem.building_id,photo=condensingunitsystem.photo, manufacturer=condensingunitsystem.manufacturer,model_number=condensingunitsystem.model_number,serial_number=condensingunitsystem.serial_number,year_built=condensingunitsystem.year_built,input_capacity=condensingunitsystem.input_capacity,output_capacity=condensingunitsystem.output_capacity,effciency=condensingunitsystem.heating_eff,area=condensingunitsystem.area)
            db.session.add(condensing_unit_system)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = condensingunitsystem.area_id))
    else:
        abort(403)


@commercial.route("/add_window_air_conditioner/<int:id>", methods=['GET', 'POST'])
@login_required
def add_window_air_conditioner(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = WindowAirConditionerForm()

        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            compressor_type = request.form['compressor_type']
            cooling_capacity = request.form["cooling_capacity"]
            refridgerant = request.form["refridgerant"]
            kwton = request.form["kwton"]
            eer = request.form["eer"]
            window_photo = request.files.get('window_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(window_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            window_air_conditioner = WindowAirConditioner(building_id=building,photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,compressor_type=compressor_type,cooling_capacity=cooling_capacity,refridgerant=refridgerant,kwton=kwton,eer=eer,area_id=id)
            try:
                db.session.add(window_air_conditioner)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding window air conditioner"
        else:
            return render_template('add_hvac_equipment.html', add='window_air_conditioner',area=area, form=form)
    else:
        abort(403)

@commercial.route("/add_window_air_conditioner/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_window_air_conditioner(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        window_air_conditioner = WindowAirConditioner.query.get_or_404(id)
        area = window_air_conditioner.area_id
        form = WindowAirConditionerForm()
        if form.validate_on_submit():
           window_air_conditioner.manufacturer = form.manufacturer.data
           window_air_conditioner.model_number = form.model_number.data
           window_air_conditioner.serial_number = form.serial_number.data 
           window_air_conditioner.year_built = form.year_built.data
           window_air_conditioner.compressor_type = form.compressor_type.data
           window_air_conditioner.cooling_capacity = form.cooling_capacity.data
           window_air_conditioner.refridgerant = form.refridgerant.data
           window_air_conditioner.kwton = form.kwton.data
           window_air_conditioner.eer = form.eer.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = window_air_conditioner.manufacturer   
            form.model_number.data = window_air_conditioner.model_number
            form.serial_number.data = window_air_conditioner.serial_number 
            form.year_built.data = window_air_conditioner.year_built
            form.cooling_capacity.data = window_air_conditioner.cooling_capacity
            form.compressor_type.data = window_air_conditioner.compressor_type 
            form.refridgerant.data = window_air_conditioner.refridgerant
            form.kwton.data = window_air_conditioner.kwton
            form.eer.data = window_air_conditioner.eer
        return render_template('add_hvac_equipment.html', add='window_air_conditioner',area=area,form=form)
    else:
        abort(403)

@commercial.route('/add_window_air_conditioner/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletewindowairconditioner(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        window_air_conditioner = WindowAirConditioner.query.get_or_404(id)
        area = window_air_conditioner.area_id
        db.session.delete(window_air_conditioner)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)


@commercial.route('/duplicatewindowairconditioner/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatewindowairconditioner(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        windowairconditioner_id = id
        windowairconditioner = WindowAirConditioner.query.get(id)
        form = WindowAirConditionerForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            window_air_conditioner = WindowAirConditioner(building_id = windowairconditioner.building_id,photo=windowairconditioner.photo, manufacturer=windowairconditioner.manufacturer,model_number=windowairconditioner.model_number,serial_number=windowairconditioner.serial_number,year_built=windowairconditioner.year_built,input_capacity=windowairconditioner.input_capacity,output_capacity=windowairconditioner.output_capacity,effciency=windowairconditioner.heating_eff,area=windowairconditioner.area)
            db.session.add(window_air_conditioner)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = windowairconditioner.area_id))
    else:
        abort(403)



@commercial.route("/add_motor/<int:id>", methods=['GET', 'POST'])
@login_required
def add_motor(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = MotorForm()
        if request.method == 'POST':
            manufacturer = request.form["manufacturer"]
            model_number = request.form["model_number"]
            serial_number = request.form["serial_number"]
            year_built = request.form["year_built"]
            condition = request.form["condition"]
            horsepower = request.form["horsepower"]
            rpm = request.form["rpm"]
            effciency = request.form["effciency"]
            volts = request.form['volts']
            bhp = request.form["bhp"]
            frame = request.form["frame"]
            fla = request.form["fla"]
            cfm = request.form["cfm"]
            phase = request.form["phase"]
            motor_photo = request.files.get('motor_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(motor_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            motor =  Motor(photo_id=file_name, manufacturer=manufacturer,model_number=model_number,serial_number=serial_number,year_built=year_built,
                            condition=condition,horsepower=horsepower,rpm=rpm,effciency=effciency,volts=volts,bhp=bhp,
                            frame=frame,fla=fla,cfm=cfm,phase=phase,area_id=id,building_id = building)
            db.session.add(motor)
            db.session.commit()
            area_id = id
            return redirect('/commercial/hvac_index/'+str(id))

        else:
            return render_template('add_hvac_equipment.html', add='motor',area=area, form=form)
    else:
        abort(403)


@commercial.route('/duplicatemotor/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatemotor(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        motor_id = id
        motor = Motor.query.get(id)
        form = MotorForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_motor = Motor(building_id = motor.building_id,photo=motor.photo, manufacturer=motor.manufacturer,model_number=motor.model_number,serial_number=motor.serial_number,year_built=motor.year_built,input_capacity=motor.input_capacity,output_capacity=motor.output_capacity,effciency=motor.heating_eff,area=motor.area)
            db.session.add(new_motor)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = motor.area_id))
    else:
        abort(403)


@commercial.route("/add_motor/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_motor(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        motor = Motor.query.get_or_404(id)
        area = motor.area_id
        form = MotorForm()
        if form.validate_on_submit():
           motor.manufacturer = form.manufacturer.data
           motor.model_number = form.model_number.data
           motor.serial_number = form.serial_number.data 
           motor.year_built = form.year_built.data
           motor.condition = form.condition.data
           motor.horsepower = form.horsepower.data
           motor.rpm = form.rpm.data
           motor.effciency = form.effciency.data
           motor.volts = form.volts.data
           motor.bhp = form.bhp.data
           motor.frame = form.frame.data
           motor.fla = form.fla.data
           motor.cfm = form.cfm.data
           motor.phase = form.phase.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.manufacturer.data = motor.manufacturer   
            form.model_number.data = motor.model_number
            form.serial_number.data = motor.serial_number 
            form.year_built.data = motor.year_built
            form.condition.data =  motor.condition
            form.horsepower.data = motor.horsepower
            form.rpm.data = motor.rpm
            form.effciency.data = motor.effciency
            form.volts.data = motor.volts
            form.bhp.data = motor.bhp
            form.frame.data = motor.frame
            form.fla.data = motor.fla
            form.cfm.data = motor.cfm
            form.phase.data = motor.phase
        return render_template('add_hvac_equipment.html', add='motor',area=area,form=form)
    else:
        abort(403)


@commercial.route('/add_motor/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletemotor(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        motor = Motor.query.get_or_404(id)
        area = motor.area_id
        db.session.delete(motor)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)



@commercial.route("/add_pump/<int:id>", methods=['GET', 'POST'])
@login_required
def add_pump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        area = Area.query.get(id)
        building = area.building_id
        form = PumpForm()

        if request.method == 'POST':
            condition = request.form['condition']
            head = request.form["head"]
            gpm = request.form["gpm"]
            pump_photo = request.files.get('pump_photo', None)
            target = os.path.join(app_root, 'static/appliance_photos/img')
            file_name = save_picture_appliance(pump_photo,'appliance_photos/img/')
            destination = '/'.join([target, file_name])
            pump =  Pump(photo_id=file_name, condition=condition,head=head,gpm=gpm,area_id=id,building_id = building)
            try:
                db.session.add(pump)
                db.session.commit()
                area_id = id
                return redirect('/commercial/hvac_index/'+str(id))
            except:
                return "There was an error adding pump"

        else:
            return render_template('add_hvac_equipment.html', add='pump',area=area, form=form)
    else:
        abort(403)
@commercial.route("/add_pump/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_pump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        pump = Pump.query.get_or_404(id)
        area = pump.area_id
        form = PumpForm()
        if form.validate_on_submit():
           pump.condition = form.condition.data
           pump.head = form.head.data
           pump.gpm = form.gpm.data
           db.session.commit()
           return redirect(url_for('commercial.hvac',area = area, id = area))

        elif request.method == 'GET':
            form.condition.data =  pump.condition
            form.head.data = pump.head
            form.gpm.data = pump.gpm
        return render_template('add_hvac_equipment.html', add='pump',area=area,form=form)
    else:
        abort(403)



@commercial.route('/add_pump/<int:id>/delete', methods=['Get','POST'])
@login_required
def deletepump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        pump = Pump.query.get_or_404(id)
        area = pump.area_id
        db.session.delete(pump)
        db.session.commit()
        return redirect(url_for('commercial.hvac',area = area, id = area))
    else:
        abort(403)

@commercial.route('/duplicatepump/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicatepump(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        pump_id = id
        pump = Pump.query.get(id)
        form = PumpForm()
        loop = 0
        duplicateammount = request.form.get('duplicateammount', type=int)
        if duplicateammount is None :
            duplicateammount = 1

        while loop < duplicateammount:

            new_pump = Pump(building_id = pump.building_id,photo=pump.photo, manufacturer=pump.manufacturer,model_number=pump.model_number,serial_number=pump.serial_number,year_built=pump.year_built,input_capacity=pump.input_capacity,output_capacity=pump.output_capacity,effciency=pump.heating_eff,area=pump.area)
            db.session.add(new_pump)
            db.session.commit()
            loop += 1

        return redirect(url_for('commercial.equipmentindex', id = pump.area_id))
    else:
        abort(403)

# photo uploading










# Validation lsits


@commercial.route("/ValidationLists")
@login_required
def Validation_Lists():
    if(current_user.is_authenticated and current_user.is_admin()):

        Building_Types = pd.read_excel("Validation_Lists\Building_Types.xlsx")

        Door_R_Valeus = pd.read_excel(
            "Validation_Lists\Door_R_Values.xlsx")

        Exterior_Wall_R_Values = pd.read_excel(
            "Validation_Lists\Exterior_Wall_R_Values.xlsx")

        Glass_SHGC = pd.read_excel(
            "Validation_Lists\Glass_SHGC.xlsx")

        Insulation_K_Values = pd.read_excel(
            "Validation_Lists\Insulation_K_Value.xlsx")

        Interior_Wall_R_Values = pd.read_excel(
            "Validation_Lists\Interior_Wall_R_Values.xlsx")

        Roof_Finish_R_Values = pd.read_excel(
            "Validation_Lists\Roof_Finish_R_Values.xlsx")

        Roof_R_Values = pd.read_excel(
            "Validation_Lists\Roof_R_Values.xlsx")

        Window_R_Values = pd.read_excel(
            "Validation_Lists\Window_R_Values.xlsx")
    else:
        abort(403)


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)





@commercial.route("/gen/<int:id>", methods=['GET', 'POST'])
@login_required
def gen_docx(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        building_id = building.id
        client_id = building.client_id
        client = Client.query.get(client_id)
              #lights_query = Light.query.filter_by(building_id=building_id).with_entities(Light.area_id, Light.hours, Light.fixture_count,
         #           Light.fixture, Light.lamp, Light.wattage).all()


        template = 'Template_6.docx'
        client_name = client.company
        facility_address = building.address
        building_name = building.name
        building_squarefootage = building.square_footage

        light_fields = ['area_id','hours','fixture_count','fixture','lamp','wattage']
        lights_query = Light.query.filter_by(building_id=building_id).all()
        lights = json.dumps(lights_query, cls=AlchemyEncoder)
        light2 = json.loads(lights)

        dhw_fields = ['building_id', 'equipment_type', 'area_id', 'tag','quantity', 'manufacturer', 'model_number', 'serial_number', 'year_built', 'input_capacity', 'fuel_type', 'storage_volume', 'effciency', 'set_point','insulation_value','notes']
        dhw_query = CommercialDHW.query.filter_by(building_id=building_id).all()
        dhw = json.dumps(dhw_query,cls=AlchemyEncoder)
        dhw2 = json.loads(dhw)

        pump_fields = ['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','gpm','fuel_type','pressure','horsepower','rpm','volts','effciency']
        pump_query = Pump.query.filter_by(building_id = building_id).all()
        pump = json.dumps(pump_query,cls=AlchemyEncoder)
        pump2 = json.loads(pump)

        motor_fields =['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','horsepower','rpm','volts','cfm','effciency']
        motor_query = Motor.query.filter_by(building_id = building_id).all()
        motor = json.dumps(motor_query,cls=AlchemyEncoder)
        motor2 = json.loads(motor)

        steam_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        steam_boiler_query = Steam_Boiler.query.filter_by(building_id = building_id).all()
        steam_boiler = json.dumps(steam_boiler_query,cls=AlchemyEncoder)
        steam_boiler2 = json.loads(steam_boiler)

        hydronic_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        hydronic_boiler_query = Hydronic_Boiler.query.filter_by(building_id = building_id).all()
        hydronic_boiler = json.dumps(hydronic_boiler_query,cls=AlchemyEncoder)
        hydronic_boiler2 = json.loads(hydronic_boiler)

        furnace_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        furnace_query = Furnace.query.filter_by(building_id = building_id).all()
        furnace = json.dumps(furnace_query,cls=AlchemyEncoder)
        furnace2 = json.loads(furnace)

        unit_heater_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        unit_heater_query = UnitHeater.query.filter_by(building_id = building_id).all()
        unit_heater = json.dumps(unit_heater_query,cls=AlchemyEncoder)
        unit_heater2 = json.loads(unit_heater)

        gas_fired_heating_coil_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        gas_fired_heating_coil_query = GasFiredHeatingCoil.query.filter_by(building_id = building_id).all()
        gas_fired_heating_coil = json.dumps(gas_fired_heating_coil_query,cls=AlchemyEncoder)
        gas_fired_heating_coil2 = json.loads(gas_fired_heating_coil)

        heat_pump_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        heat_pump_query = HeatPump.query.filter_by(building_id = building_id).all()
        heat_pump = json.dumps(heat_pump_query,cls=AlchemyEncoder)
        heat_pump2 = json.loads(heat_pump)

        electric_rest_heating_coil_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        electric_rest_heating_coil_query = ElectricRestHeatingCoil.query.filter_by(building_id = building_id).all()
        electric_rest_heating_coil = json.dumps(electric_rest_heating_coil_query,cls=AlchemyEncoder)
        electric_rest_heating_coil2 = json.loads(electric_rest_heating_coil)

        infrared_heater_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        infrared_heater_query = InfraredHeater.query.filter_by(building_id = building_id).all()
        infrared_heater = json.dumps(infrared_heater_query,cls=AlchemyEncoder)
        infrared_heater2 = json.loads(infrared_heater)

        make_up_air_unit_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        make_up_air_unit_query = MakeUpAirUnit.query.filter_by(building_id = building_id).all()
        make_up_air_unit = json.dumps(make_up_air_unit_query,cls=AlchemyEncoder)
        make_up_air_unit2 = json.loads(make_up_air_unit)

        packaged_rtu_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        packaged_rtu_query = PackagedRTU.query.filter_by(building_id = building_id).all()
        packaged_rtu = json.dumps(packaged_rtu_query,cls=AlchemyEncoder)
        packaged_rtu2 = json.loads(packaged_rtu)

        chiller_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        chiller_query = Chiller.query.filter_by(building_id = building_id).all()
        chiller = json.dumps(chiller_query,cls=AlchemyEncoder)
        chiller2 = json.loads(chiller)

        mini_split_system_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        mini_split_system_query = MiniSplitSystem.query.filter_by(building_id = building_id).all()
        mini_split_system = json.dumps(mini_split_system_query,cls=AlchemyEncoder)
        mini_split_system2 = json.loads(mini_split_system)

        packaged_terminal_ac_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        packaged_terminal_ac_query = PackagedTerminalAC.query.filter_by(building_id = building_id).all()
        packaged_terminal_ac = json.dumps(packaged_terminal_ac_query,cls=AlchemyEncoder)
        packaged_terminal_ac2 = json.loads(packaged_terminal_ac)

        condensing_unit_system_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        condensing_unit_system_query = CondensingUnitSystem.query.filter_by(building_id = building_id).all()
        condensing_unit_system = json.dumps(condensing_unit_system_query,cls=AlchemyEncoder)
        condensing_unit_system2 = json.loads(condensing_unit_system)

        window_air_conditioner_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        window_air_conditioner_query = WindowAirConditioner.query.filter_by(building_id = building_id).all()
        window_air_conditioner = json.dumps(window_air_conditioner_query,cls=AlchemyEncoder)
        window_air_conditioner2 = json.loads(window_air_conditioner)


        #photo_fields = ['steam_boiler_photos','hydronic_boiler_photos','pump_photos','motor_photos','chiller_photos','furnace_photos','heatpump_photos','pipe_photos','ahu_photos','gasfiredheatingcoil_photos','electricrestheatingcoil_photos','windowairconditioner_photos','infraredheater_photo',
        #                'makeupairunit_photos','minisplitsystem_photos','condensingunitsystem_photos','pakagedrtu_photos','packagedterminalac_photos','selfcontainedahu_photos','unitheater_photos','unitventilator_photos','dhw_photos','appliance_photos','building_photos','light_photos']
        #photo_query = Photo.query.filter_by(building_id = building_id),all()
        #photo = json.dumps(photo_query,cls=AlchemyEncoder)
        #photo2 = json.loads(photo)

        target_file = BytesIO()
        template = DocxTemplate("Template_5.docx")
        context = {
            'client_name': client_name,
            'facility_address': facility_address,
            'building_name': building_name,
            'building_squarefootage': building_squarefootage,
            'light_contents': light2,
            'dhw_contents' : dhw2,
            'pump_contents' : pump2,
            'motor_contents' : motor2,
            'hvac_contents' : steam_boiler2,
            ##'hvac_contents' : hydronic_boiler2,
            ##'hvac_contents' : furnace2,
            ##'hvac_contents' : unit_heater2,
            ##'hvac_contents' : gas_fired_heating_coil2,
            ##'hvac_contents' : heat_pump2,
            ##'hvac_contents' : electric_rest_heating_coil2,
            ##'hvac_contents' : infrared_heater2,
            ##'hvac_contents' : make_up_air_unit2,
            ##'hvac_contents' : packaged_rtu2,
            ##'hvac_contents' : chiller2,
            ##'hvac_contents' : mini_split_system2,
            ##'hvac_contents' : packaged_terminal_ac2,
            ##'hvac_contents' : condensing_unit_system2,
            ##'hvac_contents' : window_air_conditioner2
            #'photo_contents' : photo2

        }  # gets the context used to render the document


        target_file = BytesIO()
        template.render(context)
        template.save(target_file)


        document = target_file
        document.seek(0)


        return send_file(
            document, mimetype='application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.document', as_attachment=True,
            attachment_filename='invoice.docx')
    else:
        abort(403)






@commercial.route("/test/<int:id>", methods=['GET', 'POST'])
@login_required
def test(id):
    if(current_user.is_authenticated and current_user.is_admin()):
        building = Building.query.get(id)
        building_id = building.id
        client_id=building.client_id
        client = Client.query.get(client_id)
        dhw_fields = ['equipment_type', 'area_id', 'tag', 'manufacturer', 'model_number', 'serial_number', 'year_built', 'input_capacity', 'fuel_type', 'storage_volume', 'effciency']
        light_fields = ['area_id','hours','fixture_count','fixture','lamp','wattage']
        #lights_query = Light.query.filter_by(building_id=building_id).with_entities(Light.area_id, Light.hours, Light.fixture_count, Light.fixture, Light.lamp, Light.wattage).all()
        lights_query = Light.query.filter_by(building_id=building_id).all()
        dhw_query = DHW.query.filter_by(building_id=building_id).all()
        dhw = json.dumps(dhw_query,cls=AlchemyEncoder)
        dhw2 = json.loads(dhw)
        lights = json.dumps(lights_query, cls=AlchemyEncoder)
        light2 = json.loads(lights)

        pump_fields = ['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','gpm','fuel_type','pressure','horsepower','rpm','volts','effciency']
        pump_query = Pump.query.filter_by(building_id = building_id).all()
        pump = json.dumps(pump_query,cls=AlchemyEncoder)
        pump2 = json.loads(pump)

        motor_fields =['building_id','area_id','tag','manufacturer','model_number','serial_number','year_built','horsepower','rpm','volts','cfm','effciency']
        motor_query = Motor.query.filter_by(building_id = building_id).all()
        motor = json.dumps(motor_query,cls=AlchemyEncoder)
        motor2 = json.loads(motor)
        
        steam_boiler_fields = ['equipment_type','area_id','tag','manufacturer','model_number','serial_number','year_built','cooling_capacity','heating_capacity','fuel_type','heating_eff','notes']
        steam_boiler_query = Steam_Boiler.query.filter_by(building_id = building_id).all()
        steam_boiler = json.dumps(steam_boiler_query,cls=AlchemyEncoder)
        steam_boiler2 = json.loads(steam_boiler)


        return str(light2 + dhw2 + motor2 + pump2 + steam_boiler2)
    else:
        abort(403)
if __name__ == "__main__":
    app.debug = True
    app.run()





class ApplianceForm(FlaskForm):
    appliance_type = SelectField('Type', choices=[('Air Conditioner','Air Conditioner'), 
                 ('Air Ionizser','Air Ionizser'),
                 ('Appliance Plug', 'Appliance Plug'), 
                 ('Aroma Lamp', 'Aroma Lamp'), 
                 ('Attic Fan', 'Attic Fan'),
                 ('Bachelor Griller', 'Bachelor Griller'), 
                 ('Bedside Lamp', 'Bedside Lamp'),
                 ('Back Boiler', 'Back Boiler'), 
                 ('Beverage Opener', 'Beverage Opener'), 
                 ('Blender', 'Blender'),('Box fan','Box fan'),
                 ('Box mangle','Box mangle'),
                 ('Calculator','Calculator'),
                 ('Camcorder','Camcorder'),
                 ('Can opener','Can opener'),
                 ('Cassette player','Cassette player'),
                 ('Ceiling fan','Ceiling fan'),
                 ('Central vacuum cleaner','Central vacuum cleaner'),
                 ('Clock','Clock'),
                 ('Grandfather clock','Grandfather clock'),
                 ('Wall clock','Wall clock'),
                 ('Clothes dryer','Clothes dryer'),
                 ('Clothes iron','Clothes iron'),
                 ('Coffee grinder','Coffee grinder'),
                 ('Coffeemaker','Coffeemaker'),
                 ('Coffee percolator','Coffee percolator'),
                 ('Cold-pressed juicer','Cold-pressed juicer'),
                 ('Cooler','Cooler'),
                 ('Combo washer dryer','Combo washer dryer'),
                 ('Computer','Computer'),
                 ('Modem','Modem'),
                 ('Mouse (computer)','Mouse (computer)'),
                 ('Printer','Printer'),
                 ('Keyboard','Keyboard'),
                 ('Server','Server'),
                 ('Convection oven','Convection oven'),
                 ('Deep fryer','Deep fryer'),
                 ('Dehumidifier','Dehumidifier'),
                 ('Digital camera','Digital camera'),
                 ('Dish drying cabinet','Dish drying cabinet'),
                 ('Dishwasher','Dishwasher'),
                 ('Drawer dishwasher','Drawer dishwasher'),
                 ('DVD player','DVD player'),
                 ('Edger','Edger'),
                 ('Electric cooker','Electric cooker'),
                 ('Electric razor','Electric razor'),
                 ('Electric toothbrush','Electric toothbrush'),
                 ('Electric water boiler','Electric water boiler'),
                 ('Evaporative cooler','Evaporative cooler'),
                 ('Exhaust hood','Exhaust hood'),
                 ('Fan heater','Fan heater'),
                 ('Desk fan','Desk fan'),
                 ('Flame supervision device','Flame supervision device'),
                 ('Food processor','Food processor'),
                 ('Forced-air','Forced-air'),
                 ('Freezer','Freezer'),
                 ('Futon dryer','Futon dryer'),
                 ('Garbage disposal unit','Garbage disposal unit'),
                 ('Gas appliance','Gas appliance'),
                 ('Gramaphone','Gramaphone'),
                 ('Go-to-bed matchbox','Go-to-bed matchbox'),
                 ('Hair dryer','Hair dryer'),
                 ('Hair iron','Hair iron'),
                 ('Hearing aid','Hearing aid'),
                 ('Hob (hearth)','Hob (hearth)'),
                 ('Home server','Home server'),
                 ('Humidifier (Vaporizer)','Humidifier (Vaporizer)'),
                 ('HVAC','HVAC'),
                 ('Icebox','Icebox'),
                 ('Juicer','Juicer'),
                 ('Karaoke Set','Karaoke Set'),
                 ('Microphone','Microphone'),
                 ('Disco ball','Disco ball'),
                 ('Kimchi refrigerator','Kimchi refrigerator'),
                 ('Lawn mower','Lawn mower'),
                 ('Riding mower','Riding mower'),
                 ('Leaf blower','Leaf blower'),
                 ('Lighter','Lighter'),
                 ('Light fixture','Light fixture'),
                 ('Mangle','Mangle'),
                 ('Meat grinder','Meat grinder'),
                 ('Megaphone','Megaphone'),
                 ('Micathermic heater','Micathermic heater'),
                 ('Microwave oven','Microwave oven'),
                 ('Mixer','Mixer'),
                 ('Mogul lamp','Mogul lamp'),
                 ('Mousetrap','Mousetrap'),
                 ('Nightlight','Nightlight'),
                 ('Oil heater','Oil heater'),
                 ('Oven','Oven'),
                 ('Panini press','Panini press'),
                 ('Pasta maker','Pasta maker'),
                 ('Patio heater','Patio heater'),
                 ('Paper shredder','Paper shredder'),
                 ('Pencil sharpener','Pencil sharpener'),
                 ('Popcorn maker','Popcorn maker'),
                 ('Pressure-cooker','Pressure-cooker'),
                 ('Radiator (heating)','Radiator (heating)'),
                 ('Radio receiver','Radio receiver'),
                 ('Refrigerator','Refrigerator'),
                 ('Internet refrigerator','Internet refrigerator'),
                 ('Thermal mass refrigerator','Thermal mass refrigerator'),
                 ('Rotisserie','Rotisserie'),
                 ('Sewing machine','Sewing machine'),
                 ('Sink','Sink'),
                 ('Kitchen sink','Kitchen sink'),
                 ('Separate sink spray','Separate sink spray'),
                 ('Slow cooker','Slow cooker'),
                 ('Snowblower','Snowblower'),
                 ('Space heater','Space heater'),
                 ('Steam mop','Steam mop'),
                 ('Stereo','Stereo'),
                 ('Stove','Stove'),
                 ('Sump pump','Sump pump'),
                 ('Telephone','Telephone'),
                 ('Digital Phone','Digital Phone'),
                 ('Table lamp','Table lamp'),
                 ('Television set','Television set'),
                 ('Remote','Remote'),
                 ('Speaker','Speaker'),
                 ('Tie press','Tie press'),
                 ('Toaster','Toaster'),
                 ('Toaster oven','Toaster oven'),
                 ('Trash compactor','Trash compactor'),
                 ('Trouser press','Trouser press'),
                 ('Vacuum cleaner','Vacuum cleaner'),
                 ('Manual vacuum cleaner','Manual vacuum cleaner'),
                 ('Robotic vacuum cleaner','Robotic vacuum cleaner'),
                 ('Videocassette recorder','Videocassette recorder'),
                 ('Waffle iron','Waffle iron'),
                 ('Washing machine','Washing machine'),
                 ('Water cooker','Water cooker'),
                 ('Waterpik','Waterpik'),
                 ('Water purifier','Water purifier'),
                 ('Water heater','Water heater'),
                 ('Solar water heater','Solar water heater'),
                 ('Tankless water heater','Tankless water heater'),
                 ('Weed Eater','Weed Eater'),
                 ('Window fan','Window fan'),
                 ('Air fryer','Air fryer'),
                 ('Barbecue grill','Barbecue grill'),
                 ('Beehive oven','Beehive oven'),
                 ('Brasero (heater)','Brasero (heater)'),
                 ('Brazier','Brazier'),
                 ('Bread machine','Bread machine'),
                 ('Burjiko','Burjiko'),
                 ('Butane torch','Butane torch'),
                 ('Chapati maker','Chapati maker'),
                 ('Cheesemelter','Cheesemelter'),
                 ('Chocolatera','Chocolatera'),
                 ('Chorkor oven','Chorkor oven'),
                 ('Clome oven','Clome oven'),
                 ('Comal (cookware)','Comal (cookware)'),
                 ('Combi steamer','Combi steamer'),
                 ('Communal oven','Communal oven'),
                 ('Convection microwave','Convection microwave'),
                 ('Corn roaster','Corn roaster'),
                 ('Crepe maker','Crepe maker'),
                 ('Earth oven','Earth oven'),
                 ('Energy regulator','Energy regulator'),
                 ('Espresso machine','Espresso machine'),
                 ('Field kitchen','Field kitchen'),
                 ('Fire pot','Fire pot'),
                 ('Flattop grill','Flattop grill'),
                 ('Food steamer','Food steamer'),
                 ('Fufu Machine','Fufu Machine'),
                 ('Halogen oven','Halogen oven'),
                 ('Haybox','Haybox'),
                 ('Horno','Horno'),
                 ('Hot box (appliance)','Hot box (appliance)'),
                 ('Hot plate','Hot plate'),
                 ('Instant Pot','Instant Pot'),
                 ('Kamado','Kamado'),
                 ('Kettle','Kettle'),
                 ('Kitchener range','Kitchener range'),
                 ('Kujiejun','Kujiejun'),
                 ('Kyoto box','Kyoto box'),
                 ('Makiyakinabe','Makiyakinabe'),
                 ('Masonry oven','Masonry oven'),
                 ('Mess kit','Mess kit'),
                 ('Multicooker','Multicooker'),
                 ('Pancake machine','Pancake machine'),
                 ('Panini sandwich grill','Panini sandwich grill'),
                 ('Pressure cooker','Pressure cooker'),
                 ('Pressure fryer','Pressure fryer'),
                 ('Reflector oven','Reflector oven'),
                 ('Remoska','Remoska'),
                 ('Rice cooker','Rice cooker'),
                 ('Rice polisher','Rice polisher'),
                 ('Roasting jack','Roasting jack'),
                 ('Rocket mass heater','Rocket mass heater'),
                 ('Rotimatic','Rotimatic'),
                 ('Russian oven','Russian oven'),
                 ('Sabbath mode','Sabbath mode'),
                 ('Salamander broiler','Salamander broiler'),
                 ('Samovar','Samovar'),
                 ('Sandwich toaster','Sandwich toaster'),
                 ('Self-cleaning oven','Self-cleaning oven'),
                 ('Shichirin','Shichirin'),
                 ('Solar cooker','Solar cooker'),
                 ('Sous-vide cooker','Sous-vide cooker'),
                 ('Soy milk maker','Soy milk maker'),
                 ('Susceptor','Susceptor'),
                 ('Tabun oven','Tabun oven'),
                 ('Tandoor','Tandoor'),
                 ('Tangia','Tangia'),
                 ('Thermal immersion circulator','Thermal immersion circulator'),
                 ('Toaster and toaster ovens','Toaster and toaster ovens'),
                 ('Turkey fryer','Turkey fryer'),
                 ('Vacuum fryer','Vacuum fryer'),
                 ('Wet grinder','Wet grinder'),
                 ('Wood-fired oven','Wood-fired oven')])
    quantity = StringField('Quantity')
    wattage = StringField('Wattage')
    submit = SubmitField('Upload')
    submitButton = SubmitField('Add')

class LightForm(FlaskForm):
     fixtures = StringField('Number of Fixtures')
     hours = StringField('Hours')
     fixture_type = SelectField('Fixtures Type', choices=[('troffer', 'Troffer'),('linear', 'Linear'),('potlight','Potlight'),('polelight','Polelight'),('highbay','Highbay'),('wallpack','Wallpack')])
     lamp_type = SelectField('Lamp Type', choices=[('t8','T8'),('t5','T5'),('t12','T12'),('tubeled','Tubeled'),('led','LED'),('metalhalide','Metal Halide'),('highpressuresodium','High Pressure Sodium'),('cfl','CFL')])
     wattage = StringField('Lamp Wattage')
     lamps_per_fixture = StringField('Lamps Per Fixture')
     lamp_count = StringField('Number of Lamps')
class AreaForm(FlaskForm):
    name = StringField("Name")

class SteamBoilerForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')
        boiler_type = StringField('Boiler Type')
        pressure = StringField('Pressure')     

class FurnaceForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')

class HydronicBoilerForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')
        boiler_type = StringField('Boiler Type')
        lhwt = StringField('LHWT')
        ehwt = StringField('EHWT')

class UnitHeaterForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')
        supply_air_temp = StringField("Supply Air Setpoint")

class GasFiredHeatingCoilForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')

class HeatPumpForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        fuel_type = StringField("Fuel Type")

class ElectricRestHeatingCoilForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')

class InfraredHeaterForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        input_capacity = StringField('Input Capacity')
        output_capacity = StringField('Output Capacity')
        heating_eff = StringField('Heating eff')

class MakeUpAirUnitForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        cooling_capacity = StringField("Cooling Capacity")
        cooling_coil_type = StringField("Cooling Coil Type")
        compressor_type = StringField("Compressor Type")
        heating_capacity = StringField("Heating Capacity")
        heating_coil_type = StringField("Heating Coil Type")
        heating_eff = StringField('Heating eff')

class PackagedRTUForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")
        heating_capacity = StringField("Heating Capacity")
        heating_coil_type = StringField("Heating Coil Type")
        heating_eff = StringField('Heating eff')

class ChillerForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")
        chiller_type = StringField("Chiller Type")


class MiniSplitSystemForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")

class PackagedTerminalACForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")

class WindowAirConditionerForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")

class CondensingUnitSystemForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        compressor_type = StringField("Compressor Type")
        cooling_capacity = StringField("Cooling Capacity")
        refridgerant = StringField("Refridgerant")
        kwton = StringField("KW/Ton")
        eer = StringField("EER")

class MotorForm(FlaskForm):
        manufacturer = StringField('Manufacturer')
        model_number = StringField('Model Number')
        serial_number = StringField('Serial Number')
        year_built = StringField('Year Built')
        condition = StringField("Condition")
        horsepower = StringField("Horsepower")
        rpm = StringField("RPM")
        effciency = StringField("Effciency")
        volts = StringField("Volts")
        bhp = StringField("BHP")
        frame = StringField("Frame")
        fla = StringField("FLA")
        cfm = StringField("CFM")
        phase = StringField("Phase")

class PumpForm(FlaskForm):
        condition = StringField("Condition")
        head = StringField("Head")
        gpm = StringField("GPM")

class BuildingForm(FlaskForm):
        building_name = StringField("Building Name")
        address = StringField("Address")
        city = StringField("City")
        province = StringField("Province")
        postal_code = StringField("Postal Code")
        square_footage = StringField("Square Footage")

class DHWForm(FlaskForm):
    equipment_type = SelectField("Equipment Type", choices = [('Storage Heater', 'Storage Heater'), ('Boiler','Boiler'),('Instantaneous','Instantaneous')])
    tag = StringField("Tag")
    manufacturer = StringField("Manufacturer")
    model_number = StringField("Model Number")
    serial_number = StringField("Serial Number")
    input_capacity = StringField("Input Capacity")
    fuel_type = SelectField("Fuel Type", choices = [('Natural Gas','Natural Gas'), ('Electricity', 'Electricity')])
    efficiency = StringField("Efficieny")
    storage_volume = StringField("Storage Volume")
    set_point = StringField("Set Point")

class ExteriorWallForm(FlaskForm):
    material = SelectField("Material", choices = [('Brick Veneer','Brick Veneer'),('Coated Steel','Coated Steel'),('Concrete Block','Concrete Block'),('Fiberglass','Fiberglass'),('Fiberglass Paneling','Fiberglass Paneling'),('Limestone Block','Limestone Block'),('Poured Concrete','Poured Concrete'),('Steel Paneling','Steel Paneling'),('Stone Aggregate','Stone Aggregate'),('Stucco','Stucco'),('Vinyl Paneling','Vinyl Paneling'),('Wood','Wood'),('Wood Paneling','Wood Paneling')])
    rvalue = SelectField("R Value", choices = [('1.20','1.20'),('0.61','0.61'),('1.28','1.28'),('2.00','2.00'),('1.00','1.00'),('0.96','0.96'),('1.28','1.28'),('0.61','0.61'),('1.00','1.00'),('0.12','0.12'),('1.80','1.80'),('2.80','2.80'),('2.80','2.80')])

class RoofForm(FlaskForm):
    material = SelectField("Material", choices = [('Brick Veneer','Brick Veneer'),('Concrete Block','Concrete Block'),('Fiberglass Paneling','Fiberglass Paneling'),('Poured Concrete','Poured Concrete'),('Steel Paneling','Steel Paneling'),('Stone Aggregate','Stone Aggregate'),('Stucco','Stucco'),('Vinyl Paneling','Vinyl Paneling'),('Wood Paneling','Wood Paneling')])
    rvalue = SelectField("R Value", choices = [('1.20','1.20'),('1.28','1.28'),('1.00','1.00'),('1.28','1.28'),('0.61','0.61'),('1.00','1.00'),('0.12','0.12'),('0.90','0.90'),('2.80','2.80')])

class RoofFinishForm(FlaskForm):
    material = SelectField("Material", choices = [('None','None'),('Asphalt Shingles','Asphalt Shingles'),('Bitumen','Bitumen'),('Clay Tiles','Clay Tiles'),('Concrete Tiles','Concrete Tiles'),('Fiberglass Paneling','Fiberglass Paneling'),('Gravel','Gravel'),('Green Roof','Green Roof'),('Grit','Grit'),('Mineral','Mineral'),('Rubber','Rubber'),('Rubber UV Reflector','Rubber UV Reflector'),('Spanish Tiles','Spanish Tiles'),('Steel Paneling','Steel Paneling')])
    rvalue = SelectField("R Value", choices = [('0.00','0.00'),('0.44','0.44'),('0.88','0.88'),('0.25','0.25'),('0.69','0.69'),('0.88','0.88'),('0.69','0.69'),('1.00','1.00'),('0.00','0.00'),('1.00','1.00'),('0.00','0.00'),('0.00','0.00'),('1.30','1.30'),('1.60','1.60'),('0.25','0.25'),('0.61','0.61')])

class FoundationForm(FlaskForm):
    foundation_type = SelectField("Foundation Type", choices = [('Slabs-On-Grade','Slabs-On-Grade'),('Raised Floor','Raised Floor'),('Basement','Basement')])
    material = SelectField("Material", choices = [('Concrete','Concrete'),('Brick','Brick'),('Wood','Wood'),('Steel','Steel'),('Stone','Stone')])
    rx = SelectField("RX", choices = [('2','2'),('0.5','0.5'),('1','1')])
    rvalue = SelectField('R Value', choices = [('1.28','1.28'),('1.2','1.2'),('2.8','2.8'),('0.61','0.61'),('1','1')])

class ClientForm(FlaskForm):
    company = StringField("Comapny")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")
    address = StringField("Address")
    postal_code = StringField("Postal Code")
    province = StringField("Province")

class HistoricalUsageForm(FlaskForm):
    date = StringField("Date")

class UtilityForm(FlaskForm):
    date = StringField("Date")
    file = FileField(validators=[FileRequired()])

class OperatingHoursForm(FlaskForm):
    month = StringField("Month")
    changed = StringField("Changed")
    newstart = IntegerField("NewStart")
    newend = IntegerField("NewEnd")
    datenumber = IntegerField("DateNumber")



class EnergyCalendarForm(FlaskForm):
    month = StringField("Month")
    year = StringField("Year")

 