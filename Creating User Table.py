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

    userTable = """CREATE TABLE IF NOT EXISTS login (
                                    id text PRIMARY KEY,
                                    password text NOT NULL
                                )"""
    
    choicesTable = """CREATE TABLE IF NOT EXISTS indexCombos (
                                    id text NOT NULL,
                                    courseCombo text NOT NULL,
                                    indexCombo text NOT NULL,
                                    PRIMARY KEY (id, indexCombo)
                                )"""
    
    if connection is not None:
        create_table(connection, userTable)
        create_table(connection, choicesTable)
    else:
        print("Error! Connot create Database connection!")
    
if __name__ == "__main__":
    main()