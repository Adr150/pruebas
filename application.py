import os
import requests
import json

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from funciones import *


app = Flask(__name__)

""" # Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set") """

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://rzaakpzbspyfur:4cb6bef35b1a9f8f242206dc68132267df048c38590111606543c29a81195442@ec2-54-196-111-158.compute-1.amazonaws.com:5432/d2a0d7svr23q77")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():

    return render_template("index.html")

@app.route("/search")
@login_required
def search():
    return render_template("search.html")
 

@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    """Buscando el libro"""

    if not request.args.get("q"):
        return apology("informacion insuficiente",403)
    
    q = '%' + request.args.get("q")+ '%'

    consulta = "SELECT * FROM books where isbn LIKE :q OR title like :q OR author like :q;"
 
    rows = db.execute(consulta,{"q":q}).fetchall()

    print(len(rows))

    if len(rows) == 0:
        return apology("No esta :c", 404)
    


    return render_template("books.html",rows=rows)

@app.route("/book",methods=["GET","POST"])
@login_required
def info():
    if not request.args.get("isbn"):
        return apology("No hay nada que mostrar",403)
    
    #user_id = session["user_id"]
    q = request.args.get("isbn")

    consulta = "SELECT * FROM books where isbn = :q;"
    row = db.execute(consulta,{"q":q}).fetchone()

    comentarios = db.execute("SELECT * FROM comments INNER JOIN users ON user_id = id WHERE b_isbn = :isbn;", {"isbn":row["isbn"]}).fetchall()

    puntos = db.execute("SELECT SUM(points) FROM comments WHERE b_isbn = :isbn;", {"isbn":row["isbn"]}).fetchone()
    rowo = {}
    rowo["resenas"] = len(comentarios)
    if len(comentarios) == 0:
        rowo["points"] = 0
    else:
        rowo["points"] = puntos[0] // rowo["resenas"] 

    ginfo = lookup(q)

    #print(ginfo)




    


    
    return render_template("book.html",row=row,comments = comentarios, rowo=rowo, ginfo = ginfo)


@app.route("/comment", methods=["GET", "POST"])
def comment():

    if not request.form.get("commentary"):
        return apology("Necesitas comentar algo :c")
    
    
    user_id = session["user_id"]
    text = request.form.get("commentary")
    points = request.form.get("points")
    isbn = request.form.get("book")

    insert = "INSERT INTO comments(points,comment,b_isbn,user_id) VALUES(:points,:comment,:isbn,:id);"

    try:
        consulta = db.execute(insert,{"points":points,"comment":text,"isbn":isbn,"id":user_id})
        db.commit()
    except:
        return apology("Solo puedes comentar una vez",403)
    

    return redirect("/book?isbn="+isbn)



@app.route("/api", methods=["GET", "POST"])
def api():
    if not request.args.get("isbn"):
        return apology("No hay nada que mostrar",404)

    consulta = "SELECT * FROM books where isbn = :q;"
    row = db.execute(consulta,{"q":request.args.get("isbn")}).fetchone()

    if not row:
        return apology("No hay nada",404)

    

    comentarios = db.execute("SELECT * FROM comments INNER JOIN users ON user_id = id WHERE b_isbn = :isbn", {"isbn":row["isbn"]}).fetchall()


    puntos = db.execute("SELECT SUM(points) FROM comments WHERE b_isbn = :isbn", {"isbn":row["isbn"]}).fetchone()
    rowo = {}
    
    rowo["title"] = row["title"]
    rowo["author"] = row["author"]
    rowo["year"] = row["yearp"]
    rowo["isbn"] = row["isbn"]
    rowo["review_count"] = len(comentarios)
    if len(comentarios) == 0:
        rowo["points"] = 0
    else:
        rowo["points"] = puntos[0] // rowo["review_count"] 

    json.dumps(rowo)
  
    print(rowo)
 
    #row.update(dic)
    #rowo.update(dic)

    return rowo




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchall()
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["pass"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("You Must Enter a Username")
        elif not request.form.get("password"):
            return apology("You Must Enter a Password")
        elif not request.form.get("confirmation"):
            return apology("Confirm Password")

        user = request.form.get("username")

        pass1 = request.form.get("password")

        pass2 = request.form.get("confirmation")

        if pass1 != pass2:
            return apology("Passwords Don't Match")

        confirm = db.execute("SELECT username FROM users WHERE username = :usern", {"usern":user}).fetchall()

        if(len(confirm) != 0):
            return apology("Username is not available")

        db.execute("INSERT INTO users(username,pass) VALUES(:user,:hash)", {"user":user, "hash":generate_password_hash(pass1)})
        db.commit()

        return redirect('/')

    return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


