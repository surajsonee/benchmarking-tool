


# this function is used to connect and put data into the database 
import mysql.connector 


def report_to_db(date,serial_number,monthly_comp, report):

    connection = mysql.connector.connect(
        host='db-building-storage.cfo00s1jgsd6.us-east-2.rds.amazonaws.com',
        user='admin',
        password='rvqb2JymBB5CaNn',
        db= 'db_mysql_sustainergy_alldata'
        )

    cursor = connection.cursor(buffered = True)

    values =   (date,
                serial_number, 
                str(monthly_comp),
                str(report['channel_usage']),
                str(report['on_off_catagory']),
                str(report['channel_usage']),
                str(report['on_off_always']))

    insert_line = """INSERT INTO reporting 
                        (date,
                        serial_number,
                        monthly_comparison,
                        channel_usage,
                        on_off_category,
                        category_usage,
                        on_off_all)
                        VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s));"""


    print(type(values))
    cursor.execute(insert_line, values)

    connection.commit()

    cursor.close()

    return 
