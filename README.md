# Hands-Off Voice Assistant

Hands-Off is a lightweight, privacy-focused voice assistant for desktop systems. It listens for a custom wake word and then records and transcribes your spoken command using Whisper, either locally with `faster-whisper` or via the OpenAI API. Built in Python, it offers a modular and extensible foundation for creating voice-controlled desktop tools.

## Features

- Wake word detection using Picovoice Porcupine
- Speech-to-text transcription via:
  - `faster-whisper` (local, GPU-accelerated)
  - or OpenAI Whisper API (cloud-based)
- Prints transcribed command to console
- Logs all valid transcriptions to a file
- Modular Python implementation

## Project Structure

hands-off/
├── main.py # Entry point: initializes WakeWord listener
├── WakeWord.py # Handles wake word detection via Porcupine
├── Recorder.py # Records audio and uses faster-whisper for local transcription
├── Whisper.py # Alternative transcription using OpenAI's Whisper API
├── Hands-Off_en_windows_v3_0_0.ppn # Custom wake word file
└── .env # Stores your API keys

