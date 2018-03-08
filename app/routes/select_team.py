from flask import *
from app.routes.requires_auth import *

select_team = Blueprint('select_team', __name__, template_folder='templates')

@select_team.route('/selectTeam', methods=['GET'])
def select():
    session['team'] = str(request.args.get('team'))
    return redirect("/roster")

@select_team.route('/changeTeam', methods=['GET'])
@requires_auth
def change():
    return render_template("select_team.html")