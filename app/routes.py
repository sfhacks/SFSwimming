import sys
from functools import wraps
from flask import flash, redirect, render_template, request, session, abort
from app import app
from app.db import *
import hashlib
import time

class Timer():
    time = 0
    @staticmethod
    def start():
        Timer.time = time.time()

    @staticmethod
    def end():
        print(time.time()-Timer.time)


hashed_pwd = '763e6715ab44cd899ae1b172cc78d5a7'
disable_login = True
events = [
    {"stroke": "free", "distance": 50},
    {"stroke": "free", "distance": 100},
    {"stroke": "fly", "distance": 50},
    {"stroke": "fly", "distance": 100}
]

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in') and not disable_login:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('base.html')

@app.route('/roster', methods=['GET'])
@requires_auth
def roster():
    return render_template('roster.html', roster = getRoster())

@app.route('/roster', methods=['POST'])
def add_swimmer():
    # add database code to add swimmer - see login for how to interact with form data
    addPlayer(name = request.form['name'])
    return redirect("/roster")

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', hideLogout = True)

@app.route('/login', methods=['POST'])
def auth():
    if not request:
        abort(400)
    if validate_pwd(request.form['password']) and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect("/roster")
    else:
        flash('Incorrect password')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect("/login")

@app.route('/times', methods=['GET'])
@requires_auth
def list_all_times():
    # Database+template code for all times

    Timer.start()

    events_processed = []
    for event in events:
        name = event['stroke'] + " " + str(event['distance'])
        times = getSortedStrokes(stroke = event['stroke'], distance = event['distance'])
        events_processed.append({"name": name, "times": times})

    roster = getRoster()

    Timer.end()

    Timer.start()
    template =  render_template('times.html', roster = roster, strokes = ["free", "fly"], distances = [50, 100], events = events_processed)
    Timer.end()

    return template

@app.route('/times', methods=['POST'])
@requires_auth
def add_time():
    print(request.form)
    player = getPlayer(request.form["name"])
    addStroke(request.form["stroke"], int(request.form["distance"]), float(request.form["time"]), player.id)
    return redirect("/times")

@app.route('/player', methods=['GET'])
@requires_auth
def player():

    id = request.args.get('id')
    player = getPlayerById(id)
    stroke = request.args.get('stroke')
    distance = request.args.get('distance')

    times = getAllTimesForPlayer(stroke,float(distance),id)

    print(player.name)

    return render_template("playerProfile.html", swimmer = player, stroke = stroke + " " + distance, data = times)

def validate_pwd(password):
    return hashlib.md5(password.encode()).hexdigest() == hashed_pwd
