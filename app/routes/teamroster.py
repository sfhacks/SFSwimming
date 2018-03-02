from flask import *
from app.db import *
from app.routes.requires_auth import *

teamroster = Blueprint('teamroster', __name__, template_folder='templates')

@teamroster.route('/teamroster', methods=['GET'])
@requires_auth
def main():
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
    elif gender_team == "boysgold":
        gender = "M"
        team = "Gold"
    elif gender_team == "girlsgold":
        gender = "F"
        team = "Gold"

    if gender == "F":
        full_gender = "Girls"
    elif gender == "M":
        full_gender = "Boys"

    teamname = full_gender + " " + team

    return render_template('teamroster.html', roster = Player.filter_by_team(gender, team), teamname = teamname)
