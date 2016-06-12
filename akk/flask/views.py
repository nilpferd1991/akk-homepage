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


def search_everywhere(stub):
    with session_scope() as session:
        song_results = {value["song_title"]: value for value in get_results_from_stub(session, stub, Song, Song.song_title)}
        song_results.update({value["artist_name"]: value for value in get_results_from_stub(session, stub, Song, Artist.name)})
        song_results.update({value["dance_name"]: value for value in get_results_from_stub(session, stub, Song, Dance.name)})

    return flask.jsonify({"results": list(song_results.values()), "names": list(song_results.keys())})

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


def fill_song_from_args(song, session):
    artist = flask.request.args["artist"]
    dance = flask.request.args["dance"]

    queried_artists = session.query(Artist).filter(Artist.name == artist)
    queried_dances = session.query(Dance).filter(Dance.name == dance)

    song.song_title = flask.request.args["title"]

    try:
        song.artist_id = queried_artists.one().artist_id
    except sqlalchemy.orm.exc.NoResultFound:
        new_artist = Artist()
        new_artist.name = artist
        session.add(new_artist)
        session.commit()
        song.artist_id = new_artist.artist_id

    try:
        song.dance_id = queried_dances.one().dance_id
    except sqlalchemy.orm.exc.NoResultFound:
        new_dance = Dance()
        new_dance.name = dance
        session.add(new_dance)
        session.commit()
        song.dance_id = new_dance.dance_id


@app.route("/db/add_song")
def add_song():
    with session_scope() as session:
        new_song = Song()
        fill_song_from_args(new_song)
        session.add(new_song)

        return "OK"

@app.route("/db/update_song")
def update_song():
    with session_scope() as session:
        song_id = flask.request.args["songID"]

        song = session.query(Song).filter(Song.song_id == song_id).one()

        fill_song_from_args(song, session)
        session.merge(song)

        return "OK"

