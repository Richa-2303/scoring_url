from flask import Flask, request, abort, jsonify
import json
import base64
import requests, io
import pandas as pd
from ibm_watson_machine_learning import APIClient

app = Flask(__name__)

CLOUD_API_KEY = "AOp1AIdPxmbFLO5RWdmxgm9u5RU8ck2e1NRurT7qD3I4"
WML_CREDENTIALS = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": CLOUD_API_KEY
}
space_id='ac4d416b-be97-4ae6-826f-159eb627edbb'
deployment_id='5f6054e4-08a3-4a5a-8883-108bfa07afb7'
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
