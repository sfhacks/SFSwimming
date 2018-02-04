import sys
from functools import wraps
from flask import flash, redirect, render_template, request, session, abort
from app import app
from app.db import *
import hashlib

hashed_pwd = '763e6715ab44cd899ae1b172cc78d5a7'
disable_login = False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in') and not disable_login:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('base.html')

@app.route('/roster', methods=['GET'])
@requires_auth
def roster():
    return render_template('roster.html', roster = getRoster())

@app.route('/roster', methods=['POST'])
def add_swimmer():
    # add database code to add swimmer - see login for how to interact with form data
    addPlayer(name = request.form['name'])
    return redirect("/roster")

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', hideLogout = True)

@app.route('/login', methods=['POST'])
def auth():
    if not request:
        abort(400)
    if validate_pwd(request.form['password']) and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect("/roster")
    else:
        flash('Incorrect password')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect("/login")

@app.route('/times')
@requires_auth
def list_all_times():
    # Database+template code for all times
    pass

@app.route('/add') # Landing page for adding times
@requires_auth
def add_time_menu():
    return render_template('addTime.html', swimmers = getRoster())

@app.route('/addTime', methods=['POST']) # Never direct link here w/o request data -> Form request destination for adding times
@requires_auth
def addTime():
    if not request:
        abort(400)
    # add database code to add swimmer time - see login for how to interact with form
    return add_time_menu()

def validate_pwd(password):
    return hashlib.md5(password.encode()).hexdigest() == hashed_pwd
