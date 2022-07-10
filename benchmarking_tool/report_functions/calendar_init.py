# to init the calandar to the database for a full year 
import mysql.connector
import datetime
from .operating_hours import operating_hours

def calendar_init(building_id, year, days_per_week, start_hour, end_hour):
    connection = mysql.connector.connect(
    host='db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com',
    user='admin',
    password='rvqb2JymBB5CaNn',
    db= 'db_mysql_sustainergy_alldata'
    )

    cursor = connection.cursor(buffered = True)
    insert_line_check = f"SELECT {year} FROM calendar WHERE building_id = {building_id};"
    cursor.execute(insert_line_check)
    results = cursor.fetchall()

    # if there are no results then the list is not there for that year but if there is results then close and do not overwrite
    if results != []:
        cursor.close()
        return
    # need to init every month and make it a values list 
    month_list = (str(building_id), str(year), str(days_per_week), str(start_hour), str(end_hour))
    for month in range(12): 
        month_calendar = operating_hours(datetime.date(year,month + 1,1), days_per_week, start_hour, end_hour)
        month_list += (str(month_calendar),)



    #values = tuple(month_list)
    

    insert_line = """INSERT INTO calendar 
                        (building_id,
                        year,
                        occupied_days_per_week,
                        ave_start_hour,
                        ave_end_hour,
                        january,
                        february,
                        march,
                        april,
                        may,
                        june,
                        july,
                        august,
                        september,
                        october,
                        november,
                        december)
                        VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s));"""

    try:
        cursor.execute(insert_line, month_list)
    except:
        print("building has already been initiated")
        cursor.close()
        return

    connection.commit()

    cursor.close()

    return 
