import sqlalchemy
from akk import app

from akk.db.entities import Song, Artist, Dance
from akk.db.engine import session_scope
from akk.flask.functionality import get_results_from_stub
from akk.utilities.json import json_answer_with_scope

import flask


@json_answer_with_scope("song_title")
def list_songs(session, stub):
    return get_results_from_stub(session, stub, Song)


@json_answer_with_scope("name")
def list_artists(session, stub):
    return get_results_from_stub(session, stub, Artist)


@json_answer_with_scope("name")
def list_dances(session, stub):
    return get_results_from_stub(session, stub, Dance)


@json_answer_with_scope("song_title")
def search_everywhere(session, stub):
    song_results = {value["song_id"]: value for value in get_results_from_stub(session, stub, Song, Song.song_title)}
    song_results.update({value["song_id"]: value for value in get_results_from_stub(session, stub, Song, Artist.name)})
    song_results.update({value["song_id"]: value for value in get_results_from_stub(session, stub, Song, Dance.name)})

    return list(song_results.values())

@app.route("/db/delete_song")
def delete_song():
    id = flask.request.args["songID"]

    with session_scope() as session:
        try:
            songs_to_delete = session.query(Song).filter(Song.song_id == id).one()
            session.delete(songs_to_delete)
            return "OK"
        except sqlalchemy.orm.exc.NoResultFound:
            return "Database entry not found.", 500

@app.route("/db/delete/artist/<id>")
def delete_artist(id):
    with session_scope() as session:
        try:
            artist_to_delete = session.query(Artist).filter(Artist.artist_id == id).one()
            session.delete(artist_to_delete)
            return "OK"
        except sqlalchemy.orm.exc.NoResultFound:
            return "Database entry not found.", 500

@app.route("/db/delete/dance/<id>")
def delete_dance(id):
    with session_scope() as session:
        try:
            dances_to_delete = session.query(Dance).filter(Dance.dance_id == id).one()
            session.delete(dances_to_delete)
            return "OK"
        except sqlalchemy.orm.exc.NoResultFound:
            return "Database entry not found.", 500


@app.route("/db/completion")
def completion():
    search_column = flask.request.args["type"]
    search_stub = flask.request.args["term"]

    if search_column == "search":
        return search_everywhere(search_stub)
    elif search_column == "songs":
        return list_songs(search_stub)
    elif search_column == "artists":
        return list_artists(search_stub)
    elif search_column == "dances":
        return list_dances(search_stub)

@app.route("/db/get_song")
@json_answer_with_scope("song_title")
def get_song(session):

    song_id = flask.request.args["songID"]

    return [session.query(Song).filter(Song.song_id == song_id).one().get_dict()]