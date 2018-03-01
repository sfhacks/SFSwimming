from flask import *
from app.db import *
from app.routes.requires_auth import *
from app.config import events

event = Blueprint('event', __name__, template_folder='templates')

@event.route('/event', methods=['GET'])
@requires_auth
def show_event():
    gender_team = session['team']

    if gender_team == "boysjv":
        gender = "M"
        team = "Junior Varsity"
    elif gender_team == "boysvarsity":
        gender = "M"
        team = "Varsity"
    elif gender_team == "girlsjv":
        gender = "F"
        team = "Junior Varsity"
    elif gender_team == "girlsvarsity":
        gender = "F"
        team = "Varsity"

    stroke = request.args.get('stroke')
    data = []
    for event in events:
        if event["stroke"] == stroke:
            data.append({
                "name": stroke + " " + str(event["distance"]),
                "timesByPlayer": Player.top_players(stroke, event["distance"], gender, team),
                "totalTimes": Time.top_times(stroke, event["distance"], gender, team)
            })

    return render_template('event.html', stroke=stroke, events=data)
