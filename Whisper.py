import pyaudio
import os
import wave
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

class Record:
    NEON_GREEN = "\033[92m"
    RESET_COLOUR = "\033[0m"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.chunk_file = "temp_chunk.wav"

    def record_chunk(self, p, stream, file_path, chunk_length=5):
        frames = []
        for _ in range(0, int(16000/1024 * chunk_length)):
            data = stream.read(1024)
            frames.append(data)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))

    def transcribe_chunk(self, file_path):
        with open(file_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file
            )
            return response.text.strip()

    def start(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        accumulated_transcription = ""

        print("listening")

        try:
            self.record_chunk(p, stream, self.chunk_file)
            transcription = self.transcribe_chunk(self.chunk_file)

                
            if transcription.lower() not in {"thank you", "thank you very much"}:
                print(self.NEON_GREEN + transcription + self.RESET_COLOUR)
                accumulated_transcription += transcription + " "

            #os.remove(self.chunk_file)
                

        except KeyboardInterrupt:
            print("\nStopping and saving log...")

            with open("log.txt", "w") as log_file:
                log_file.write(accumulated_transcription)

        finally:
            print("LOG: " + accumulated_transcription)
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    recorder = Record()
    recorder.start()
