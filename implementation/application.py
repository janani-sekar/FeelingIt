import os
import random
from datetime import date, timedelta
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mood.db")


@app.route("/", methods=["GET", "POST"])
@login_required
#code for homepage
def index():
    if request.method == "POST":

        #gets today's date
        today = date.today()
        uid = session["user_id"]

        #takes input based on which mood button the user clicks
        mood = request.values.get("mood")

        #checks for null values an returns error
        if mood == None or uid == None:
            return apology(400)

        #selects and checks if mood has already been entered for today
        rows = db.execute("SELECT mood FROM moods WHERE user_id = :user_id AND day = :today", user_id = session["user_id"], today = today)
        if len(rows) == 0:

            #if no mood has been entered, insert mood into database
            db.execute("INSERT INTO moods (user_id, mood) VALUES (:user_id, :mood)", user_id = uid, mood = mood)
        else:

            #if mood already entered for today, update old mood with new input
            db.execute("UPDATE moods SET mood = :mood WHERE user_id = :user_id AND day = :today", mood = mood, user_id = uid, today = today)


    return render_template("index.html")



@app.route("/calendar", methods =["GET", "POST"])
@login_required
def calendar():
    """return past moods for user in calendar"""
    today = date.today()
    print (today)

    #gets date for a week ago
    weekago = today - timedelta(days = 6)

    """current week"""
    #select days from this week, today included
    rows = db.execute("SELECT mood, day FROM moods WHERE day >= :date and user_id = :user_id ORDER BY day", date = weekago, user_id = session["user_id"])
    currentDay = weekago
    moods = []
    i = 0
    for i in range(1,8):
        print (currentDay)
        moods.append({"mood": None, "day": str(currentDay)})
        currentDay = currentDay + timedelta(days = 1)

    #adds moods from this week to list
    for item in rows:
        for mood in moods:
            if item["day"] == mood["day"]:
                mood["mood"] = item["mood"]

    """last week"""
    twoweeksago = today - timedelta(days = 13)
    #selects days from last week
    rowstwo = db.execute("SELECT mood, day FROM moods WHERE day >= :date AND day <:weekago AND user_id = :user_id ORDER BY day", date = twoweeksago, weekago = weekago, user_id = session["user_id"])
    currentDaytwo = twoweeksago
    moodstwo = []
    j = 0

    #adds all the moods from last week to list
    for j in range(1,8):
        moodstwo.append({"mood": None, "day": str(currentDaytwo)})
        currentDaytwo = currentDaytwo + timedelta(days = 1)
    for item in rowstwo:
        for mood in moodstwo:
            if item["day"] == mood["day"]:
                mood["mood"] = item["mood"]

    """two weeks ago"""
    threeweeksago = today - timedelta(days = 20)
    #same logic, selects days from two weeks ago
    rowsthree = db.execute("SELECT mood, day FROM moods WHERE day >= :date AND day <:twoweeksago AND user_id = :user_id ORDER BY day", date = threeweeksago, twoweeksago = twoweeksago, user_id = session["user_id"])
    currentDaythree = threeweeksago
    moodsthree = []
    k = 0

    #adds all the moods from two weeks ago to list
    for k in range(1,8):
        moodsthree.append({"mood": None, "day": str(currentDaythree)})
        currentDaythree = currentDaythree + timedelta(days = 1)
    for item in rowsthree:
        for mood in moodsthree:
            if item["day"] == mood["day"]:
                mood["mood"] = item["mood"]

    return render_template("calendar.html", moods = moods, moodstwo = moodstwo, moodsthree = moodsthree)



@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    today = date.today()
    weekago = today - timedelta(days = 6)
    #selects mood data for this week
    rows = db.execute("SELECT moods.mood, weight FROM moods JOIN weights ON  moods.mood = weights.mood WHERE day >= :date and user_id = :user_id", date = weekago, user_id = session["user_id"])
    print(rows)
    total = 0
    count = 0

    #calculates weighted average, based on given values in table
    for item in rows:
        total += item["weight"]
        count += 1
    averageWeight = total/count
    if averageWeight > 0:

        #if mood generally positive, randomly select positive advice
        ideas = db.execute("SELECT action FROM weekly WHERE value = 'TRUE'")

    if averageWeight <= 0:

        #if mood generally negative, randomly select negative advice
        ideas = db.execute("SELECT action FROM weekly WHERE value = 'FALSE'")

    reco = random.choice(ideas)

    #daily reccomendation
    moods = db.execute("SELECT mood from moods WHERE day = :today and user_id = :user_id", today = today, user_id = session["user_id"])
    dailyReco = {}

    #checks if mood has already been entered today
    if len(moods) == 0:
        dailyReco["activity"] = "You have not yet entered a mood for today."
    else:

        #selects random advice based on current mood

        dailyMood = moods[0]["mood"]
        dailyIdeas = db.execute("SELECT activity from daily WHERE mood = :mood", mood = dailyMood)
        dailyReco = random.choice(dailyIdeas)

#checks for patterns of anxiety/sadness
    checker = []
    alert = ""
    for item in rows:
        checker.append(item["mood"])
        if checker.count("anxious") >= 3:
            alert = "You seem to be really anxious this week. Is everything ok? It might help to talk to someone you trust."
        if checker.count("sad") >= 3:
            alert = "You seem to be really sad this week. Is everything ok? It might help to talk to someone you trust."

    return render_template("analysis.html", reco = reco, dailyReco = dailyReco, alert = alert)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        #make sure username provided
        if not request.form.get("username"):
            return apology("must provide username", 400)

        #make sure password provided
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        #check if provided password matches confirmation
        elif not request.form.get("password") == request.form.get("confirmpassword"):
            return apology("passwords do not match", 400)

        pwhash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = request.form.get("username"), hash = pwhash)

        session["user_id"] = request.form.get("username")

        return redirect("/")

    else:
        return render_template("register.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
