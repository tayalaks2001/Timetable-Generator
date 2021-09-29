import sqlite3.dump
from sqlite3 import connect, Error

# First, we define a function called create_connection() that connects to an SQLite database specified by the database file dbFile.
def create_connection(dbFile):

    connection = None

    # When you connect to an SQLite database file that does not exist, SQLite automatically creates the new database for you.
    try:
        # The connect() function opens a connection to an SQLite database. 
        # It returns a Connection object that represents the database. 
        # By using the Connection object, you can perform various database operations.
        connection = connect(dbFile) 
        print(sqlite3.version)

    except Error as e:
        print(e)

    finally:
        # It is a good programming practice that you should always close the database connection when you complete with it.
        if connection:
            connection.close()

if __name__ == "__main__":
    create_connection("/Users/akstayal/Desktop/Timetable Generator 2/database.db")