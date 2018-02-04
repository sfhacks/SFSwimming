import sys


from flask import flash, redirect, render_template, request, session, abort
from app import app
from app.db import *
import hashlib

hashed_pwd = '763e6715ab44cd899ae1b172cc78d5a7'

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	return render_template('base.html')

@app.route('/roster')
def roster():
	if not session.get('logged_in'):
		return render_template('login.html')
	return render_template('roster.html', roster = getRoster())

@app.route('/roster/add', methods=['POST'])
def add_swimmer():
	# add database code to add swimmer - see login for how to interact with form data
	return render_template('roster.html', roster = getRoster())

@app.route('/login', methods=['POST'])
def login():
	if not request:
		abort(400)
	if validate_pwd(request.form['password']) and request.form['username'] == 'admin':
		session['logged_in'] = True
	else:
		flash('Incorrect password')
	return index()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()

@app.route('/times')
def list_all_times():
	if not session.get('logged_in'):
		return render_template('login.html')
	# Database+template code for all times

@app.route('/add') # Landing page for adding times
def add_time_menu():
	if not session.get('logged_in'):
		return render_template('login.html')
	return render_template('addTime.html', swimmers = getRoster())

@app.route('/addTime', methods=['POST']) # Never direct link here w/o request data -> Form request destination for adding times
def addTime():
	if not request:
		abort(400)
	if not session.get('logged_in'):
		return render_template('login.html')
	# add database code to add swimmer time - see login for how to interact with form
	return add_time_menu()

def validate_pwd(password):
	return hashlib.md5(password.encode()).hexdigest() == hashed_pwd
