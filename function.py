import pandas as pd 
import numpy as np
import os
import sys
from itertools import product, combinations
from random import shuffle

coursesTables, allIndices, validIndices, numIndices = {}, {}, {}, {}

def main(courses, indicesChoices):

    indicesChoices = {course:indices for [course, indices] in indicesChoices}
    allCoursesPath = "Timetable Generator\Courses Timetables Pre-processed"

    global coursesTables, allIndices, validIndices, numIndices
    
    # IMPORTING RELEVANT SCHEDULES

    for course in courses:

        df = pd.read_csv(os.path.join(allCoursesPath, course+".csv")) 
        coursesTables[course] = df # Delete

        allIndices[course] = list(map(int, np.unique(df["Index"]))) 
        validIndices[course] = []
    
        while not validIndices[course]:
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
        for courseLesson in courses:

            if courseLecture!=courseLesson:

                courseTable = coursesTables[courseLesson]
                for rowNum in range(courseTable.shape[0]):

                    '''if lecture[0]=="CZ2005" and courseLesson=="CZ2003":
                        print(courseTable.iloc[rowNum])'''
                    indexLesson, typeLesson, groupLesson, dayLesson, timeLesson, venueLesson, weekLesson = courseTable.iloc[rowNum]
                    if indexLesson in validIndices[courseLesson] and dayLecture==int(dayLesson) and len(set(weekLecture).intersection(list(map(int, weekLesson.split()))))>0:
                    
                        startTimeLesson, endTimeLesson = list(map(int, timeLesson.split()))
                        if not (endTimeLecture<=startTimeLesson or endTimeLesson<=startTimeLecture):
                            '''if lecture[0]=="CZ2005" and courseLesson=="CZ2003":
                                print("Entered if")'''
                            if typeLesson=="Lec/Studio":
                                if [courseLesson, courseLecture] not in lecturesClashing and [courseLecture, courseLesson] not in lecturesClashing:
                                    lecturesClashing.append([courseLecture, courseLesson])
                            else:
                                validIndices[courseLesson].remove(indexLesson)

    if lecturesClashing:
        for lectures in lecturesClashing:
            print("Lectures", lectures[0], "and", lectures[1], "are clashing!")
        sys.exit()

    return validIndices

def checkNonLectureClashes(courses, validIndices):

    global coursesTables, allIndices, numIndices

    indicesCombos = [list(item) for item in product(*validIndices.values())]
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
            return indicesCombo
        
    # CZ2001 CZ2002 CZ2003 CZ2007 MH2100 MH2500

validIndices = main(["CZ2001", "CZ2002", "CZ2003", "CZ2004", "CZ2005", "CZ2007"], [["CZ2001",[]], ["CZ2002",[]], ["CZ2003",[]], ["CZ2004",[]], ["CZ2005",[]], ["CZ2007",[]]])
print(validIndices)