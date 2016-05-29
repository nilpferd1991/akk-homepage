import flask

from akk.db.engine import session_scope
from akk.db.entities import Song, Artist, Dance

_app = flask.Flask(__name__)


def json_answer(func):
    def func_wrapper(*args, **kwargs):
        results = func(*args, **kwargs)

        return flask.jsonify({"results": results})

    return func_wrapper


@_app.route("/db/list/<type>/<stub>")
@json_answer
def list_songs(type, stub):
    with session_scope() as s:
        class_type = None
        column_name = None
        if type == "songs":
            class_type = Song
            column_name = Song.song_title
        elif type == "artists":
            class_type = Artist
            column_name = Artist.name
        elif type == "dances":
            class_type = Dance
            column_name = Dance.name
        else:
            flask.abort(500)

        stub_regex = "%" + stub + "%"
        results = s.query(class_type).filter(column_name.like(stub_regex)).all()

        return [r.get_dict() for r in results]
