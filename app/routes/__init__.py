from app import app
from app.routes.roster import roster
from app.routes.auth import auth
from app.routes.event import event
from app.routes.meet import meet
from app.routes.player import player
from app.routes.times import times
from app.routes.requires_auth import requires_auth


app.register_blueprint(roster)
app.register_blueprint(auth)
app.register_blueprint(event)
app.register_blueprint(meet)
app.register_blueprint(player)
app.register_blueprint(times)

@app.route('/')
@requires_auth
def index():
    return redirect('/times')
