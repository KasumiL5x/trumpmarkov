import flask
from api import TrumpGenerator

app = flask.Flask(__name__)
trump = TrumpGenerator()

@app.route('/')
def index():
	tweet = trump.generate()
	return flask.render_template('index.html', prediction_out=tweet)

@app.route('/gen', methods=['GET', 'POST'])
def gen():
	tweet = trump.generate()
	return flask.render_template('index.html', prediction_out=tweet)
