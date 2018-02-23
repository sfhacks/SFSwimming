from flask import *
from app.db import *
from app.routes.requires_auth import *


player = Blueprint('player', __name__, template_folder='templates')

@player.route('/player', methods=['GET']) #Specific event for player
@requires_auth
def main():
    player = Player.objects.get(id=request.args.get('id'))
    stroke = request.args.get('stroke')
    distance = request.args.get('distance')
    times = player.times(stroke = stroke, distance = float(distance))

    return render_template("player_event_profile.html", swimmer = player, stroke = stroke + " " + distance, values = times)

@player.route('/playerProfile', methods=['GET']) # All events for player
@requires_auth
def playerProfile():
    player = Player.objects.get(id=request.args.get('id'))
    times = player.times()

    return render_template('player_profile.html', swimmer=player, values=times)
