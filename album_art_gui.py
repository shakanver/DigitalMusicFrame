import requests
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from io import BytesIO
from PIL import Image
from spotify_api_helpers import SpotifyAPIHelpers
from typing import Tuple

class AlbumArtGUI(QWidget):
    def __init__(self, spotify_api_helpers):
        super().__init__()
        self.spotify_api_helpers = spotify_api_helpers

        # set titles
        self.title = ""
        self.subtitle = ""
        self.second_subtitle = ""

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

        # Add song name (title) label
        self.title = QLabel(self)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Add artist name label
        self.subtitle = QLabel(self)
        self.subtitle.setStyleSheet("color: white;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.subtitle)

        # Add album name label
        self.second_subtitle = QLabel(self)
        self.second_subtitle.setStyleSheet("color: white;")
        self.second_subtitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.second_subtitle)

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Create a timer to update the album art and song info every second, by querying the API
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000) #update UI every second

        # Initial load of data
        self.update_ui()

    def update_ui(self):
        try:
            current_track_response = spotify_api_helpers.get_current_track()
            current_track_content = current_track_response['item']
            if not current_track_content: 
                self._set_album_art_and_text(album_art_path="./assets/spotify.png")
            elif current_track_response['currently_playing_type'] == 'track':
                album_art_path, title, subtitle, second_subtitle = self._get_track_info(current_track_content)
                self._set_album_art_and_text(album_art_path=album_art_path, title=title, subtitle=subtitle, second_subtitle=second_subtitle)
            elif current_track_response['currently_playing_type'] == 'episode':
                episode_cover, episode_name = self._get_episode_info(current_track_content)
                self._set_album_art_and_text(album_art_path=episode_cover, title=episode_name)
            else:
                self._set_album_art_and_text(album_art_path="./assets/spotify.png")
        except ValueError as ve:
            if str(ve) == "No track is currently playing on spotify":
                self._set_album_art_and_text(album_art_path="./assets/spotify.png"), str(ve)
        except requests.exceptions.HTTPError as he:
                self._set_album_art_and_text(album_art_path='./assets/close.png', title="ERROR", subtitle=str(he))
        except requests.exceptions.ConnectionError as ce:
                print(f"WARNING: connection error encountered\n{str(ce)}\nre-establishing connection")

    def _get_track_info(self, current_track_obj: any) -> Tuple[str,str,str]:
        # Parse song text info
        song_title = current_track_obj['name']
        artist_name = current_track_obj['artists'][0]['name']
        album_name = current_track_obj['album']['name']

        # Parse album cover art
        # By default just getting the image with the largest dimensions
        album_image_url = current_track_obj['album']['images'][0]['url']
        album_image_result = requests.get(album_image_url)
        album_image = Image.open(BytesIO(album_image_result.content))
        album_art_path = './assets/album_art.png'
        album_image.save(album_art_path, 'PNG')

        return album_art_path, song_title, artist_name, album_name
    
    def _get_episode_info(self, current_track_obj: any) -> Tuple[str, str]:
        print(current_track_obj)
        episode_title = current_track_obj['name']

        # Parse image
        episode_image_url = current_track_obj['images'][0]['url']
        episode_image_result = requests.get(episode_image_url)
        episode_image = Image.open(BytesIO(episode_image_result.content))
        episode_image_path = './assets/album_art.png'
        episode_image.save(episode_image_path, 'PNG')

        return episode_image_path, episode_title
    
    def _set_album_art_and_text(self, album_art_path, title='', subtitle='', second_subtitle=''):
        # Update the album art
        pixmap = QPixmap(album_art_path)
        pixmap = pixmap.scaled(int(self.width() * 0.8), int(self.height() * 0.8), Qt.KeepAspectRatio)
        self.album_art.setPixmap(pixmap)

        # Update the song info text
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.second_subtitle.setText(second_subtitle)
        # self._adjust_text_sizes()

        self._show_screen_dimensions()

    def _show_screen_dimensions(self):
        screen = QApplication.primaryScreen()
        dpi = screen.physicalDotsPerInch()

        print(f"Screen Width (Inches): {self.width()/dpi} | Screen Height (Inches): {self.height()/dpi}")

    def _adjust_text_sizes(self):
        # Get the window dimensions
        window_height = self.height()

        # Adjust the font sizes based on window height
        # Song title gets the largest font size
        title_font_size = int(window_height * 0.05)  # 5% of window height
        self.title.setFont(QFont('Verdana', title_font_size))

        # Song artist gets a medium font size
        artist_font_size = int(window_height * 0.035)  # 3.5% of window height
        self.subtitle.setFont(QFont('Verdana', artist_font_size))

        # Album name gets the smallest font size
        album_font_size = int(window_height * 0.03)  # 3% of window height
        self.second_subtitle.setFont(QFont('Verdana', album_font_size))

# Run the application
if __name__ == '__main__':
    token = input('please enter the login token: ')
    refresh_token = input('please enter the refresh token: ')
    spotify_api_helpers = SpotifyAPIHelpers(token=token, refresh_token=refresh_token)
    app = QApplication(sys.argv)
    window = AlbumArtGUI(spotify_api_helpers)
    window.show()
    sys.exit(app.exec_())