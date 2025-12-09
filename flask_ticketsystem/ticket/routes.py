from ticket import app, db
from flask import render_template, request, redirect, url_for
from sqlalchemy import text

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/tickets")
def tickets_page():
    items = [
        {"id":1, "priority":2, "username":"Gustav", "title":"Issue with login"},
        {"id":2, "priority":1, "username":"Anna", "title":"Page not loading"},
        {"id":3, "priority":3, "username":"John", "title":"Feature request"},]
    return render_template("ticket.html", items=items)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("Password")

        print(f"Login request - Username: {username}, Password: {password}")
        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("Invalid username")
            return render_template("login.html")
        elif password is None or isinstance(password, str) is False or len(password) < 3:
            print("Invalid password")
            return render_template("login.html")

        sqlstmt = f"SELECT * FROM bugusers WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing SQL: {sqlstmt}")
        result = db.session.execute(text(sqlstmt))
        user = result.fetchall()
        if not user:
            print("Login failed: No matching user found")
            return render_template("login.html")
        
        print("Login successful")
        resp = redirect(url_for("tickets_page"))
        resp.set_cookie("username", username)
        return resp
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("Password")
        password2 = request.form.get("Password2")

        print(f"Register request - Username: {username}, Password: {password}, Password2: {password2}")
        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("Invalid username")
            return render_template("register.html")
        elif password is None or isinstance(password, str) is False or len(password) < 3:
            print("Invalid password")
            return render_template("register.html")
        elif password2 is None or isinstance(password2, str) is False or password != password2:
            print("Passwords do not match")
            return render_template("register.html")

        sqlstmt = f"SELECT * FROM bugusers WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing SQL: {sqlstmt}")
        result = db.session.execute(text(sqlstmt))
        user = result.fetchall()
        if user:
            print("Register failed: User already exists")
            return render_template("register.html")

        sqlstmt = f"INSERT INTO bugusers (username, password, email_address) VALUES ('{username}', '{password}', 'fuck@you.com')"
        print(f"Executing SQL: {sqlstmt}")
        db.session.execute(text(sqlstmt))
        db.session.commit()

        print("Register successful")
        resp = redirect(url_for("tickets_page"))
        resp.set_cookie("username", username)
        return resp
    return render_template("register.html")