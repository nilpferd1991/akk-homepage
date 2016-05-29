from akk.db.engine import session_scope
from akk.db.entities import *
from tests.test_db.fixtures import FullDBTestCase


class TestDance(FullDBTestCase):
    def test_dance(self):
        with session_scope() as s:

            dances = s.query(Dance).all()

            self.assertEqual(len(dances), 1)
            self.assertEqual(dances[0].name, "Tango")

    def test_artist(self):
        with session_scope() as s:

            artists = s.query(Artist).all()

            self.assertEqual(len(artists), 1)
            self.assertEqual(artists[0].name, "Test Artist")

    def test_song(self):
        with session_scope() as s:

            songs = s.query(Song).all()

            self.assertEqual(len(songs), 2)
            self.assertEqual(songs[0].song_title, "Test Song")
            self.assertEqual(songs[0].artist.name, "Test Artist")
            self.assertEqual(songs[0].dance.name, "Tango")

    def test_users(self):
        with session_scope() as s:

            users = s.query(User).all()

            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].name, "Herbert")

    def test_playlists(self):
        with session_scope() as s:

            playlists = s.query(Playlist).all()

            self.assertEqual(len(playlists), 1)
            self.assertEqual(playlists[0].user.name, "Herbert")
            self.assertEqual(len(playlists[0].songs), 2)
            self.assertEqual(playlists[0].songs[0].song_title, "Test Song")
            self.assertEqual(playlists[0].songs[1].song_title, "Another Test Song")

    def test_delete_artist(self):
        with session_scope() as s:

            artist = s.query(Artist).one()
            s.delete(artist)
            s.commit()

            self.assertEqual(len(s.query(Artist).all()), 0)
            self.assertEqual(len(s.query(Dance).all()), 1)
            self.assertEqual(len(s.query(Song).all()), 0)
            self.assertEqual(len(s.query(Songlist).all()), 0)
            self.assertEqual(len(s.query(Playlist).all()), 1)
            self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_song(self):
        with session_scope() as s:

            song = s.query(Song).first()
            s.delete(song)
            s.commit()

            self.assertEqual(len(s.query(Artist).all()), 1)
            self.assertEqual(len(s.query(Dance).all()), 1)
            self.assertEqual(len(s.query(Song).all()), 1)
            self.assertEqual(len(s.query(Songlist).all()), 1)
            self.assertEqual(len(s.query(Playlist).all()), 1)
            self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_dance(self):
        with session_scope() as s:

            dance = s.query(Dance).one()
            s.delete(dance)
            s.commit()

            self.assertEqual(len(s.query(Artist).all()), 1)
            self.assertEqual(len(s.query(Dance).all()), 0)
            self.assertEqual(len(s.query(Song).all()), 0)
            self.assertEqual(len(s.query(Songlist).all()), 0)
            self.assertEqual(len(s.query(Playlist).all()), 1)
            self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_user(self):
        with session_scope() as s:

            user = s.query(User).one()
            s.delete(user)
            s.commit()

            self.assertEqual(len(s.query(Artist).all()), 1)
            self.assertEqual(len(s.query(Dance).all()), 1)
            self.assertEqual(len(s.query(Song).all()), 2)
            self.assertEqual(len(s.query(Songlist).all()), 0)
            self.assertEqual(len(s.query(Playlist).all()), 0)
            self.assertEqual(len(s.query(User).all()), 0)

    def test_delete_playlist(self):
        with session_scope() as s:

            playlist = s.query(Playlist).one()
            s.delete(playlist)
            s.commit()

            self.assertEqual(len(s.query(Artist).all()), 1)
            self.assertEqual(len(s.query(Dance).all()), 1)
            self.assertEqual(len(s.query(Song).all()), 2)
            self.assertEqual(len(s.query(Songlist).all()), 0)
            self.assertEqual(len(s.query(Playlist).all()), 0)
            self.assertEqual(len(s.query(User).all()), 1)
