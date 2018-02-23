from flask import *
from app.db import *
from app.routes.requires_auth import *
import hashlib


auth = Blueprint('auth', __name__, template_folder='templates')

hashed_pwd = '763e6715ab44cd899ae1b172cc78d5a7'



@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html', hideLogout = True)

@auth.route('/login', methods=['POST'])
def main():
    if not request:
        abort(400)
    if validate_pwd(request.form['password']) and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect("/roster")
    else:
        flash('Incorrect password')


@auth.route('/logout')
def logout():
    session['logged_in'] = False

    return redirect("/login")

def validate_pwd(password):
    return hashlib.md5(password.encode()).hexdigest() == hashed_pwd
