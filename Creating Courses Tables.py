import sqlite3
from sqlite3 import Error, connect
import os

def create_connection(databasePath):

    connection = None
    try:
        connection = connect(databasePath)
    except Error as e:
        print(e)
    
    return connection

def create_table(connection, sqlCode):

    try:
        cursor = connection.cursor()
        cursor.execute(sqlCode)
    except Error as e:
        print(e)

def main():

    databasePath = "Timetable Generator\database.db"
    connection = create_connection(databasePath)

    for course in os.listdir("Timetable Generator\Courses Timetables Original"):

        sqlCode = """CREATE TABLE IF NOT EXISTS {tab} (
                                        id text NOT NULL,
                                        type text,
                                        lesson_group text,
                                        day text,
                                        time text,
                                        venue text,
                                        remark text,
                                        PRIMARY KEY (id, day, time)
                                    );""".format(tab=course[:-4])

        if connection is not None:
            create_table(connection, sqlCode)
        else:
            print("Error! Connot create Database connection!")

if __name__ == "__main__":
    main()