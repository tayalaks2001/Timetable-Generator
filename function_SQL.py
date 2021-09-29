import os
import sys
from itertools import combinations
from random import choice
import sqlite3

allIndices, validIndices, numIndices = {}, {}, {}
allCoursesPath = "Timetable Generator\database.db"

def main(courses, indicesChoices):

    global allIndices, validIndices, numIndices 
    connection = sqlite3.connect(allCoursesPath)
    cursor = connection.cursor()
    indicesChoices = {course:indices for [course, indices] in indicesChoices}   
        
    # IMPORTING RELEVANT SCHEDULES

    for course in courses:

        cursor.execute("Select distinct id from {}".format(course,))
        result = cursor.fetchall()
        allIndices[course] = list(map(lambda x: int(x[0]), result))
    
        validIndices[course] = []
        if indicesChoices[course]:
            for indexChoice in indicesChoices[course]:
                if indexChoice in allIndices[course]:
                    validIndices[course].append(indexChoice)
                else:
                    print("Index", indexChoice, "not found for course", course, end="!\n") 
        else:
            validIndices[course] = allIndices[course].copy()

    numIndices[course] = len(allIndices[course])

    # PREPARING A LIST OF LECTURE TIMINGS FOR ALL COURSES

    lectureTimings = []
    for course in courses:

        cursor.execute("SELECT day, time, remark FROM {} where id={} and type='Lec/Studio'".format(course, validIndices[course][0],))
        lectureRows = cursor.fetchall()

        for row in lectureRows:
            day, time, remark = row
            lectureTimings.append([course, int(day), list(map(int, time.split())), list(map(int, remark.split()))])

    # CHECKING CLASHES WHERE AT LEAST ONE OF THE LESSONS IS A LECTURE

    lecturesClashing = []
    for lecture in lectureTimings:

        courseLecture, dayLecture, [startTimeLecture, endTimeLecture], weekLecture = lecture
        for courseLesson in courses:
            
            if courseLecture!=courseLesson:

                cursor.execute("SELECT * FROM {}".format(courseLesson,))
                lessonTable = cursor.fetchall()
                for row in lessonTable:

                    indexLesson, typeLesson, groupLesson, dayLesson, timeLesson, venueLesson, weekLesson = row
                    if int(indexLesson) in validIndices[courseLesson] and dayLecture==int(dayLesson) and len(set(weekLecture).intersection(list(map(int, weekLesson.split()))))>0:

                        startTimeLesson, endTimeLesson = list(map(int, timeLesson.split()))
                        if not (endTimeLecture<=startTimeLesson or endTimeLesson<=startTimeLecture):

                            if typeLesson=="Lec/Studio":
                                if [courseLesson, courseLecture] not in lecturesClashing and [courseLecture, courseLesson] not in lecturesClashing:
                                    lecturesClashing.append([courseLecture, courseLesson])
                            else:
                                validIndices[courseLesson].remove(int(indexLesson))

    if lecturesClashing:
        for lectures in lecturesClashing:
            print("Lectures", lectures[0], "and", lectures[1], "are clashing!")
        sys.exit()

    connection.close()
    return validIndices

def check_non_lecture_clashes(courses, validIndices):

    global allIndices, numIndices
    connection = sqlite3.connect("Timetable Generator\database.db")
    cursor = connection.cursor()

    while True:

        allLessons, indicesCombo = [], []
        for course in courses:
            index = choice(validIndices[course])
            indicesCombo.append(index)
            cursor.execute("SELECT * FROM {} WHERE id={} and type!='Lec/Studio'".format(course,index,))
            result = cursor.fetchall()
            for row in result:
                indexLesson, typeLesson, groupLesson, dayLesson, timeLesson, venueLesson, weekLesson = list(row) 
                allLessons.append([int(dayLesson), list(map(int, timeLesson.split())), list(map(int, weekLesson.split()))])

        flag = False
        for day in range(1,7):
            temp = [lessons for lessons in allLessons if lessons[0]==day]
            for lesson1, lesson2 in combinations(temp, 2):
                [dayLesson1, [startTimeLesson1, endTimeLesson1], weekLesson1], [dayLesson2, [startTimeLesson2, endTimeLesson2], weekLesson2] = lesson1, lesson2
                if dayLesson1==dayLesson2 and len(set(weekLesson1).intersection(weekLesson2))>0 and (startTimeLesson1<=startTimeLesson2<endTimeLesson1 or startTimeLesson2<=startTimeLesson1<endTimeLesson2):
                    flag = True
                    break
            if flag:
                break


        else:

            indices = ["0800-0830", "0830-0900", "0900-0930", "0930-1000", "1000-1030", "1030-1100", "1100-1130", "1130-1200", 
                       "1200-1230", "1230-1300", "1300-1330", "1330-1400", "1400-1430", "1430-1500", "1500-1530", "1530-1600", 
                       "1600-1630", "1630-1700", "1700-1730", "1730-1800", "1800-1830", "1830-1900", "1900-1930", "1930-2000", 
                       "2000-2030", "2030-2100", "2100-2130"]
            timetable = {time:[[] for _ in range(6)] for time in indices}

            for index, course in zip(indicesCombo, courses):

                cursor.execute("SELECT type, day, time, remark FROM {} WHERE id={}".format(course,index,))
                result = cursor.fetchall()

                for row in result:

                    type_, day, time, week = list(row) 
                    start, end = list(map(int, time.split()))

                    while start<end:

                        start = str(start)
                        start = "0"*(4-len(start))+start
                        if start[2:]=="00":
                            var = start[:-2]+"30"
                        else:
                            var = str(int(start[:-2])+1)+"00"
                        weeklist, weekstr = list(map(int, week.split())), "Wk "
                        start_, end_ = weeklist[0], weeklist[0]

                        for i in range(1, len(weeklist)):
                            if weeklist[i]-weeklist[i-1]!=1:
                                if weekstr!="Wk ":
                                    weekstr += ", " 
                                weekstr += (str(start_) if start_==end_ else str(start_)+"-"+str(end_))
                                start_ = end_ = weeklist[i]
                            else:
                                end_ = weeklist[i]

                        if weekstr!="Wk ":
                            weekstr += ", "
                        weekstr += str(start_) if start_==end_ else str(start_)+"-"+str(end_)

                        timetable[start+"-"+"0"*(4-len(var))+var][int(day)-1].append(course+" "+type_+"  "+weekstr)
                        start = int(var)

            timetable = {day+1: [row[day] for time, row in sorted(timetable.items(), key = lambda x: x[0])] for day in range(6)}
            span = {day+1: [None for _ in range(len(indices))] for day in range(6)}
            for idx_col, col in enumerate(timetable.values()):
                cont_string, count = col[0], 1
                span[idx_col+1][0] = 1
                for idx_row, curr_string in enumerate(col[1:]):
                    if curr_string==cont_string:
                        span[idx_col+1][idx_row+1-count] += 1
                        count += 1
                    else:
                        span[idx_col+1][idx_row+1] = 1
                        cont_string, count = curr_string, 1
            span = {day+1: [str(_) if _ is not None else _ for _ in span[day+1]] for day in range(6)}
            connection.close()
            return timetable, indices, span, indicesCombo