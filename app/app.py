from flask import Flask
from .utils.musicbrainz import process_artist_data
from .utils.db import get_recordings_by_artist, get_relevant_recording

app = Flask(__name__)


@app.route("/search/<name>")
def search(name):
    return get_relevant_recording(name)


@app.route("/fetch/<name>")
def fetch(name):
    process_artist_data(name)
    return get_recordings_by_artist(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
