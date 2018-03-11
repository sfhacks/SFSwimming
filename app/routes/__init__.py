from flask import redirect, session
from app import app
from app.routes.roster import roster
from app.routes.auth import auth
from app.routes.event import event
from app.routes.meet import meet
from app.routes.player import player
from app.routes.times import times
from app.routes.teamroster import teamroster
from app.routes.requires_auth import requires_auth
from app.routes.select_team import select_team


app.register_blueprint(roster)
app.register_blueprint(auth)
app.register_blueprint(event)
app.register_blueprint(meet)
app.register_blueprint(player)
app.register_blueprint(times)
app.register_blueprint(teamroster)
app.register_blueprint(select_team)


@app.route('/')
@requires_auth
def index():
    return redirect('/login')

@app.context_processor
def inject_team():
	print(session)
	if "team" in session:
		return dict(team=("Boys" if session["gender"] == "M" else "Girls") + " " + session["team"])
	else:
		return dict()
    
