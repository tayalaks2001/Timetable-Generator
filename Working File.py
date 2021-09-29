import pandas as pd 
import numpy as np
import os
import sys
from itertools import product, combinations
from random import shuffle

def printTimetable(indicesCombo):

    columns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    indices = ["0800-0830", "0830-0900", "0900-0930", "0930-1000", "1000-1030", "1030-1100", "1100-1130", "1130-1200", "1200-1230", 
    "1230-1300", "1300-1330", "1330-1400", "1400-1430", "1430-1500", "1500-1530", "1530-1600", "1600-1630", "1630-1700", "1700-1730",
    "1730-1800", "1800-1830", "1830-1900", "1900-1930", "1930-2000", "2000-2030", "2030-2100", "2100-2130"]
    printDF = pd.DataFrame(columns=columns, index=indices)
    printDF = printDF.fillna("")

    for course, index in zip(courses, indicesCombo):
        miniDF = coursesTables[course]
        miniDF = miniDF[miniDF["Index"]==index]
        for rowNum in range(miniDF.shape[0]):
            row = miniDF.iloc[rowNum]
            startTime, endTime = row["Time"].split()
            rowStart = 2*(int(startTime[:2])-8) + (1 if int(startTime[-2:])==30 else 0)
            rowEnd = 2*(int(endTime[:2])-8) + (0 if int(endTime[-2:])==30 else -1)
            printDF.iloc[rowStart:rowEnd+1, row["Day"]-1] = [course]*(rowEnd-rowStart+1)

    print(printDF)

allCoursesPath = r"C:\Users\Jasraj Singh\Desktop\Projects\Timetable Generator\Courses Timetables Pre-processed"

# TAKING INPUT

courses = input("Which courses do you plan to take? ").split()
coursesTables, allIndices, validIndices, numIndices = {}, {}, {}, {}

# IMPORTING RELEVANT SCHEDULES

for course in courses:

    df = pd.read_csv(os.path.join(allCoursesPath, course+".csv"))
    coursesTables[course] = df

    allIndices[course] = list(np.unique(df["Index"]))
    validIndices[course] = []

    while not validIndices[course]:
        indicesChoices = list(map(int, input("Which indices would you prefer for course "+course+"? ").split()))
        if indicesChoices:
            for indexChoice in indicesChoices:
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

    df = coursesTables[course]
    if "Lec/Studio" in df["Type"].values:

        df = df[df["Index"]==validIndices[course][0]]
        df = df[df["Type"]=="Lec/Studio"]
        df = df.reset_index(drop=True)

        for idx in range(df.shape[0]):
            lectureTimings.append([course, df["Day"][idx], list(map(int, df["Time"][idx].split())), list(map(int, df["Remark"][idx].split()))])

# CHECKING CLASHES WHERE AT LEAST ONE OF THE LESSONS IS A LECTURE

lecturesClashing = []
for lecture in lectureTimings:

    courseLecture, dayLecture, [startTimeLecture, endTimeLecture], weekLecture = lecture
    for courseLesson in coursesTables:

        if courseLecture!=courseLesson:

            courseTable = coursesTables[courseLesson]
            for rowNum in range(courseTable.shape[0]):

                indexLesson, typeLesson, groupLesson, dayLesson, timeLesson, venueLesson, weekLesson = courseTable.iloc[rowNum]
                if indexLesson in validIndices[courseLesson] and dayLecture==int(dayLesson) and len(set(weekLecture).intersection(list(map(int, weekLesson.split()))))>0:

                    startTimeLesson, endTimeLesson = list(map(int, timeLesson.split()))
                    if not (endTimeLecture<=startTimeLesson or endTimeLesson<=startTimeLecture):

                        if typeLesson=="Lec/Studio":
                            if [courseLesson, courseLecture] not in lecturesClashing and [courseLecture, courseLesson] not in lecturesClashing:
                                lecturesClashing.append([courseLecture, courseLesson])
                        else:
                            validIndices[courseLesson].remove(indexLesson)

if lecturesClashing:
    for lectures in lecturesClashing:
        print("Lectures", lectures[0], "and", lectures[1], "are clashing!")
    sys.exit()

# CHECKING CLASHES WHERE NONE OF THE LESSSONS IS A LECTURE

indicesCombos = [item for item in product(*validIndices.values())]
shuffle(indicesCombos)
lessonTimings = []

for course in courses:

    df = coursesTables[course]
    step = df.shape[0]//numIndices[course]
    lessonTimings.append({})

    for indexPosition, index in enumerate(allIndices[course]):

        if index in validIndices[course]:

            lessonTimings[-1][index] = []
            dfIndex = df.iloc[step*indexPosition:step*(indexPosition+1)]
            dfIndex = dfIndex[dfIndex["Type"]!="Lec/Studio"]
            dfIndex = dfIndex.reset_index(drop=True)
            
            for rowNum in range(dfIndex.shape[0]):
                indexLesson, typeLesson, groupLesson, dayLesson, timeLesson, venueLesson, weekLesson = dfIndex.iloc[rowNum]
                lessonTimings[-1][index].append([int(dayLesson), list(map(int, timeLesson.split())), list(map(int, weekLesson.split()))])

# lessonTimings looks like [{_ : [[day, [start, end], [weeks]], ...], ...} ...]

for indicesCombo in indicesCombos:

    allLessons = []
    for position, index in enumerate(indicesCombo):
        allLessons.extend(lessonTimings[position][index])
    allLessons.sort(key = lambda x: (x[0], x[1][0]))
    for idx in range(len(allLessons)-1):
        [dayLesson1, [startTimeLesson1, endTimeLesson1], weekLesson1], [dayLesson2, [startTimeLesson2, endTimeLesson2], weekLesson2] = allLessons[idx], allLessons[idx+1]
        if dayLesson1==dayLesson2 and len(set(weekLesson1).intersection(weekLesson2))>0 and (endTimeLesson1>startTimeLesson2 or startTimeLesson1==startTimeLesson2):
            break
    else:
        printTimetable(indicesCombo)
        more = input("Do you want more combinations? ")
        if more.lower()!="yes":
            break
      
# CZ2001 CZ2002 CZ2003 CZ2007 MH2100 MH2500