from flask import *
from app.db import *
from app.routes.requires_auth import *

teamroster = Blueprint('teamroster', __name__, template_folder='templates')

@teamroster.route('/teamroster', methods=['GET'])
@requires_auth
def main():
    gender = session["gender"]
    team = session["team"]

    print(session)

    teamname = ("Boys" if session["gender"] == "M" else "Girls") + " " + team

    print(teamname)

    return render_template('teamroster.html', roster = Player.filter_by_team(gender, team), teamname = teamname, path = "team_roster")
