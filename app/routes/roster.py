from flask import *
from app.db import *
from app.routes.requires_auth import *

genders = ['M', 'F']
teams = ['Junior Varsity', 'Varsity']

roster = Blueprint('roster', __name__, template_folder='templates')

@roster.route('/roster', methods=['GET'])
@requires_auth
def main():
    return render_template('roster.html', roster = Player.all(), genders = genders, teams = teams)

@roster.route('/roster', methods=['POST'])
@requires_auth
def add_swimmer():
    Player(name = request.form['name'], gender = request.form['gender'], team = request.form['team']).save()
    return redirect("/roster")

@roster.route('/roster', methods=['DELETE'])
@requires_auth
def delete_swimmer():
    name = request.args["name"]
    Player.remove(name)

    return "Success", 200
