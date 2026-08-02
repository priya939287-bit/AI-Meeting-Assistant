from flask import Flask, render_template, request, redirect, url_for, send_file

import os

from transcribe import speech_to_text
from summary import summarize_text
from action_items import extract_action_items 
from database import (
    save_meeting,
    get_all_meetings,
    search_meetings,
    delete_all_meetings
)

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meetings")
def meetings():

    meetings = get_all_meetings()

    return render_template(
        "meetings.html",
        meetings=meetings
    )


@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    meetings = search_meetings(keyword)

    return render_template(
        "meetings.html",
        meetings=meetings
    )


@app.route("/delete_all", methods=["POST"])
def delete_all():

    delete_all_meetings()

    return redirect(url_for("meetings"))


@app.route("/upload", methods=["POST"])
def upload():

    audio = request.files["audio"]

    if audio.filename == "":
        return "Please choose a file."

    if allowed_file(audio.filename):

        filepath = "uploads/" + audio.filename
        audio.save(filepath)

        transcript = speech_to_text(filepath)

        summary = summarize_text(transcript)

        action_items = extract_action_items(transcript)

        actions = "\n".join(action_items)

        save_meeting(
            transcript,
            summary,
            actions
        )

        return render_template(
            "index.html",
            transcript=transcript,
            summary=summary,
            actions=action_items
        )

    else:
        return "Only audio files (.mp3, .wav, .m4a) are allowed."
@app.route("/download_summary")
def download_summary():

    summary = request.args.get("summary")

    filepath = os.path.join("downloads", "meeting_summary.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(summary)

    return send_file(filepath, as_attachment=True) 


if __name__ == "__main__":
    app.run(debug=True)