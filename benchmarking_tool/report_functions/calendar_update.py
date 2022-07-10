
# this function will take in a calandar that has been updated and then change it out in the database 
import mysql.connector
import datetime

def calendar_update(building_id, year, new_calendar):

    connection = mysql.connector.connect(
    host='db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com',
    user='admin',
    password='rvqb2JymBB5CaNn',
    db= 'db_mysql_sustainergy_alldata'
    )

    cursor = connection.cursor(buffered = True)

    #find the month the calendar is to replace 

    date = new_calendar[0]['day']

    month = date.month

    if month == 1:
        month_name = 'january'
    elif month == 2:
        month_name = 'february'
    elif month == 3:
        month_name = 'march'
    elif month == 4:
        month_name = 'april'
    elif month == 5:
        month_name = 'may'
    elif month == 6:
        month_name = 'june'
    elif month == 7:
        month_name = 'july'
    elif month == 8:
        month_name = 'august'
    elif month == 9:
        month_name = 'september'
    elif month == 10:
        month_name = 'october'
    elif month == 11:
        month_name = 'november'
    elif month == 12:
        month_name = 'december'

    insert_line = "UPDATE calendar SET " + month_name + " = (%s) WHERE building_id = (%s) AND year = (%s);"

    values = (str(new_calendar), building_id, year)

    cursor.execute(insert_line, values)

    connection.commit()

    cursor.close()

    return