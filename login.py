from sqlite3 import connect

def exists(id_, password):

    connection = connect("Timetable Generator\database.db")
    cursor = connection.cursor()
    cursor.execute("select * from login where id=? and password=?", (id_, password,))
    result = cursor.fetchall()
    print(result)
    if result:
        return True
    else:
        return False