# Speech Recognition in Python

This project is a simple web application for transcribing audio files to text using Python and Google's Speech-to-Text API. The web application allows users to upload .wav files and see the transcribed text.

## Features

- File upload functionality
- Audio transcription using Google's Speech-to-Text API
- Error handling for non-.wav files
- Beautiful and user-friendly interface

## Installation

1. Clone this repository:

git clone https://github.com/yourusername/Speech-Recognition-Python.git

2. Navigate to the project directory:

cd Speech-Recognition-Python

3. Install the necessary Python packages:

python3 -m pip install flask
python3 -m pip install SpeechRecognition

## Usage

1. Start the application:

python app.py

2. Open the link shown in the terminal in a web browser.

3. Upload a .wav audio file and click `Transcribe` to see the transcribed text.

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

## Notes

This web application only supports .wav files. Other audio formats will need to be converted to .wav format before they can be transcribed.
