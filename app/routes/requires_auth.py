from functools import wraps
from flask import *
import os

disable_login = True

if os.environ.get('DOCKER'):
    disable_login = False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in') and not disable_login:
            return redirect("/login")
        if disable_login and "team" not in session:
        	session["team"] = "Varisty"
        	session["gender"] = "M"
        return f(*args, **kwargs)
    return decorated
