from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from function_SQL import *
from login import exists
from signup import checkExists, addToDB
from save_to_db import save_to_db
from saved_timetables import saved_timetables
import jinja2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = "dljsaklqk24e21cjn!Ew@@dsa5"

@app.route("/SignUp", methods = ["GET", "POST"])
def signup():

    if request.method=="POST":
        id_ = request.form["id_"]
        password = request.form["password"]
        if checkExists(id_):
            pass
        else:
            addToDB(id_, password)
            flash("Thanks")
            return redirect("/ChooseCourses")

    return render_template("Sign_Up.html")

@app.route("/")
@app.route("/Login", methods = ["GET", "POST"])
def login():

    if request.method=="POST":
        id_ = request.form["ID"]
        password = request.form["Password"]
        if exists(id_, password):
            if "ID" in session:
                session.pop("ID")
            if "Password" in session:
                session.pop("Password")
            session["ID"], session["Password"] = id_, password
            return redirect("/Home")
        else:
            return redirect("/Login")

    return render_template("Login.html")   

@app.route("/Home")
def home():

    return render_template("Home.html")

@app.route("/MyTimetables")
def timetables():
    courselist, indiceslist = saved_timetables(session.get("ID"))
    return render_template("Saved_Timetables.html", l = len(courselist))


@app.route("/PrintSavedTimetable")
def print_saved_timetables():
    pos = int(request.args.get("pos"))
    courselist, indiceslist = saved_timetables(session.get("ID"))
    pos = pos%len(courselist)
    courses = courselist[pos]
    indicesChoice = indiceslist[pos]
    validIndices = main(courses, indicesChoice)
    timetable, timings, span, indicesCombo = check_non_lecture_clashes(courses, validIndices)
    if "Timetable" in session:
        session.pop("Timetable")
    if "Indices Combo" in session:
        session.pop("Indices Combo")
    if "Span" in session:
        session.pop("Span")
    session["Timetable"], session["Indices Combo"], session["Span"] = timetable, indicesCombo, span
    return render_template("Print_Saved_Timetables.html", timetable=timetable, timings=timings, span=span, courses=courses, length=len(courses), pos=pos)


@app.route("/ChooseCourses", methods = ["GET", "POST"])
def choose_courses():

    if request.method=="POST":
        for key in list(session):
            if key!="ID" and key!="Password":
                session.pop(key)
        courses = [request.form["course"+str(i)] for i in range(1,11) if request.form["course"+str(i)]]
        session["Courses"] = courses
        return redirect("/ChooseIndices")
        
    else:
        return render_template("Choose_Courses.html")

@app.route("/ChooseIndices", methods = ["GET", "POST"])
def choose_indices():

    if request.method=="POST":
        courses = session["Courses"]
        indicesChoices = [[course, list(map(int, request.form["Indices"+course].split()))] for course in courses]
        validIndices = main(courses, indicesChoices)
        if "Indices Choices" in session:
            session.pop("Indices Choices")
        session["Indices Choices"] = indicesChoices
        if "Valid Indices" in session:
            session.pop("Valid Indices")
        session["Valid Indices"] = validIndices
        return redirect("/PrintTimetable")

    else:
        courses = session["Courses"]
        return render_template("Choose_Indices.html", courses=courses)

@app.route("/PrintTimetable")
def print_timetable():

    courses, validIndices = session.get("Courses"), session.get("Valid Indices")
    timetable, timings, span, indicesCombo = check_non_lecture_clashes(courses, validIndices)
    if "Timetable" in session:
        session.pop("Timetable")
    if "Indices Combo" in session:
        session.pop("Indices Combo")
    if "Span" in session:
        session.pop("Span")
    session["Timetable"], session["Indices Combo"], session["Span"] = timetable, indicesCombo, span
    return render_template("Print_Timetable.html", timetable=timetable, timings=timings, span=span, courses=courses, length=len(courses))

@app.route("/Confirmation")
def confirmation():
    
    indicesCombo = session.get("Indices Combo")
    save_to_db(session.get("ID"), session.get("Courses"), list(map(str, indicesCombo)))
    return render_template("Confirmation.html", indicesCombo=indicesCombo)   

if __name__ == "__main__":
    app.run(debug=True)