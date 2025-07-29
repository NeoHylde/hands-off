import os
import pvporcupine
from pvrecorder import PvRecorder
import wave
import struct
import signal
import sys
from dotenv import load_dotenv

load_dotenv()



porcupine = pvporcupine.create(
    access_key=os.getenv("ACCESS_KEY"),
    keyword_paths=["Hands-Off_en_windows_v3_0_0.ppn"]
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")

print("listening for wake word")

try:
    recorder.start()
    while True:
        frame = recorder.read()
        keyword_index = porcupine.process(frame)
        if keyword_index >= 0:
            print("wake word detectd")
except KeyboardInterrupt:
    print("stopping")
finally:
    recorder.stop()
    recorder.delete()
    porcupine.delete()
