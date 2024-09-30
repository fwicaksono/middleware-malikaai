import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, x-client-key, x-client-token, x-client-secret, Authorization"
    return response

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/middleware', methods=['POST', 'OPTIONS'])
def middleware():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    print("data", request.json)
    destination_url = request.json['destination_url']
    destination_method = request.json['destination_method'].lower()
    query_params_list = request.json['query_params_list'] if 'query_params_list' in request.json else []
    query_params_list = eval(query_params_list) if isinstance(query_params_list, str) else query_params_list
    body_params_list = request.json['body_params_list'] if 'body_params_list' in request.json else []
    body_params_list = eval(body_params_list) if isinstance(body_params_list, str) else body_params_list
    headers_list = request.json['headers_list'] if 'headers_list' in request.json else []
    headers_list = eval(headers_list) if isinstance(headers_list, str) else headers_list
    query_raw_data = {}
    for k in query_params_list:
        query_raw_data[k] = request.json.get(k)
    body_raw_data = {}
    for k in body_params_list:
        body_raw_data[k] = request.json[k] if k in request.json else request.form[k]
    headers_raw_data = {}
    for k in headers_list:
        headers_raw_data[k] = request.headers.get(k)
    if len(query_raw_data) == 0:
        query_raw_data = None
    if len(headers_raw_data) == 0:
        headers_raw_data = None
    try:
        print("query_raw_data", query_raw_data)
        response = requests.request(
            method=destination_method,
            url=destination_url,
            params=query_raw_data,
            json=body_raw_data,
            headers=headers_raw_data
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status_code": response.status_code,
        "response_data": response.json()
    })
