from flask import Flask, request, abort, jsonify
import json
import base64
import requests, io
import pandas as pd
from ibm_watson_machine_learning import APIClient
import os

app = Flask(__name__)

CLOUD_API_KEY = os.environ['CLOUD_API_KEY']
WML_CREDENTIALS = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": CLOUD_API_KEY
}
space_id=os.environ['space_id']
deployment_id=os.environ['deployment_id']
@app.route('/spaces/<space_id>/deployments/<deployment_id>/predictions', methods=['POST'])
def wml_scoring(space_id, deployment_id):
	print(1)
	if not request.json:
		abort(400)
	wml_credentials = WML_CREDENTIALS
	payload_scoring = {
        "input_data": [
            request.json
        ]
    }

	wml_client = APIClient(wml_credentials)
	wml_client.set.default_space(space_id)

	records_list=[]
	scoring_response = wml_client.deployments.score(deployment_id, payload_scoring)
	return jsonify(scoring_response["predictions"][0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9443, debug=True)
