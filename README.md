# DigitalMusicFrame

## Setup

### Register an App on Your Spotify Dashboard
The following documentation from Spotify outlines how you can register your own app via the dashboard.
https://developer.spotify.com/documentation/web-api/concepts/apps


### Python Virtual Environment

To run the application, you'll need to create a Python Virtual Environment with Conda, by performing the following steps:

1. Download the latest stable version of Conda from the following link:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html

2. Create a new virtual environment called DigitalMusicFrame using the following command:

    `conda create --name DigitalMusicFrame  python=3.12.2`

3. Activate the virtual environment using the following command:

    `conda activate DigitalMusicFrame`

4. Install all the required packages using the following command:

    `pip install -r requirements.txt`

### Adding Environment Variables

You'll need to define some environment variables for the application to use in order to authenticate yourself and provide authorization to access your information with spotify. Setup the variables using the following steps:

1. Navigate to the backend folder, and create a file called .env
2. Populate the file with the following contents:
```
CLIENT_ID='ADD YOUR CLIENT ID HERE'
CLIENT_SECRET='ADD YOUR CLIENT SECRET HERE'
REDIRECT_URI='YOUR REDIRECT URL HERE'
APP_PORT='PORT YOUR REGISTERED APP LISTENS TO HERE'
```
Replace the values of each variable based on whats provided on your Spotify Dashboard

## Launch instructions

Follow these instructions to start up the backend

1. Activate the virtual environment by running the following command:

    `conda activate DigitalMusicFrame`

2. Start the login app using the following command:

    `python3 spotify_api.py`

3. Open a browser, and navigate to the login url:

    `http://localhost:{YOUR_PORT_NUMBER_HERE}/login`

    This should return you a token and refresh token like this:

    ```
    {
        "access_token": "YOUR_NEW_TOKEN",
        "expires_in": 3600,
        "refresh_token": "YOUR_NEW_REFRESH_TOKEN",
        "scope": "user-read-currently-playing user-read-private",
        "token_type": "Bearer"
    }
    ```
    NOTE:
    when its your first time authenticating, you'll be redirected to a browser page from spotify, asking if you to authorize your spotify app to access your data. And then it will return the token data as expected

4. Once you've logged in an gotten the token, you can close the login app spotify_api.py, and run the gui app 'album_art_gui.py'. you will be prompted to enter the token and refresh token you were provided with from step 3. Then, you should see the app start.

## Credit for Assets Used
All assets used in this project were accessed from FlatIcon:
https://www.flaticon.com/

Spotify Icon:
"https://www.flaticon.com/free-icons/spotify-sketch" Spotify sketch icons created by Fathema Khanom - Flaticon

Error Icon:
"https://www.flaticon.com/free-icons/close" close icons created by Alfredo Hernandez - Flaticon



