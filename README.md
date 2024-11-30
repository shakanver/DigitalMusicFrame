# DigitalMusicFrame

## Setup

This section outlines the pre-requisite setup steps that need to be taken in order to launch the app.

### Register an App on Your Spotify Dashboard
The following documentation from Spotify outlines how you can register your own app via the dashboard.
https://developer.spotify.com/documentation/web-api/concepts/apps

NOTE: when registering you app specify the port number as 3001

### Python Virtual Environment

To run the application, you'll need to create a Python Virtual Environment with Conda, by performing the following steps:

1. Download the latest stable version of Conda from the following link:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html

2. Create a new virtual environment called DigitalMusicFrame using the following command:

    `conda create --name digiframe  python=3.9.2`

    NOTE: I'm using an older version of python because this project is running on a raspberry pi 3, which cant run newer python versions

3. Activate the virtual environment using the following command:

    `conda activate digiframe`

4. Install all the required packages using the following command:

    `pip install -r requirements.txt`

## Launch instructions

### Launching the api

1. Open a terminal, navigate to the DigitakMusicFrame project

2. Activate the virtual environment you created in the setup stage by running the following command:

    `conda activate digiframe`

3. Start the login app using the following command:

    `python3 spotify_api.py`

3. Open a browser, and navigate to the login url:

    `http://localhost:3001/login`

and enter your login details and which will include your client ID and client secret. You should be able to obtain this by going to your spotify dashboard, clicking on the app you created during setup and navigating to the settings of that app.


## Credit for Assets Used
All assets used in this project were accessed from FlatIcon:
https://www.flaticon.com/

Spotify Icon:
"https://www.flaticon.com/free-icons/spotify-sketch" Spotify sketch icons created by Fathema Khanom - Flaticon

Error Icon:
"https://www.flaticon.com/free-icons/close" close icons created by Alfredo Hernandez - Flaticon



