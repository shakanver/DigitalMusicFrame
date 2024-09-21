import requests
from dotenv import load_dotenv
import os
import json
import string
import base64

class SpotifyAPIHelpers:
    def __init__(self, token, refresh_token):
        self.token = token
        self.refresh_token = refresh_token
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.app_port = os.getenv('APP_PORT')
        self.spotify_api_url = f'http://localhost:{self.app_port}'

    def get_current_track(self) -> dict:
        my_info_url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {
            "Authorization": f'Bearer {self.token}'
        }

        #TODO: add a try-catch here, to handle ConnectionError: Connnection Reset by Peer
        response = requests.get(my_info_url, headers=headers)
        response_content = response.content.decode()

        if not response_content:
            raise ValueError("No track is currently playing on spotify")

        if response.status_code != 200:
            error_contents = json.loads(response_content)
            error_message = error_contents['error']['message']
            if response.status_code == 401 and "The access token expired" in error_message:
                self._refresh_token()
                headers = {
                    "Authorization": f'Bearer {self.token}'
                }
                response = requests.get(my_info_url, headers=headers)
                response.raise_for_status()
                response_content = response.content.decode()

        return json.loads(response_content)

    def _refresh_token(self) -> None:
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
        self.token = response_json.get('access_token')
        self.refresh_token = response_json.get('refresh_token')

        print("TOKEN REFRESHED")

    @staticmethod
    def generate_b64_encoded_string(plain_string: string) -> string:
        string_bytes = plain_string.encode()
        string_bytes_b64 = base64.b64encode(string_bytes)
        string_b64_encoded = string_bytes_b64.decode()
        return string_b64_encoded
