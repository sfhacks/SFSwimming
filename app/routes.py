import sys
from functools import wraps
from flask import *
from app import app
from app.db import *
import hashlib

hashed_pwd = '763e6715ab44cd899ae1b172cc78d5a7'
disable_login = True
events = [
    {"stroke": "free", "distance": 50},
    {"stroke": "free", "distance": 100},
    {"stroke": "free", "distance": 200},
    {"stroke": "free", "distance": 500},
    {"stroke": "fly", "distance": 50},
    {"stroke": "back", "distance": 50},
    {"stroke": "back", "distance": 100},
    {"stroke": "breast", "distance": 50},
    {"stroke": "breast", "distance": 100},
    {"stroke": "medley", "distance": 100}
]

event_names = list(set([event['stroke'] for event in events]))
event_distances = list(set([event['distance'] for event in events]))

# use this decorator on routes that are protected
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
    return redirect('/times')

# Roster

@app.route('/roster', methods=['GET'])
@requires_auth
def roster():
    return render_template('roster.html', roster = Player.all())

@app.route('/roster', methods=['POST'])
def add_swimmer():
    Player(name = request.form['name']).save()

    return redirect("/roster")

@app.route('/roster', methods=['DELETE'])
def delete_swimmer():
    name = request.args["name"]
    Player.remove(name)

    return "Success", 200

# Login/Logout

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


def validate_pwd(password):
    return hashlib.md5(password.encode()).hexdigest() == hashed_pwd

# Times

@app.route('/times', methods=['GET'])
@requires_auth
def list_all_times():
    # Database+template code for all times
    roster = Player.all()
    meets = Meet.all()
    template = render_template('times.html', roster = roster, strokes = event_names, distances = event_distances, meets = meets)
    return template

@app.route('/times', methods=['POST'])
@requires_auth
def add_time():
    player = Player.objects.get(name = request.form["name"])
    meet = Meet.objects.get(name = request.form["meet"])

    Time(stroke = request.form["stroke"], distance = int(request.form["distance"]), time = (request.form["time"]), player = player.id, meet = meet).save()

    return redirect("/times")

# Event

@app.route('/event', methods=['GET'])
@requires_auth
def show_event():
    stroke = request.args.get('stroke')
    data = []
    for event in events:
        if event["stroke"] == stroke:
            data.append({
            "name": stroke + " " + str(event["distance"]),
            "timesByPlayer": Player.top_players(stroke, event["distance"]),
            "totalTimes": Time.top_times(stroke, event["distance"])
            })

    return render_template('event.html', stroke=stroke, events=data)

# Meets

@app.route('/meets', methods=['GET'])
@requires_auth
def meets():
    return render_template("meets.html", meets = Meet.all())

@app.route('/meets', methods=['POST'])
@requires_auth
def add_meet():
    Meet(name = request.form["name"]).save()
    return redirect("/meets")

# Player

@app.route('/player', methods=['GET']) #Specific event for player
@requires_auth
def player():
    player = Player.objects.get(id=request.args.get('id'))
    stroke = request.args.get('stroke')
    distance = request.args.get('distance')
    times = player.times(stroke = stroke, distance = float(distance))

    return render_template("playerProfile.html", swimmer = player, stroke = stroke + " " + distance, values = times)

@app.route('/playerProfile', methods=['GET']) # All events for player
@requires_auth
def playerProfile():
    player = Player.objects.get(id=request.args.get('id'))
    times = player.times()

    return render_template('fullProfile.html', swimmer=player, values=times)
