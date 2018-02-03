import sys


from flask import flash, redirect, render_template, request, session, abort
from app import app
from app.db import *
import hashlib

from flask import Markup

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

@app.route('/login', methods=['POST'])
def login():
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
def list_times():

@app.route('/add')
def add_time():    

def validate_pwd(password):
	return hashlib.md5(password.encode()).hexdigest() == hashed_pwd

	