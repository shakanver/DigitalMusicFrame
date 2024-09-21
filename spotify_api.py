from flask import Flask, request, redirect, Response, jsonify
from dotenv import load_dotenv
import requests
import random
import string
import base64
import json
import os
from spotify_api_helpers import SpotifyAPIHelpers

# Flask App
app = Flask(__name__)

# Environment Variables
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
app_port = os.getenv('APP_PORT')

# Helper methods
def generate_random_string(length: int) -> string:
    characters = string.ascii_letters + string.digits  # includes both uppercase, lowercase, and digits
    return ''.join(random.choice(characters) for _ in range(length))

# TODO: remove if the static method in helpers works
def generate_b64_encoded_string(plain_string: string) -> string:
    string_bytes = plain_string.encode()
    string_bytes_b64 = base64.b64encode(string_bytes)
    string_b64_encoded = string_bytes_b64.decode()
    return string_b64_encoded

# Endpoints
@app.route('/', methods=['GET'])
def status():
    return Response("app is running", status=200)

@app.route('/login', methods=['GET'])
def login():
    state = generate_random_string(16)
    scope = 'user-read-private user-read-currently-playing'
    spotify_auth_url = (
        'https://accounts.spotify.com/authorize?'
        'response_type=code'
        f'&client_id={client_id}'
        f'&scope={scope}'
        f'&redirect_uri={redirect_uri}'
        f'&state={state}'     
    )

    return redirect(spotify_auth_url)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if not state:
        return Response(f'Bad Request: missing state', status=400)

    if not auth_code:
        code_not_provided_error = 'Bad Request: code was not provided'
        if error:
            return Response(f'{code_not_provided_error}, error returned: \n {error}', status=400)
        else:
            return Response(code_not_provided_error, status=400)
        
    token_request_url = 'https://accounts.spotify.com/api/token'
    auth_string = f'{client_id}:{client_secret}'

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {SpotifyAPIHelpers.generate_b64_encoded_string(auth_string)}'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }

    token_response = requests.post(url=token_request_url, headers=headers, data=data)

    if token_response.status_code != 200:
        return Response(f"HTTP Error: \n status code: {token_response.status_code} \n message: {token_response.content}", status=500)

    return token_response.json()

if __name__ == '__main__':
    app.run(debug=True, port=app_port)