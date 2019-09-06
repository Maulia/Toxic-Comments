import joblib
import json
from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

from preprocess import *


app = Flask(__name__, static_url_path='/static')

model_pencemaran = 'static/models/model_pencemaran.joblib'
model_sara = 'static/models/model_sara.joblib'
model_pornografi = 'static/models/model_porno.joblib'
model_radikal = 'static/models/model_radikalisme.joblib'

with open(model_pencemaran, 'rb') as file:
	cemar = joblib.load(file)

with open(model_sara, 'rb') as file:
	sara = joblib.load(file)

with open(model_pornografi, 'rb') as file:
	grafi = joblib.load(file)

with open(model_radikal, 'rb') as file:
	radikal = joblib.load(file)

def preprocessing(text):
	transformed_text = text.lower()
	transformed_text = remove_n(text)
	transformed_text = remove_newline(transformed_text)
	transformed_text = remove_url(transformed_text)
	transformed_text = remove_twitter_ig_formatting(transformed_text)
	transformed_text = remove_kaskus_formatting(transformed_text)
	transformed_text = translate_emoticon(transformed_text)
	transformed_text = transformed_text.lower()
	transformed_text = tokenize_text(transformed_text)
	transformed_text = remove_repeating_characters(transformed_text)
	transformed_text = transform_slang_words(transformed_text)
	transformed_text = remove_non_alphabet(transformed_text)
	transformed_text = remove_excessive_whitespace(transformed_text)
	transformed_text = transformed_text.lower().strip()
	transformed_text = stop(transformed_text)
	transformed_text = stem(transformed_text)
	return transformed_text

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/about.html')
def about():
	return render_template('about.html')   

@app.route('/predict', methods=['POST'])
def predict():
	if request.method == "POST":
		category = []
		text = request.form['text']
		# text = data['text']
		text = preprocessing(text)
		pred_cemar = cemar.predict([text])
		pred_grafi = grafi.predict([text])
		pred_sara = sara.predict([text])
		pred_radikal = radikal.predict([text])
		if len(text)==0:
			category.append('HARAP MASUKKAN KOMENTAR')
		else:
			if pred_cemar==1:
				category.append('PENCEMARAN NAMA BAIK')
			if pred_grafi==1:
				category.append('PORNOGRAFI')
			if pred_sara==1:
				category.append('SARA')
			if pred_radikal==1:
				category.append('RADIKALISME')
			if pred_cemar==0 and pred_grafi==0 and pred_sara==0 and pred_radikal==0:
				category.append('NETRAL')
		# if not category:
		# 	category.append('HARAP MASUKKAN KOMENTAR')
		return render_template('index.html', predict=category)

if __name__ == "__main__":
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)