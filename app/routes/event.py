from flask import *
from app.db import *
from app.routes.requires_auth import *
from app.config import events

event = Blueprint('event', __name__, template_folder='templates')

@event.route('/event', methods=['GET'])
@requires_auth
def show_event():
    gender = session["gender"]
    team = session["team"]

    stroke = request.args.get('stroke')
    data = []
    for event in events:
        if event["stroke"] == stroke:
            data.append({
                "name": str(event["distance"]) + " " + stroke[0].upper() + stroke[1:],
                "timesByPlayer": Player.top_players(stroke, event["distance"], gender, team),
                "totalTimes": Time.top_times(stroke, event["distance"], gender, team)
            })

    return render_template('event.html', stroke=stroke, events=data)
