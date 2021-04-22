@app.route("/login", methods=["GET", "POST"])
def login():   
    # lol ='' innecesario
    # username = '' x2  

    if request.method == "POST":
        username= request.form.get('username')
        # Ensure username was submitted
        if not request.form.get("username"):
           return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        lol= db.execute("SELECT * FROM users WHERE user_name = :username",{"username":request.form.get("username")}).fetchone()
        # db.commit x3 
        if len(lol) != 1 or not check_password_hash(lol[0]["pass"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        lol = dict(lol)
        print(lol)
        session ["user_id"] = lol["id_user"]

        return redirect("/buscar")
    else:
        return render_template('login.html'