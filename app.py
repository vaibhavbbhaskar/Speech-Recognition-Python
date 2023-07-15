import os
import io
import tempfile 
import ffmpeg
from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)

# Allowed audio extensions
ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.flac', '.mp4'] 

# Format mappings
format_map = {
    '.mp3': 'wav',
    '.m4a': 'wav',
    '.mp4': 'wav',
    '.flac': 'wav',  
}

# Route handler
@app.route("/", methods=["GET", "POST"])
def index():

    transcript = ""
    message = ""

    if request.method == "POST":

    # Check if audio file was uploaded
        if "file" not in request.files:
            message = "No audio file uploaded"
            return render_template('index.html', message=message)

        file = request.files["file"]

        # Check if filename is empty
        if file.filename == "":
            message = "Empty audio file"
            return render_template('index.html', message=message)

        # Check file extension
        input_ext = os.path.splitext(file.filename)[1].lower()
        if not input_ext in ALLOWED_EXTENSIONS:
            message = "Invalid audio file format"
            return render_template('index.html', message=message)

        # Process valid audio
        if file:

            # Save file
            input_file = file.read()  
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(input_file)
            temp_file.close() 

            # Convert audio to WAV
            try:
                output_format = format_map.get(input_ext, 'wav')
                out, err = (
                    ffmpeg
                    .input(temp_file.name)
                    .output('pipe:', format=output_format)
                    .run(capture_stdout=True)
                )
                wav_audio = io.BytesIO(out)
            
            except ffmpeg.Error:
                message = "Error converting audio"
                return render_template('index.html', message=message) 

            finally:
                os.remove(temp_file.name)

            # Transcribe audio
            if wav_audio:

                recognizer = sr.Recognizer()
                audioFile = sr.AudioFile(wav_audio)

            with audioFile as source:
                data = recognizer.record(source)

            try:
                transcript = recognizer.recognize_google(data)
            
            except sr.UnknownValueError:
                message = "Unable to recognize audio"

            return render_template('index.html', transcript=transcript, message=message)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)