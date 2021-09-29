from sqlite3 import connect

def checkExists(id_):

    connection = connect(r"C:\Users\user\Desktop\Timetable Generator\database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM login WHERE id=?", (id_,))
    result = cursor.fetchall()

    if result:
        return True
    else:
        return False

def addToDB(id_, password):

    connection = connect(r"C:\Users\user\Desktop\Timetable Generator\database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO login (id, password) VALUES (?, ?)", [id_, password])
    connection.commit()

    return