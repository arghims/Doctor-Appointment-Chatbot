import mysql.connector


def DataUpdate(task, PERSON, time, time2):
    mydb = mysql.connector.connect(
        host="localhost",
        user="himanshi",
        password="Adi1290*",
        database="Appointments"
    )
    mycursor = mydb.cursor(buffered=True)
    if task == 'check':
        mycursor.execute('select 1 from Credentials where Appointmentdate = "{}" limit 1;'.format(time))
        if mycursor.fetchone():
            print("yes")
    elif task == "delete":
        print("DELETE from Credentials WHERE PatientName = '{}';".format(PERSON))
        sql = "DELETE from Credentials WHERE PatientName = '{}';".format(PERSON)
        mycursor.execute(sql)
    else:
        mycursor.execute('select 1 from Credentials where Appointmentdate = "{}" limit 1;'.format(time))
        if mycursor.fetchone():
            print("Appointment slot already booked")
        else:
            sql = 'INSERT INTO Credentials(PatientName, Appointmentdate, time)VALUES("{0}","{1}","{2}");'.format(PERSON, time, time2)
            mycursor.execute(sql)
            print("Appointment booked")

    mydb.commit()

if __name__=="__main__":
   DataUpdate('check', None, '07:00PM, Wednesday Jul 22, 2020', None)
