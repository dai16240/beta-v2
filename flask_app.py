import os
import dataset
import json

DATABASE_URI = os.environ.get('DATABASE_URL')
db = dataset.connect(DATABASE_URI)

pred_table = db['predictions']

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/table')
def table():
	t_headers = ['ΔΙΟ','ΩΡΑ','ΚΩΔ','ΟΜΑΔΕΣ','1','Χ','2','ΠΡΟΒΛΕΨΗ']
	games = [g for g in pred_table.all()]
	return render_template('table.html', games=games, t_headers=t_headers)

@app.route('/predictions')
def get_predictions():
	predictions = []
	for g in pred_table.all():
		predictions.append({
				'img': g['flag'],
				'time': g['time'],
				'trnmnt': g['trnmnt'],
				'gid': g['gid'],
				'home': g['home'],
				'away': g['away'],
				'1': g['one'],
				'X': g['chi'],
				'2': g['two'],
				'prediction': g['prediction']
			})
	return json.dumps({"predictions": predictions})