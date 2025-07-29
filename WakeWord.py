import os
import pvporcupine
from pvrecorder import PvRecorder
import wave
import struct
import signal
import sys
from dotenv import load_dotenv
from Recorder import Record

class Wake:
    def __init__(self):
        load_dotenv()
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("ACCESS_KEY"),
            keyword_paths=["Hands-Off_en_windows_v3_0_0.ppn"]
        )
        self.recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
        self.whisper = Record()

    def start(self):
        print("listening for wake word")

        try:
            self.recorder.start()
            while True:
                frame = self.recorder.read()
                keyword_index = self.porcupine.process(frame)
                if keyword_index >= 0:
                    print("wake word detected")
                    self.whisper.start()
        except KeyboardInterrupt:
            print("stopping")
        finally:
            self.recorder.stop()
            self.recorder.delete()
            self.porcupine.delete()
