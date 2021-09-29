from sqlite3 import connect

def saved_timetables(userid):

    connection = connect(r"C:\Users\user\Desktop\Timetable Generator\database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT courseCombo, indexCombo FROM indexCombos where id=?", (userid,))
    result = cursor.fetchall()
    courselist=[]
    indiceslist=[]
    for courses, indices in result:
        courselist.append(list(courses.split()))
        temp=[]
        idxsplit = list(map(int, indices.split()))
        for i in range(len(courselist[-1])):
            temp.append([courselist[-1][i],[idxsplit[i]]])
        indiceslist.append(temp)
    return courselist,indiceslist