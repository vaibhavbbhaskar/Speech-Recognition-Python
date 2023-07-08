from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import os
import io

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    transcript = ""
    message = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if file:
            # Check if the file is a wav file
            _, file_extension = os.path.splitext(file.filename)
            if file_extension.lower() != ".wav":
                message = "Please upload a .wav format file."
            else:
                recognizer = sr.Recognizer()
                audioFile = sr.AudioFile(io.BytesIO(file.read()))
                with audioFile as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, key = None)

    return render_template('index.html', transcript=transcript, message=message)


if __name__== "__main__":
    app.run(debug= True, threaded = True)