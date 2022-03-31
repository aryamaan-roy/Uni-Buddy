import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import math
from helps import apology, login_required

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
db = SQL("sqlite:///student.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("studentname"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE Name = :username",
                          username=request.form.get("studentname"))

        # Ensure username is not redundant
        if len(rows) != 0 :
            return apology("Username already exists", 403)

        # Ensure password is not redundant
        rows = db.execute("SELECT * FROM students WHERE Hash = :hashpass",
                          hashpass = generate_password_hash(request.form.get("password")))


        if len(rows) != 0 :
            return apology("Password already exists", 403)

        #Ensure both passwords match
        if request.form.get("password") != request.form.get("password_confirmation"):
            return apology("Passwords do not match", 403)
        #insert new user in db
        db.execute("INSERT INTO students(Name, Hash) VALUES(?,?)", request.form.get("studentname"), generate_password_hash(request.form.get("password")))


        iddict = db.execute("select id from students where Name=?", request.form.get("studentname"))
        session["user_id"] = iddict[0]["id"]

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("studentname"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE Name = :studentname",
                          studentname=request.form.get("studentname"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["Hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    if request.method == "POST":
        if not request.form.get("name"):
            return apology("must provide username")
        if not request.form.get("message"):
            return apology("must provide message")
        if not request.form.get("sub"):
            return apology("must provide subject")
        rows = db.execute("select * from students where Name=?", request.form.get("name"))
        if len(rows) != 1:
            return apology("Student does not exist")
        namerow = db.execute("select Name from students where id=?", session["user_id"])
        db.execute("insert into messages values(?,?,?,?)", namerow[0]["Name"], request.form.get("sub"), request.form.get("message"), request.form.get("name"))
        return render_template("message.html")
    else:
        name = db.execute("select Name from students")
        studlist = []
        for row in name:
            studlist.append(row["Name"])
        return render_template("compose.html", studlist=studlist)

@app.route("/message")
@login_required
def message():
    namerow = db.execute("select Name from students where id=?", session["user_id"])
    name = namerow[0]["Name"]
    mssglist = db.execute("select * from messages")
    return render_template("message.html", mssglist=mssglist, name=name)

@app.route("/mathhelp")
@login_required
def mathhelp():
    return render_template("mathhelp.html")

@app.route("/calc", methods=["GET", "POST"])
@login_required
def calc():
    if request.method == "POST":
        if not request.form.get("operation"):
            return apology("Operation not selected")
        if (not request.form.get("num1")) or (not request.form.get("num2")):
            return apology("Numbers not entered")
        try:
            num1 = float(request.form.get("num1"))
            num2 = float(request.form.get("num2"))
        except:
            return apology("Enter only real numbers")
        symbol = str(request.form.get("operation"))
        if symbol == "X":
            answer = float(num1*num2)
        elif symbol == "-":
            answer = float(num1-num2)
        elif symbol == "+":
            answer = float(num1+num2)
        elif symbol == "%":
            num1 = int(num1)
            num2 = int(num2)
            answer = num1%num2
        else:
            answer = float(num1/num2)
        return render_template("ans.html", exp1=num1, exp2=num2, answer=answer, symbol=symbol)
    else:
        return render_template("calc.html")

@app.route("/2variables", methods=["GET", "POST"])
@login_required
def var():
    if request.method == "POST":
        if (not request.form.get("a1")) or (not request.form.get("a2")) or (not request.form.get("b1")) or (not request.form.get("b2")) or (not request.form.get("c1")) or (not request.form.get("c2")) :
            return apology("Enter values")
        try:
            a1 = float(request.form.get("a1"))
            b1 = float(request.form.get("b1"))
            c1 = float(request.form.get("c1"))
            a2 = float(request.form.get("a2"))
            b2 = float(request.form.get("b2"))
            c2 = float(request.form.get("c2"))
        except:
            return apology("Only enter real values")
        y = ((a2*c1) - (a1*c2)) / ((b1*a2) - (a1*b2))
        x = (c1 - (b1*y)) / a1
        eq1 = str(str(a1)+'x + '+str(b1)+'y = '+str(c1))
        eq2 = str(str(a2)+'x + '+str(b2)+'y = '+str(c2))
        ans = str("x is "+str(x)+" and y is "+str(y))
        sym = " and "
        return render_template("ans.html", exp1=eq1, exp2=eq2, answer=ans, symbol=sym)
    else:
        return render_template("2variables.html")

@app.route("/quadratic", methods=["GET", "POST"])
@login_required
def quad():
    if request.method == "POST":
        if (not request.form.get("a")) or (not request.form.get("b")) or (not request.form.get("c")) :
            return apology("Enter values")
        try:
            a = float(request.form.get("a"))
            b = float(request.form.get("b"))
            c = float(request.form.get("c"))
        except:
            return apology("Only enter real values")
        eq = str(str(a)+'x^2 + '+str(b)+'x + '+str(c)+' = 0')
        determinant = (b**2) - (4*a*c)
        if determinant < 0:
            answer = "No real roots"
        elif determinant == 0:
            root = (-1*b) / (2*a)
            answer = str("Only one root = "+str(root))
        else:
            root1 = ((-1*b) + math.sqrt(determinant)) / (2*a)
            root2 = ((-1*b) - math.sqrt(determinant)) / (2*a)
            answer = str("The roots are "+str(root1)+" and "+str(root2))
        return render_template("ans.html", exp1=eq , exp2='' , answer=answer, symbol='')
    else:
        return render_template("quadratic.html")

