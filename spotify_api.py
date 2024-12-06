from flask import Flask, request, redirect, Response, jsonify, render_template
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
import random
import string
import base64
import json
import os

# Flask App
app = Flask(__name__)

# Cache to store some dynamic variables
app_cache = {}

# Environment Variables
load_dotenv()
redirect_uri = os.getenv('REDIRECT_URI')
app_port = os.getenv('APP_PORT')

# Helper methods
def generate_random_string(length: int) -> string:
    characters = string.ascii_letters + string.digits  # includes both uppercase, lowercase, and digits
    return ''.join(random.choice(characters) for _ in range(length))

def refresh_token(self) -> None:
    auth_string = f'{self.client_id}:{self.client_secret}'
    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {self.generate_b64_encoded_string(auth_string)}'
    }

    data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : f'{self.refresh_token}',
        'client_id' : f'{self.client_id}'
    }

    response = requests.post(url=url, headers=headers, data=data)
    response.raise_for_status()
    response_json = response.json()
    app_cache["TOKEN"] = response_json.get('access_token')
    app_cache["REFRESH_TOKEN"] = response_json.get('refresh_token')
    print("TOKEN REFRESHED")

def generate_b64_encoded_string(plain_string: string) -> string:
    string_bytes = plain_string.encode()
    string_bytes_b64 = base64.b64encode(string_bytes)
    string_b64_encoded = string_bytes_b64.decode()
    return string_b64_encoded

def gen_colour_palette_from_album_art(album_art_url):
    image_response = requests.get(album_art_url)
    imgage = Image.open(BytesIO(image_response.content))
    quantized = imgage.quantize(colors=5, kmeans=5)
    convert_rgb = quantized.convert('RGB')
    colors = convert_rgb.getcolors()
    color_str = sorted(colors, reverse=True)
    final_list = []
    for i in color_str:
        final_list.append(i[1])
    
    # Determine the width and height of the final palette image
    swatch_size = 100
    width = swatch_size * len(final_list)
    height = 20
    
    # Create a new image with the determined size
    palette_image = Image.new("RGB", (width, height))
    
    # Draw each color in the palette as a vertical strip
    for i, color in enumerate(final_list):
        for x in range(i * swatch_size, (i + 1) * swatch_size):
            for y in range(height):
                palette_image.putpixel((x, y), color)
    
    # Save the final palette image as a JPEG file
    palette_image.save('static/assets/palette.png', "PNG")

# Endpoints
@app.route('/', methods=['GET'])
def status():
    return Response("app is running", status=200)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # validate inputs
        if not request.form.get("clientid"):
            return Response(response="Please enter a valid client id", status=400)
        if not request.form.get("clientsecret"):
            return Response(response="Please enter a valid client secret", status=400)
        
        app_cache["CLIENT_ID"] = request.form.get("clientid")
        app_cache["CLIENT_SECRET"] = request.form.get("clientsecret")

        # redirect user request to spotify using client id and client secret
        state = generate_random_string(16)
        scope = 'user-read-private user-read-currently-playing user-read-playback-state'
        spotify_auth_url = (
            'https://accounts.spotify.com/authorize?'
            'response_type=code'
            f'&client_id={app_cache["CLIENT_ID"]}'
            f'&scope={scope}'
            f'&redirect_uri={redirect_uri}'
            f'&state={state}'     
        )

        return redirect(spotify_auth_url)

    else:
        return render_template("login.html")

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
    auth_string = f'{app_cache["CLIENT_ID"]}:{app_cache["CLIENT_SECRET"]}'

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

    token_response_json = token_response.json()
    app_cache["TOKEN"] = token_response_json["access_token"]
    app_cache["REFRESH_TOKEN"] = token_response_json["refresh_token"]

    return render_template('album_art.html')

@app.route('/queue')
def queue():
    my_info_url = "https://api.spotify.com/v1/me/player/queue"
    headers = {
        "Authorization": f'Bearer {app_cache["TOKEN"]}'
    }

    response = requests.get(my_info_url, headers=headers)
    response_content = response.content.decode()

    if not response_content:
        return json.dumps('queue is empty')
    
    if response.status_code != 200:
        error_contents = json.loads(response_content)
        error_message = error_contents["error"]["message"]
        if response.status_code == 401 and "The access token expired" in error_message:
            refresh_token()
            headers = {
                "Authorization": f'Bearer {app_cache["TOKEN"]}'
            }
            response = requests.get(my_info_url, headers=headers)
            response.raise_for_status()
            response_content = response.content.decode()
    return json.loads(response_content)

@app.route('/colourpalette', methods=['POST', 'PUT'])
def colourpalette():
    album_art_url = request.args.get('albumArtUrl')
    if not album_art_url:
        return jsonify(message="please provide a valid album art url", status=400)
    
    gen_colour_palette_from_album_art(album_art_url)

    return jsonify(message="palette generated successfully", status=200)

if __name__ == '__main__':
    app.run(debug=True, port=app_port)