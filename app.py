from flask import Flask, render_template, request
from transcribe import speech_to_text

app = Flask(__name__)
ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    
    audio = request.files["audio"]

    if audio.filename == "":
        return "Please choose a file."

    if allowed_file(audio.filename):

        filepath = "uploads/" + audio.filename
        audio.save(filepath)

        transcript = speech_to_text(filepath)

        return transcript



    else:

        return "Only audio files (.mp3, .wav, .m4a) are allowed."

if __name__ == "__main__":
    app.run(debug=True) 
    