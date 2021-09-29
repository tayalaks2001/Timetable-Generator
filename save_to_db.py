from sqlite3 import connect

def save_to_db(userid, courses, indices):

    connection = connect(r"C:\Users\user\Desktop\Timetable Generator\database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT into indexCombos (id, courseCombo, indexCombo) VALUES (?, ?, ?)", (userid, " ".join(courses), " ".join(indices)))
    connection.commit()

    return