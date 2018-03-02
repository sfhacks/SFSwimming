from flask import *
from app.db import *
from app.routes.requires_auth import *
from app.config import events


event_names = list(set([event['stroke'] for event in events]))
event_distances = list(set([event['distance'] for event in events]))

times = Blueprint('times', __name__, template_folder='templates')

@times.route('/times', methods=['GET'])
@requires_auth
def list_all_times():
    times = Time.all_times()
    roster = Player.all()
    meets = Meet.all()
    template = render_template('times.html', roster = roster, strokes = event_names, distances = event_distances, meets = meets, times = times)
    return template

@times.route('/times', methods=['POST'])
@requires_auth
def add_time():
    player = Player.objects.get(name = request.form["name"])
    meet = Meet.objects.get(name = request.form["meet"])
    time_seconds = Time.parse_time(request.form["time"])
    str_time = Time.reverse_time(time_seconds)

    Time(stroke = request.form["stroke"], distance = int(request.form["distance"]), time = time_seconds, player = player.id, meet = meet, str_time = str_time).save()

    return redirect("/times")
