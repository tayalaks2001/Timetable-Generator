import pandas as pd 
import os

def extractWeeks(string):
    
    numbers, flag, var = [], 0, ""
    string = string.split(",")

    for substring in string:
        try:
            _ = int(substring)
            numbers.append(substring)
        except:
            if "-" in substring:
                substring = substring.split("-")
                substring[0] = "".join(filter(lambda y: y.isdigit(), substring[0]))
                numbers.extend(list(map(str, list(range(int(substring[0]), int(substring[1])+1)))))
            else:
                substring = "".join(filter(lambda y: y.isdigit(), substring))
                numbers.append(substring)      

    return numbers

allCoursesOriginalPath = "Timetable Generator\Courses Timetables Original"
days = {"Mon":"1", "Tue":"2", "Wed":"3", "Thu":"4", "Fri":"5", "Sat":"6"}

for course in os.listdir(allCoursesOriginalPath):

    df = pd.read_csv(os.path.join(allCoursesOriginalPath,course))
    
    df["Index"] = df["Index"].fillna(method="ffill")
    df["Index"] = df["Index"].apply(lambda x: str(x).strip())

    df["Day"] = df["Day"].apply(lambda x: days[x] if type(x)==str else x)
    df["Time"] = df["Time"].apply(lambda x: " ".join(list(map(str, x.split("-")))) if type(x)==str else x)
    
    df["Remark"] = df["Remark"].apply(lambda x: " ".join(extractWeeks(x.strip())) if type(x)==str else " ".join(list(map(str, list(range(1,14))))))
    
    allCoursesNewPath = "Timetable Generator\Courses Timetables Pre-processed"
    df.to_csv(os.path.join(allCoursesNewPath, course), encoding="utf-8-sig", index=False)