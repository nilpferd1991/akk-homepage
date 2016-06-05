import os
import tempfile

from akk import app
from akk.db.engine import session_scope, init_db
from akk.db.entities import Dance, Artist, Song, User, Playlist, Songlist

from flask.ext.testing import TestCase


class DBTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.test_client = app.test_client()

        init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class FullDBTestCase(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)

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