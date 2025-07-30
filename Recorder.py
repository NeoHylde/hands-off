from faster_whisper import WhisperModel
import pyaudio
import os
import wave

class Record:
    # ANSI escape codes
    NEON_GREEN = "\033[92m"
    RESET_COLOUR = "\033[0m"

    def __init__(self):
        model_size = "medium.en"
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16")

    def record_chunk(self, p, stream, file_path, chunk_length=1.5):
        frames = []
        for _ in range(0, int(16000/1024 * chunk_length)):
            data = stream.read(1024)
            frames.append(data)
        
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

    def transcribe_chunk(self, model, file_path):
        segments, info = model.transcribe(file_path)
        full_text = "".join([segment.text.strip() for segment in segments])

        if full_text.lower() in {"thank you very much.", "thank you."}:
            return ""

        return full_text

    def start(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        try:    
            print("recording")
            chunk_file = "temp_chunk.wav"
            self.record_chunk(p, stream, chunk_file)
            transcription = self.transcribe_chunk(self.model, chunk_file)   
            print(self.NEON_GREEN + transcription + self.RESET_COLOUR)  
            os.remove(chunk_file)
        except KeyboardInterrupt:
            print("stopping")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            return transcription