from flask import Flask, request, redirect, Response
from dotenv import load_dotenv
import requests
import random
import string
import base64
import json
import os

# Flask App
app = Flask(__name__)

# Environment Variables
load_dotenv()
#TODO: add the port number as a env variable
#TODO: create a readme of how to setup and run the environment
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Cache to store flask app session variables
# TODO: backup cache to file
app_cache = {}

# Helper methods
def generate_random_string(length: int) -> string:
    characters = string.ascii_letters + string.digits  # includes both uppercase, lowercase, and digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_b64_encoded_string(plain_string: string) -> string:
    string_bytes = plain_string.encode()
    string_bytes_b64 = base64.b64encode(string_bytes)
    string_b64_encoded = string_bytes_b64.decode()
    return string_b64_encoded

def refresh_token() -> string:
    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : f'{app_cache['refresh_token']}',
        'client_id' : f'{client_id}'
    }

    response = requests.post(url=url, headers=headers, data=data)
    response.raise_for_status()
    response_json = response.json()
    app_cache['token'] = response_json.get('access_token')
    app_cache['refresh_token'] = response_json.get('refresh_token')

# Endpoints
@app.route('/')
def status():
    return Response("app is running", status=200)

@app.route('/login')
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
        'Authorization': f'Basic {generate_b64_encoded_string(auth_string)}'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }

    token_response = requests.post(url=token_request_url, headers=headers, data=data)

    if token_response.status_code != 200:
        return Response(f"HTTP Error: \n status code: {token_response.status_code} \n message: {token_response.content}", status=500)

    response_as_json = token_response.json()
    app_cache['token'] = response_as_json.get('access_token')
    app_cache['refresh_token'] = response_as_json.get('refresh_token')

    return f'Token acquired!'

@app.route('/currenttrack')
def currenttrack():
    my_info_url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f'Bearer {app_cache['token']}'
    }

    response = requests.get(my_info_url, headers=headers)
    response_content = response.content.decode()

    if not response_content:
        return Response("No track is currently playing on Spotify", status=200)

    if response.status_code != 200:
        error_message = response_content['error']['message']
        if response.status_code == 401 and "The access token expired" in error_message:
            refresh_token()
            headers = {
                "Authorization": f'Bearer {app_cache['token']}'
            }
            response = requests.get(my_info_url, headers=headers)
            response_content = response.content.decode()

    return Response(response_content, status=response.status_code)

if __name__ == '__main__':
    app.run(debug=True, port=3001)