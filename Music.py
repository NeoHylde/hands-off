import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time

class Music:
    PURPLE = "\033[95m"
    RESET_COLOUR = "\033[0m"

    def __init__(self):
        if os.path.exists(".cache"):
            os.remove(".cache")
        load_dotenv()

        self.scope = "user-library-read user-modify-playback-state user-read-playback-state"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=self.scope
        ))

        print(self.PURPLE + "authenticated as:" + self.RESET_COLOUR + self.RESET_COLOUR, self.sp.me()['display_name'])

        devices = self.sp.devices()
        if not devices['devices']:
            print("no active devices")
            exit()

        self.device_id = devices['devices'][0]['id']

    

    def play_track(self, track_name):
        results = self.sp.search(q=track_name, type="track", limit=1)
        if not results['tracks']['items']:
            print(self.PURPLE + "song not found." + self.RESET_COLOUR)
            exit()

        track_uri = results['tracks']['items'][0]['uri']
        track_name = results['tracks']['items'][0]['name']
        artist = results['tracks']['items'][0]['artists'][0]['name']

        self.sp.start_playback(device_id=self.device_id, uris=[track_uri])
        print(self.PURPLE + f"now playing: {artist} – {track_name}." + self.RESET_COLOUR)

    def pause_track(self):
        try:
            self.sp.pause_playback(device_id=self.device_id)
            print(self.PURPLE + "pausing." + self.RESET_COLOUR)
        except spotipy.exceptions.SpotifyException as e:
            print(f"spotify API error: {e}")

    def continue_track(self):
        try:
            self.sp.start_playback(device_id=self.device_id)
            print(self.PURPLE + "continuing." + self.RESET_COLOUR)
        except spotipy.exceptions.SpotifyException as e:
            print(f"spotify API error: {e}")

    def next_track(self):
        try:
            self.sp.next_track(self.device_id)
        except spotipy.exceptions.SpotifyException as e:
            print(f"spotify API error: {e}")

    def skip_forward(self, seconds=60):
        try:
            playback = self.sp.current_playback()
            if playback and playback['is_playing']:
                current_position = playback['progress_ms']
                new_position = current_position + (seconds * 1000)
                self.sp.seek_track(new_position, device_id=self.device_id)
                print(self.PURPLE +  f"skipped forward {seconds} seconds." + self.RESET_COLOUR)
            else:
                print("no track currently playing.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"spotify API error: {e}")


        


