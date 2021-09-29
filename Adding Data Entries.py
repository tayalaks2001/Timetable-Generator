import pandas as pd 
import sqlite3
from sqlite3 import connect, Error
import os

def create_connection(databasePath):

    connection = None
    try:
        connection = connect(databasePath)
    except Error as e:
        print(e)
    return connection

def addRows(connection, course, row):

    sqlCode = "INSERT INTO {} (id, type, lesson_group, day, time, venue, remark) VALUES (?,?,?,?,?,?,?)".format(course,)
    cursor = connection.cursor()
    cursor.execute(sqlCode, row)
    connection.commit()
    return cursor.lastrowid

def main():

    databasePath = "Timetable Generator\database.db"
    connection = create_connection(databasePath)
    with connection:
        timetablesPath = "Timetable Generator\Courses Timetables Pre-processed"
        for course in os.listdir(timetablesPath):
            df = pd.read_csv(os.path.join(timetablesPath, course))
            for rowNum in range(df.shape[0]):
                row = list(df.iloc[rowNum].apply(lambda x: str(x)))
                rowID = addRows(connection, course[:-4], row)

    return 
    
if __name__ == "__main__":
    main()