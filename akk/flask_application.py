import flask

from akk.db.engine import session_scope
from akk.db.entities import Song, Artist, Dance
from akk.utilities.json import json_answer

_app = flask.Flask(__name__)


@_app.route("/db/list/<type>/<stub>")
@json_answer
def list_something(type, stub):
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


if __name__ == "__main__":
    _app.run()