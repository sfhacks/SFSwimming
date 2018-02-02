from flask import render_template
from app import app
from flask import Markup

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', name='Chech')
