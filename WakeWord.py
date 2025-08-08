import os
import pvporcupine
from pvrecorder import PvRecorder
import wave
import struct
import signal
import sys
from dotenv import load_dotenv
from Recorder import Record
from Music import Music
from playsound import playsound

class Wake:
    def __init__(self):
        load_dotenv()
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("ACCESS_KEY"),
            keyword_paths=["Hands-Off_en_windows_v3_0_0.ppn"]
        )
        self.recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
        self.whisper = Record()
        self.music = Music()

    def parse_command(self, transcription):
        transcription = transcription.lower()
        
        if transcription.startswith("play"):
            song_name = transcription.replace("play", "").strip()
            self.music.play_track(song_name)

        elif "pause" in transcription:
            self.music.pause_track()

        elif "next" in transcription:
            self.music.next_track()

        elif "skip forward" in transcription:
            self.music.skip_forward(60)

        elif "continue" in transcription:
            self.music.continue_track()

        return ("unknown", transcription)


    def start(self):
        print("listening for wake word")

        try:
            self.recorder.start()
            while True:
                frame = self.recorder.read()
                keyword_index = self.porcupine.process(frame)
                if keyword_index >= 0:
                    print("wake word detected")
                    transcript = self.whisper.start()
                    self.parse_command(transcription=transcript)
        except KeyboardInterrupt:
            print("stopping")
        finally:
            self.recorder.stop()
            self.recorder.delete()
            self.porcupine.delete()