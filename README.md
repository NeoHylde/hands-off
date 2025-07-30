# Hands-Off Voice Assistant

Hands-Off is a lightweight voice assistant for desktop systems. It listens for a custom wake word and then records and transcribes your spoken command using Whisper, either locally with faster-whisper or via the OpenAI API. Built in Python, it provides a modular and extensible foundation for creating voice-controlled desktop tools.

## Demo

https://youtu.be/mPXLuGkYVnY

## Features

- Wake word detection using Picovoice Porcupine
- Speech-to-text transcription with:
  - faster-whisper for local GPU-accelerated processing
  - OpenAI Whisper API for cloud-based transcription
- Spotify music playback control including:
- Play, pause, continue, skip, and fast-forward
- Console output of recognized commands
- Local logging of valid transcriptions
- Fully modular Python codebase

## Project Structure

hands-off/
├── main.py                  # Entry point for the application
├── WakeWord.py             # Handles wake word detection and command routing
├── Recorder.py             # Records and transcribes audio using faster-whisper
├── Whisper.py              # Records and transcribes audio using OpenAI Whisper API
├── Music.py                # Integrates Spotify playback via Spotipy
├── requirements.txt        # Python dependencies
├── Hands-Off_en_windows_v3_0_0.ppn  # Wake word model file
├── .env                    # API keys and credentials
└── README.md               # Project documentation

## Setup

1. Clone repo.
2. Download requirements.
3. Create .env with these:
    ACCESS_KEY=your_porcupine_key
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
4. Make sure .ppn file is in base directory.
5. Run with python main.py.

## Remarks
Ensure you have an active Spotify device running to use playback controls

Only one transcription method is active at a time, depending on which Record class is instantiated

The assistant recognizes commands like "play [song]", "pause", "continue", "next", and "skip forward". 
The "next" command is still wip as of 30.07.25
