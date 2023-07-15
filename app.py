import os
import io
import tempfile
import ffmpeg
from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)

format_map = {
    '.mp3': 'wav',
    '.m4a': 'wav',
    '.mp4': 'wav',
    '.flac': 'wav',
}

# Route handler for home page
@app.route("/", methods=["GET", "POST"])
def index():

    transcript = ""
    message = ""

    if request.method == "POST":
            
        # Check for uploaded file
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]

        if file:

        # Save file
            input_file = file.read()
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(input_file)
            temp_file.close()

            # Get file extension
            input_ext = os.path.splitext(temp_file.name)[1].lower()
        
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
            
            # Transcribe audio
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(wav_audio)
        
        except ffmpeg.Error:
            message = "Error converting audio" 
        
        finally:
            os.remove(temp_file.name)

        if wav_audio:
            # Transcribe audio
            with audioFile as source:
                data = recognizer.record(source)
                try:
                    transcript = recognizer.recognize_google(data)
                except sr.UnknownValueError:
                    message = "Unable to recognize audio"

    return render_template('index.html', transcript=transcript, message=message)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)