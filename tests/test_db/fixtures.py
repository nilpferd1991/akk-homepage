from unittest import TestCase

from akk.db.engine import session_scope
from akk.db.entities import Dance, Artist, Song, User, Playlist, Songlist


class DBTestCase(TestCase):
    def delete_all(self):
        with session_scope() as s:

            for dance in s.query(Dance).all():
                s.delete(dance)
            for artist in s.query(Artist).all():
                s.delete(artist)
            for song in s.query(Song).all():
                s.delete(song)
            for user in s.query(User).all():
                s.delete(user)
            for playlist in s.query(Playlist).all():
                s.delete(playlist)
            for songlist in s.query(Songlist).all():
                s.delete(songlist)
            s.commit()

    def tearDown(self):
        self.delete_all()


class FullDBTestCase(DBTestCase):
    def setUp(self):
        self.delete_all()

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