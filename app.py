import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import join_room, leave_room, send, SocketIO

from utility import login_required

app = Flask(__name__)

app.config["SECRET_KEY"] = "slkdjflksjdflksjd"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

rooms = {}



db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # we check if the username and password are invalid
        if not request.form.get("username"):
            return render_template("register.html", error="Username is blank." )
        
        if len(request.form.get("username")) > 22:
            return render_template("register.html", error="Username exceeds the maximum length of 24 characters.")

        users = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if users:
            return render_template("register.html", error="Username is not available")

        elif not request.form.get("password"):
            return render_template("register.html", error="missing password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="passwords don't match")
        # after all the checks we hash th pw and insert them to the Database
        hashed = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hashed,
        )

        cookie = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = cookie[0]["id"]
        session["name"] = cookie[0]["username"]

        return redirect("/")

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
        if not request.form.get("username"):
            return render_template("login.html",error="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",error="must provide password")
        

        if len(request.form.get("username")) > 22:
            return render_template("register.html", error="Username exceeds the maximum length of 24 characters.")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html",error="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/mancity")
@login_required
def mancity():
    session["room"] = "mancity"
    session["chat"] = "Manchester City"
    return redirect("/room")


@app.route("/spurs")
@login_required
def spurs():
    session["room"] = "spurs"
    session["chat"] = "Tottenham Hotspur"
    return redirect("/room")


@app.route("/arsenal")
@login_required
def arsenal():
    session["room"] = "arsenal"
    session["chat"] = "Arsenal"
    return redirect("/room")


@app.route("/liverpool")
@login_required
def liverpool():
    session["room"] = "liverpool"
    session["chat"] = "Liverpool"
    return redirect("/room")

@app.route("/aston-villa")
@login_required
def aston():
    session["room"] = "aston-villa"
    session["chat"] = "Aston Villa"
    return redirect("/room")

@app.route("/brighton")
@login_required
def brighton():
    session["room"] = "brighton"
    session["chat"] = "Brighton"
    return redirect("/room")


@app.route("/west-ham")
@login_required
def west():
    session["room"] = "west-ham"
    session["chat"] = "West Ham"
    return redirect("/room")


@app.route("/newcastle")
@login_required
def newcastle():
    session["room"] = "newcastle"
    session["chat"] = "Newcastle"
    return redirect("/room")

@app.route("/crystal-palace")
@login_required
def crystal():
    session["room"] = "crystal-palace"
    session["chat"] = "Crystal Palace"
    return redirect("/room")


@app.route("/man-utd")
@login_required
def man():
    session["room"] = "man-utd"
    session["chat"] = "Manchester United"
    return redirect("/room")

@app.route("/chelsea")
@login_required
def chelsea():
    session["room"] = "chelsea"
    session["chat"] = "Chelsea"
    return redirect("/room")


@app.route("/fulham")
@login_required
def fulham():
    session["room"] = "fulham"
    session["chat"] = "Fulham"
    return redirect("/room")


@app.route("/nott'm-forest")
@login_required
def forest():
    session["room"] = "nottm-forest"
    session["chat"] = "Nottingham Forest"
    return redirect("/room")

@app.route("/wolves")
@login_required
def wolves():
    session["room"] = "wolves"
    session["chat"] = "Wolverhampton"
    return redirect("/room")

@app.route("/brentford")
@login_required
def brentford():
    session["room"] = "brentford"
    session["chat"] = "Brentford"
    return redirect("/room")


@app.route("/everton")
@login_required
def everton():
    session["room"] = "everton"
    session["chat"] = "Everton"
    return redirect("/room")



@app.route("/luton")
@login_required
def luton():
    session["room"] = "luton"
    session["chat"] = "Luton Town"
    return redirect("/room")

@app.route("/burnley")
@login_required
def burnley():
    session["room"] = "burnley"
    session["chat"] = "Burnley"
    return redirect("/room")



@app.route("/bournemouth")
@login_required
def bournemouth():
    session["room"] = "bournemouth"
    session["chat"] = "AFC Bournemouth"
    return redirect("/room")


@app.route("/sheffield-utd")
@login_required
def sheffield():
    session["room"] = "sheffield-utd"
    session["chat"] = "Sheffield United"
    return redirect("/room")








@app.route("/room")
@login_required
def room():
    room = session.get("room")
    chat = session.get("chat")
    if room is None or chat is None or session.get("name") is None:
        return redirect("/")
    
    
    
    messages = db.execute("SELECT * FROM messages WHERE room = ? ORDER BY created_at", room)


    return render_template("chat_room.html", code=room, messages=messages, chat=chat)

@socketio.on("message")
@login_required
def message(data):
    room = session.get("room")
    if not room:
        return
    
    content = {
        "user_id": "System",
        "name": session.get("name"),
        "message": data["data"]
    }

    db.execute("INSERT INTO messages (room, user_id, content) VALUES (?, ?, ?)", room, session["name"], content["message"])

    send(content, to=room)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
@login_required
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    
    join_room(room)

    send({"user_id": "System","name": name, "message": "has entered the room"}, to=room)
    #rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
@login_required
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")





@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



if __name__ == "__main__":
    socketio.run(app, debug=True)