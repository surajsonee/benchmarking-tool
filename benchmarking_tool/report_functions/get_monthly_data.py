import mysql.connector 

def get_monthly_data(serial_number,month_num, year):
    
    connection = mysql.connector.connect(
    host='db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com',
    user='admin',
    password='rvqb2JymBB5CaNn',
    db= 'db_mysql_sustainergy_alldata'
    )
    


    '''
    connection = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='hello12345',
    db= 'sys'
    
    )
    '''

    cursor = connection.cursor(buffered = True)


    # this is what it should be but bacause we dont have building_ID in that table yet we need to use serial_number
    #building_id = "twstsklsadflkj"

    #cursor.execute(f"SELECT channel1_name,channel1_usage, channel1_schedule FROM emporia_data WHERE = emporia_building_id = {building_id}")


    # this is the function to get the data that will be used to create the reporting data 



    serial_num = '"' + serial_number + '"'
    
    month = month_num
    
    cursor.execute(f"""SELECT date, channel4_name,channel4_usage,channel4_schedule, 
                                    channel5_name,channel5_usage,channel5_schedule,
                                    channel6_name,channel6_usage,channel6_schedule,
                                    channel7_name,channel7_usage,channel7_schedule,
                                    channel8_name,channel8_usage,channel8_schedule,
                                    channel9_name,channel9_usage,channel9_schedule,
                                    channel10_name,channel10_usage,channel10_schedule,
                                    channel11_name,channel11_usage,channel11_schedule,
                                    channel12_name,channel12_usage,channel12_schedule,
                                    channel13_name,channel13_usage,channel13_schedule,
                                    channel14_name,channel14_usage,channel14_schedule,
                                    channel15_name,channel15_usage,channel15_schedule,
                                    channel16_name,channel16_usage,channel16_schedule,
                                    channel17_name,channel17_usage,channel17_schedule,
                                    channel18_name,channel18_usage,channel18_schedule,
                                    channel19_name,channel19_usage,channel19_schedule
                                    
                                    FROM emporia_data WHERE serial_number = {serial_num} AND MONTH(date) = {month} AND YEAR(date) = {year}""")


    #cursor.execute(f"SELECT serial_number FROM emporia_data")

    results = cursor.fetchall()

    return results