import mysql.connector
import datetime

def calendar_pull(building_id,year, month):

    connection = mysql.connector.connect(
    host='db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com',
    user='admin',
    password='rvqb2JymBB5CaNn',
    db= 'db_mysql_sustainergy_alldata'
    )

    cursor = connection.cursor(buffered = True)

    if type(month) == str: 
        month_name = month.lower()

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

    insert_line = f"SELECT {month_name} FROM calendar WHERE building_id = {building_id} AND year = {year};"

    cursor.execute(insert_line)

    results = cursor.fetchall()
    results_list = results[0]

    cursor.close()

    return eval(results_list[0])