import sys


from flask import render_template
from app import app
from app.db import *

from flask import Markup

@app.route('/')
def index():
	return render_template('base.html')


@app.route('/roster')
def roster():
	return render_template('roster.html', roster = getRoster())

