from akk import app

from akk.db.entities import Song, Artist, Dance
from akk.flask.functionality import get_results_from_stub
from akk.utilities.json import json_answer_with_scope


@app.route("/db/list/songs/<stub>")
@json_answer_with_scope
def list_songs(session, stub):
    return get_results_from_stub(session, stub, Song)


@app.route("/db/list/artists/<stub>")
@json_answer_with_scope
def list_artists(session, stub):
    return get_results_from_stub(session, stub, Artist)


@app.route("/db/list/dances/<stub>")
@json_answer_with_scope
def list_dances(session, stub):
    return get_results_from_stub(session, stub, Dance)


@app.route("/db/search/<stub>")
@json_answer_with_scope
def search_everywhere(session, stub):
    song_results = get_results_from_stub(session, stub, Song, Song.song_title)
    artists_results = get_results_from_stub(session, stub, Song, Artist.name)
    dances_results = get_results_from_stub(session, stub, Song, Dance.name)

    return song_results + artists_results + dances_results