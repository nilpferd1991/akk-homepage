import pkg_resources
from akk.db.engine import session_scope
from akk.db.entities import *
from flask import g

from akk import app

app.config.update(dict(
    DATABASE=pkg_resources.resource_filename("akk", "db_data/database.db")
))
app.config.from_envvar('AKK_SETTINGS', silent=True)

@app.cli.command("initdb")
def initdb_command():
    from akk.db.engine import init_db
    init_db()
    with session_scope() as s:
        tango = Dance(name="Tango")
        s.add(tango)

        artist = Artist(name="Test Artist")
        s.add(artist)

        song = Song(song_title="Test Song", artist=artist, dance=tango)
        s.add(song)

        another_song = Song(song_title="Another Test Song", artist=artist, dance=tango)
        s.add(song)

        user = User(name="Herbert", password_hash="1", password_salt="2")
        s.add(user)

        playlist = Playlist(user=user, songs=[song, another_song])
        s.add(playlist)

        s.commit()