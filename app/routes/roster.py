from flask import *
from app.db import *
from app.routes.requires_auth import *

roster = Blueprint('roster', __name__, template_folder='templates')

@roster.route('/roster', methods=['GET'])
@requires_auth
def main():
    return render_template('roster.html', roster = Player.all())

@roster.route('/roster', methods=['POST'])
@requires_auth
def add_swimmer():
    Player(name = request.form['name']).save()

    return redirect("/roster")

@roster.route('/roster', methods=['DELETE'])
@requires_auth
def delete_swimmer():
    name = request.args["name"]
    Player.remove(name)

    return "Success", 200
