from flask import *
from app.db import *
from app.routes.requires_auth import *
from app.config import events

event = Blueprint('event', __name__, template_folder='templates')

@event.route('/event', methods=['GET'])
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
