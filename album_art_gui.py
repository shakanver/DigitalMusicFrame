import requests
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from io import BytesIO
from PIL import Image
from spotify_api_helpers import SpotifyAPIHelpers

class AlbumArtGUI(QWidget):
    def __init__(self, spotify_api_helpers):
        super().__init__()
        self.spotify_api_helpers = spotify_api_helpers
        self.album_art_path = ""
        self.song_title = ""
        self.artist_name = ""
        self.album_name = ""

        # Set window properties
        self.setWindowTitle('Album Art GUI')
        self.setGeometry(100, 100, 400, 600)

        # Set background color to black
        self.setStyleSheet("background-color: black;")

        # Create a layout
        self.layout = QVBoxLayout()

        # Add album art (centered)
        self.album_art = QLabel(self)
        self.album_art.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.album_art)

        # Add song name, artist, and album text (centered)
        self.song_info = QLabel(self)
        self.song_info.setStyleSheet("color: white;")
        self.song_info.setFont(QFont('Arial', 14))
        self.song_info.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.song_info)

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Create a timer to update the album art and song info every second, by querying the API
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000) #update UI every 5 seconds

        # Initial load of data
        self.update_ui()

    def update_ui(self):
        # Send GET request to API to get songs
        self.parse_data_from_spotify_api()

        # Update the album art
        pixmap = QPixmap(self.album_art_path)
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        self.album_art.setPixmap(pixmap)

        # Update the song info text
        song_text = f"{self.song_title}\n{self.artist_name}\n{self.album_name}"
        self.song_info.setText(song_text)

    def parse_data_from_spotify_api(self) -> None:
        try:
            current_track_response = spotify_api_helpers.get_current_track()
            self.song_title = current_track_response['item']['name']
            self.artist_name = current_track_response['item']['artists'][0]['name']
            self.album_name = current_track_response['item']['album']['name']
            album_image_url = current_track_response['item']['album']['images'][0]['url']
            album_image_result = requests.get(album_image_url)
            album_image = Image.open(BytesIO(album_image_result.content))
            self.album_art_path = './assets/album_art.png'
            album_image.save(self.album_art_path, 'PNG')
            
        except ValueError as ve:
            if str(ve) == "No track is currently playing on spotify":
                self.album_art_path = "./assets/spotify.png"
        except requests.exceptions.HTTPError as he:
                self.album_art_path = "./assets/close.png"
                self.song_title = "ERROR"
                self.artist_name = str(he)

# Run the application
if __name__ == '__main__':
    token = input('please enter the login token: ')
    refresh_token = input('please enter the refresh token: ')
    spotify_api_helpers = SpotifyAPIHelpers(token=token, refresh_token=refresh_token)
    app = QApplication(sys.argv)
    window = AlbumArtGUI(spotify_api_helpers)
    window.show()
    sys.exit(app.exec_())