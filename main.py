from flask import Flask, request, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

# load API Key
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


@app.route('/')
def index():
	return render_template('index.html')


def fetch_name_type_content(json_data):
	result = []
	for entity in json_data['entities']:
		name = entity['name']
		entity_type = entity['type']
		for mention in entity['mentions']:
			result.append({
			    'name': name,
			    'type': entity_type
			})
	return result


@app.route('/analyze', methods=['POST'])
def analyze():
	text = request.form['text']

	# The URL for the API request
	url = f'https://language.googleapis.com/v2/documents:analyzeEntities?key={api_key}'

	# The request payload
	payload = {
	    "document": {
	        "type": "PLAIN_TEXT",
	        "content": text
	    },
	    "encodingType": "UTF8"
	}

	# Make the API request
	response = requests.post(url,
	                         headers={'Content-Type': 'application/json'},
	                         data=json.dumps(payload))

	# Check the response status and process the result
	if response.status_code == 200:
		result = response.json()
		filtered_result = fetch_name_type_content(result)
		return jsonify({'input_text': text, 'output': filtered_result})
	else:
		return f"Error: {response.status_code}\n{response.text}"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
