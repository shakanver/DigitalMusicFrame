# DigitalMusicFrame

## Setup

### Create and Register an App on Your Spotify Dashboard



### Python Virtual Environment

To run the backend, you'll need to create a Python Virtual Environment with Conda, by performing the following steps:

1. Download the latest stable version of Conda from the following link:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html

2. Create a new virtual environment called DigitalMusicFrame using the following command:

    `conda create --name DigitalMusicFrame  python=3.12.2`

3. Activate the virtual environment using the following command:

    `conda activate DigitalMusicFrame`

4. Install all the required packages using the following command:

    `pip install -r requirements.txt`

### Adding Environment Variables for the Backend

You'll need to define some environment variables for the backend to use in order to authenticate yourself and provide authorization to access your information with spotify. Setup the variables using the following steps:

1. Navigate to the backend folder, and create a file called .env
2. Populate the file with the following contents:
```
CLIENT_ID='ADD YOUR CLIENT ID HERE'
CLIENT_SECRET='ADD YOUR CLIENT SECRET HERE'
REDIRECT_URI='YOUR REDIRECT URL HERE'
```
Replace the values of each variable based on whats provided on your Spotify Dashboard

## Running the Backend

### Launch instructions

Follow these instructions to start up the backend

1. Activate the virtual environment by running the following command:

    `conda activate DigitalMusicFrame`

2. Start the app using the following command:

    `python3 spotify_api.py`


## Credit for Assets Used
Spotify Icon:
"https://www.flaticon.com/free-icons/spotify-sketch" Spotify sketch icons created by Fathema Khanom - Flaticon

Error Icon:
"https://www.flaticon.com/free-icons/close" close icons created by Alfredo Hernandez - Flaticon



